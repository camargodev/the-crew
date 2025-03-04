# The Crew

This is a python server (soon to-be) for an online version of the card game The Crew.

## Setting up the repo

(in case I clean up my Windows machine)

### To set up on a new instance

- Run on root (if you want a virtual env):
  - `python -m venv venv`
  - `Set-ExecutionPolicy Unrestricted -Scope Process`
  - `\venv\Scripts\activate`
- Then, for every folder (yes, this is boring):
  - `New-Item __init__.py -ItemType File`

### Dependencies

- `pip install pytest`
- `pip install pytest-cov`
- `pip install punq`
- `pip install pytest-mock`

## To run tests with coverage

- `pytest --cov=src --cov-report=html`
- Open `htmlcov\index.html` on a browser
