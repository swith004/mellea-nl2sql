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

## Database

This project uses the MovieLens Latest Small dataset,
published by GroupLens Research at the University of Minnesota.

Dataset:
https://grouplens.org/datasets/movielens/latest/

Download:
https://files.grouplens.org/datasets/movielens/ml-latest-small.zip

### Database setup

Download and extract the dataset:

```bash
mkdir -p data
curl -L --fail -o data/ml-latest-small.zip https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
unzip -q data/ml-latest-small.zip -d data
```

Create and populate the SQLite database:

```bash
python load_movielens.py
```

The database is generated at `data/movielens.db`.

Running the script lists the loaded tables and their row counts.

### Database schema

**movies**
- movieId: INTEGER, primary key
- title: TEXT
- genres: TEXT (pipe-separated genres)

**ratings**
- userId: INTEGER
- movieId: INTEGER, foreign key to movies
- rating: REAL (0.5 to 5.0)
- timestamp: INTEGER (Unix timestamp)
- Primary key: (userId, movieId)

**tags**
- userId: INTEGER
- movieId: INTEGER, foreign key to movies
- tag: TEXT
- timestamp: INTEGER (Unix timestamp)

**links**
- movieId: INTEGER, primary key and foreign key to movies
- imdbId: TEXT
- tmdbId: INTEGER

### Relationships

`ratings.movieId`, `tags.movieId`, and `links.movieId`
reference `movies.movieId`.

MovieLens provides anonymized user IDs but no separate users table.

### Data attribution

Dataset: MovieLens Latest Small, GroupLens Research,
University of Minnesota.

Harper, F. M., & Konstan, J. A. (2015).
The MovieLens Datasets: History and Context.
ACM Transactions on Interactive Intelligent Systems, 5(4).
https://doi.org/10.1145/2827872

See the original dataset README for usage and redistribution conditions.
