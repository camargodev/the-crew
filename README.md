# the-crew

To set up on a new instance:
- python -m venv venv
- Set-ExecutionPolicy Unrestricted -Scope Process
- \venv\Scripts\activate
- New-Item src\__init__.py -ItemType File
- New-Item tests\__init__.py -ItemType File

Dependencies:
- pip install pytest