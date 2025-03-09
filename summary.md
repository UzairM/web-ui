# Web-UI Codebase Summary

## Root Directory

- **webui.py**: The main application file that implements the Gradio-based web interface for controlling browser agents. Contains functions for running different types of browser agents, configuring LLM settings, and managing UI interactions.

- **requirements.txt**: Lists Python dependencies for the project.

- **Dockerfile** and **Dockerfile.arm64**: Docker configuration files for building the application container for x86 and ARM architectures respectively.

- **docker-compose.yml**: Docker Compose configuration for running the application.

- **supervisord.conf**: Configuration for Supervisor process control system, likely used to manage the application processes in production.

- **entrypoint.sh**: Shell script used as the Docker container entry point.

- **LICENSE**: License information for the project.

- **README.md**: Project documentation.

- **SECURITY.md**: Security policy and information.

- **.env.example**: Example environment variables configuration.

## src Directory

### agent/

- **custom_agent.py**: Extends the base Agent class with custom functionality. Implements the core agent behavior, including executing actions, managing message flows, and handling the agent's thought process and planning.

- **custom_message_manager.py**: Manages the communication between the agent and LLM, handling message formatting and token management.

- **custom_prompts.py**: Contains custom system and agent message prompts for the LLM to generate appropriate responses.

- **custom_views.py**: Defines data structures and schemas for agent outputs and step information.

### browser/

- **custom_browser.py**: Custom implementation of the browser functionality, extending the base Browser class.

- **custom_context.py**: Manages browser context configurations and settings.

### controller/

- **custom_controller.py**: Controls the execution flow between the agent and browser, managing actions and responses.

### utils/

- **agent_state.py**: Manages the agent's state and provides mechanisms to request the agent to stop.

- **deep_research.py**: Implements advanced web research capabilities, allowing the agent to search for and extract information from the web.

- **default_config_settings.py**: Provides default configuration settings and functions to load and save configurations.

- **llm.py**: Functions for initializing and interacting with various LLM providers.

- **utils.py**: General utility functions used throughout the application, including file management, UI helpers, and more.

## tests Directory

- **test_browser_use.py**: Tests for browser automation functionality.

- **test_deep_research.py**: Tests for the deep research capabilities.

- **test_llm_api.py**: Tests for LLM API integration.

- **test_playwright.py**: Tests for Playwright browser automation.

## assets Directory

- **web-ui.png**: Logo or screenshot image for the web UI.

- **examples/**: Directory containing example configurations or use cases.

## Key Features

1. **Browser Automation**: The system can control a browser to perform tasks specified by the user.

2. **LLM Integration**: Supports various LLM providers for powering the agent's decision-making.

3. **Deep Research**: Capabilities for conducting extensive web research on topics.

4. **Custom Agent**: Implements a customizable agent architecture that can be adapted for different use cases.

5. **Configurable UI**: A Gradio-based web interface for easy interaction with the system.

6. **Recording and History**: Support for recording browser sessions and maintaining history of agent actions.

## Architecture

The system follows a modular architecture with:

1. **Agent**: Core decision-making component that determines what actions to take.

2. **Browser**: Interface to interact with web browsers via Playwright.

3. **Controller**: Manages the execution flow and available actions.

4. **Utils**: Shared utility functions and configuration management.

The system uses asynchronous programming extensively with Python's asyncio for handling concurrent operations and interactions with the browser and LLM APIs.
