import os
import logging
import time
from pathlib import Path
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Configure Google Gemini API
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)  # type: ignore
    else:
        logger.warning("GEMINI_API_KEY not found in environment variables")
except Exception as e:
    logger.error(f"Error configuring Google Gemini API: {str(e)}")

async def video_to_prompt(video_path):
    """
    Convert a video of browser interaction to a task prompt for an LLM agent.
    Directly uploads the video to Google Gemini API for analysis.
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        str: Generated task prompt for the LLM agent
    """
    try:
        # Validate video file
        if not os.path.exists(video_path):
            return "Error: Video file not found."
        
        # Check if file is a video
        valid_extensions = ['.mp4', '.avi', '.mov', '.webm', '.mkv']
        if not any(video_path.lower().endswith(ext) for ext in valid_extensions):
            return "Error: File does not appear to be a supported video format."
        
        # Check if Gemini API key is configured
        if not GEMINI_API_KEY:
            return "Error: Google Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."
        
        # Initialize Gemini model
        model = genai.GenerativeModel(model_name='gemini-2.0-flash')  # type: ignore
        
        # Craft the prompt for Gemini
        system_prompt = """
        You are an expert at analyzing browser interactions and converting them to clear, detailed instructions.
        Analyze this video of someone using a web browser.
        
        Your task is to:
        1. Identify the website(s) being visited and the specific actions taken
        2. Note any data entry, button clicks, navigation, or form submissions
        3. Identify any specific text being searched for or entered
        4. Determine the overall goal of the browser session
        5. Create a detailed, step-by-step prompt that a browser automation agent could follow to reproduce these actions
        
        Format your response as follows:
        ```
        Task: [One sentence describing the overall goal]
        
        Steps:
        1. [Detailed instruction for step 1]
        2. [Detailed instruction for step 2]
        ...
        
        Additional details:
        - [Any important information like specific search terms, URLs, or data inputs]
        - [Any timing considerations or conditional actions]
        ```
        
        Focus only on providing this prompt without any additional commentary.
        """
        
        # Load the video file
        with open(video_path, 'rb') as f:
            video_data = f.read()
        
        # Set up the generation config
        generation_config = genai.GenerationConfig(  # type: ignore
            temperature=0.2,
            top_p=0.95,
            top_k=64,
            max_output_tokens=2048,
        )
        
        # Determine the MIME type based on file extension
        mime_type = "video/mp4"  # Default
        if video_path.lower().endswith('.webm'):
            mime_type = "video/webm"
        elif video_path.lower().endswith('.mov'):
            mime_type = "video/quicktime"
        elif video_path.lower().endswith('.avi'):
            mime_type = "video/x-msvideo"
        elif video_path.lower().endswith('.mkv'):
            mime_type = "video/x-matroska"
        
        # Send the video to Gemini for analysis
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [
                    {"text": system_prompt},
                    {"inline_data": {
                        "mime_type": mime_type,
                        "data": base64.b64encode(video_data).decode('utf-8')
                    }}
                ]}
            ],
            generation_config=generation_config
        )
        
        # Extract text from response
        prompt = response.text if hasattr(response, 'text') else None
        
        # If text attribute doesn't exist, try alternatives
        if prompt is None and hasattr(response, 'parts'):
            prompt = response.parts[0].text if response.parts else "Error: Unable to extract response text"
        
        # Format the prompt for the agent
        if prompt and not prompt.startswith("Error:"):
            logger.info(f"Successfully generated prompt from video: {video_path}")
        else:
            logger.error(f"Failed to generate prompt: {prompt}")
        
        return prompt or "Error: No valid response from Gemini model"
    
    except Exception as e:
        logger.error(f"Error in video_to_prompt: {str(e)}")
        return f"Error generating prompt: {str(e)}" 