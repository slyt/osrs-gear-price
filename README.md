# osrs-gear-price

## Development
Create virtual environment and install dev requirements with pip-sync.

    python -m venv env
    pip install pip-tools
    pip-sync requirements-dev.txt

## Formatting
This repo uses black and flake8 as well as other

## Compiling requirements

    pip-compile
    pip-compile --extra=dev --output-file=requirements-dev.txt pyproject.toml
