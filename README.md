# AI FAQ Assistant for "7-Day AI Agents Email Crash Course"

[![Build Status](https://img.shields.io/travis/com/your-username/your-repo.svg)](https://travis-ci.com/your-username/your-repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered FAQ assistant that can answer questions about a course, using materials from a GitHub repository. This project is the result of the "7-Day AI Agents Email Crash Course" by Alexey Grigorev.

## Overview

This project is a comprehensive, step-by-step guide to building a Retrieval-Augmented Generation (RAG) based AI agent. It addresses the common problem of answering user questions based on a specific knowledge base, in this case, the content of a public GitHub repository containing markdown files.

The project is structured as a 7-day course, covering the entire lifecycle of an AI agent, from data ingestion and processing to building a user interface and evaluating the agent's performance. It serves as a practical, hands-on example for anyone looking to build their own AI agents.

## Features

*   **Data Ingestion**: Fetches and processes data from public GitHub repositories.
*   **Advanced Chunking**: Implements multiple data chunking strategies, including simple character-based, paragraph-based, and intelligent, AI-driven chunking.
*   **Hybrid Search**: Combines lexical search (using `minsearch`) and semantic search (using `sentence-transformers`) for optimal retrieval.
*   **Agentic Framework**: Uses `pydantic-ai` and OpenAI's GPT models to create an agent capable of using tools to answer questions.
*   **Interaction Logging**: Logs all interactions for later analysis and evaluation.
*   **AI-Powered Evaluation**: Includes a system for using an "LLM as a Judge" to evaluate the quality of the agent's responses.
*   **Dual Interfaces**: Provides both a Command-Line Interface (CLI) and a web-based UI built with Streamlit.

## Project Structure

The project is organized into several key Python files:

*   `main.py`: The entry point for the Command-Line Interface (CLI).
*   `app.py`: The entry point for the Streamlit web application.
*   `ingest.py`: Handles the ingestion and indexing of data from the GitHub repository.
*   `search_agent.py`: Defines the AI agent and its interaction logic.
*   `search_tools.py`: Encapsulates the search functionalities (lexical, semantic, and hybrid).
*   `logs.py`: Manages the logging of interactions.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/7-Day-AI-Agents-Email-Crash-Course.git
    cd 7-Day-AI-Agents-Email-Crash-Course
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your OpenAI API Key:**
    Create a `.env` file in the root of the project and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your-api-key-here"
    ```

## Usage

You can interact with the AI FAQ assistant through either the CLI or the Streamlit web UI.

### Command-Line Interface

To run the CLI, execute the following command:

```bash
python aihero/course/main.py
```

The application will initialize the agent and prompt you to ask questions in the terminal.

### Streamlit Web UI

To launch the web-based interface, run the following command:

```bash
streamlit run aihero/course/app.py
```

This will open a new tab in your browser with the chat interface.

## Contributing

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a pull request.

## Tests

Currently, there are no automated tests in this project. Adding a test suite would be a great contribution!

## Credits and Acknowledgments

*   This project is based on the "7-Day AI Agents Email Crash Course" by **Alexey Grigorev**.
*   The project utilizes several open-source libraries, including:
    *   [Streamlit](https://streamlit.io/)
    *   [Pydantic AI](https://github.com/pydantic/pydantic-ai)
    *   [OpenAI Python Library](https://github.com/openai/openai-python)
    *   [Minsearch](https://github.com/alexeygrigorev/minsearch)
    *   [Sentence Transformers](https://www.sbert.net/)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.