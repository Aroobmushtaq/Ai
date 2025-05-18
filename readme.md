#  What is Poetry?
Poetry is a tool that helps :
Manage your Python project
Handle all packages/dependencies (like fastapi, pandas, etc.)
Keep everything organized (like npm for JavaScript or pipenv for Python)

## Install Poetry (so your system can use it)
### In Windows (PowerShell):
Open PowerShell (not CMD), and run this:
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

## Install Project Dependencies
If you're working with a project that already has a pyproject.toml file, run:
poetry install --no-root
This command installs all required dependencies for the project.

### Create a New Poetry Project
To start a new project with Poetry, run:
poetry init
Follow the prompts to set up your project and define dependencies.


