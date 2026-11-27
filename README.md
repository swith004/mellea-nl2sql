# mellea-nl2sql
FIU Student Mellea Project: Ask-Your-Database

Ask a real database questions in plain English and get real answers back — built with Mellea so the generated SQL is validated and automatically repaired if it's wrong.

## Setup
Python 3.11+
pip install mellea
A backend: Ollama running an IBM Granite model locally, or a hosted Granite endpoint
Pick a database

## How to contribute
Fork this repo, pick an open issue, and open a pull request. The interface (CLI, notebook, or web app) is your team's choice

## End-to-end example

Run the example after setting up Ollama and loading the MovieLens database:

```bash
python demo_nl2sql.py
```

Sample question:
"Show the movie IDs and titles of the first 5 movies, ordered by movieId."

The script uses Mellea and Granite to generate SQL, runs the query against the SQLite database, and prints the results.

The expected result is the first five movies by movieId, starting with Toy Story (1995) and Jumanji (1995).
