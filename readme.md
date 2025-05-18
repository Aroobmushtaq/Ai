# What is **Poetry**?

**Poetry** is a tool that helps you:

- **Manage your Python project**  
- **Handle all packages/dependencies** (like `fastapi`, `pandas`, etc.)  
- **Keep everything organized**, similar to `npm` for JavaScript or `pipenv` for Python

---

## Install **Poetry** (so your system can use it)

### On **Windows** (PowerShell):

Open **PowerShell** (not CMD), then run this command:

```powershell```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

---

## Install Project Dependencies

- If you're working with a project that already has a `pyproject.toml` file, run:
poetry install --no-root

### Create a New Poetry Project
- To start a new project with Poetry, run:
poetry init

## Manage Dependencies
- To add a new dependency:
poetry add <package-name>
- To remove a dependency:
poetry remove <package-name>

---
# What is FastApi
FastAPI is a modern, fast web framework for building APIs with Python. It supports async, auto-generates docs, and is ideal for high-performance backend services.

# What is Uvicorn
Uvicorn is a lightning-fast ASGI server used to run FastAPI apps. It handles incoming web requests and supports async features for high performance.

## Installing FastAPI and Uvicorn
- Add FastAPI with standard dependencies:
poetry add "fastapi[standard]"

- Add Uvicorn (ASGI server):
poetry add uvicorn

## Run with Python
- Use poetry run to execute Python scripts:
poetry run python <relative-path-to-file>

## Run with FastAPI/Uvicorn
- Use poetry run with Uvicorn to serve FastAPI applications:
poetry run uvicorn <relative-path-to-module>:app --reload
  - Replace / with . in the path, and change .py to :app.

