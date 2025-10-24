# Project: buscaescuela
**Description**: Python web scraper for Buenos Aires school search, organized for scalability and best practices. This file contains LLM agent guidelines and coding standards for the project.

## Notes for the LLM agent (GitHub Copilot)
- Always add imports at the top of files.
- Do not ask if I want to test the code, assume I will.
- If there are indentation errors, fix them automatically.
- If there are import errors, adjust imports to use absolute paths relative to the src package.
- Avoid unnecessary comments; code should be self-explanatory. If comments are needed, always write them in English.
- Use meaningful and descriptive variable, function, and class names.
- Keep functions short and focused on a single responsibility.
- Avoid code duplication; use functions or classes to reuse logic.
- Validate and handle exceptions gracefully.
- Keep the project structure modular and organized.
- Use a requirements.txt or pyproject.toml to manage dependencies.
- Write docstrings for public functions and classes (in English).
- Use version control (git) and write clear commit messages.
- Keep configuration and secrets out of the codebase (use .env files).
- Regularly refactor and clean up unused code.
- Write tests for critical logic if the project grows.
- Follow PEP8 style guide for Python code formatting.
