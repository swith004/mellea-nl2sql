# mellea-nl2sql
FIU Student Mellea Project: Ask-Your-Database

Ask a real database questions in plain English and get real answers back — built with Mellea so the generated SQL is validated and automatically repaired if it's wrong.

## Setup
This project requires Python 3.11+ and uv for managing dependencies.

Clone the repository:

git clone https://github.com/swith004/mellea-nl2sql.git
cd mellea-nl2sql

Create a virtual environment:
```bash
uv python install 3.11
uv venv --python 3.11
```
Activate the environment:

Mac/Linux:
```bash
source .venv/bin/activate
```
Windows:
```bash
.venv\Scripts\Activate.ps1
```
Install the dependencies:
```bash
uv pip install -r requirements.txt
```
To check that Mellea installed correctly:
```bash
python -c "import mellea; print('Mellea installed successfully')"
```
Ollama and an IBM Granite model are used for the LLM backend.

## How to contribute
Fork this repo, pick an open issue, and open a pull request. The interface (CLI, notebook, or web app) is your team's choice
