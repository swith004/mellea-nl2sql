"""One-shot: write tests/questions.json with all 32 benchmark questions.
Run from the repo root: py tests/_build_questions.py
"""
import json
from pathlib import Path

Q = [
    ("q001", "lookup-simple", "How many movies are in the database?", "Count star on movies."),
    ("q002", "lookup-simple", "How many ratings has user 42 submitted?", "Single-table count with where."),
    ("q003", "lookup-simple", "What is the title of the movie with movieId 318?", "Direct id lookup. Baseline must ace this."),
    ("q004", "lookup-simple", "List all distinct genre strings that appear in the movies table.", "SELECT DISTINCT genres."),
    ("q005", "lookup-simple", "How many users have rated at least one movie?", "COUNT DISTINCT userId."),
    ("q006", "lookup-simple", "What is the highest rating value that appears in the ratings table?", "MAX. Should be 5.0."),
    ("q007", "lookup-simple", "How many movies have the exact genre string 'Comedy'?", "Exact match, not LIKE. Trap for baseline."),
    ("q008", "lookup-simple", "How many ratings are exactly 5.0?", "Count with equality on a float."),
    ("q009", "lookup-simple", "What is the tmdbId of the movie with movieId 1?", "Links table lookup."),
    ("q010", "lookup-simple", "How many distinct tags appear in the tags table?", "COUNT DISTINCT tag."),
    ("q011", "join-aggregate", "What is the average rating of 'Toy Story (1995)'?", "Join movies + ratings on title."),
    ("q012", "join-aggregate", "List the top 10 movies by number of ratings, from most to least.", "Group by + order by count desc + limit."),
    ("q013", "join-aggregate", "What is the average rating for each genre string?", "Tests genre-string vs split disambiguation."),
    ("q014", "join-aggregate", "How many movies have at least 100 ratings?", "Group by movieId with HAVING clause."),
    ("q015", "join-aggregate", "Find the 5 movies with the highest average rating among movies that have at least 1000 ratings.", "HAVING + subquery; baseline often forgets filter."),
    ("q016", "join-aggregate", "How many movies were released in 1995, according to the year in parentheses in the title?", "Year must be parsed from title string."),
    ("q017", "join-aggregate", "What are the 3 most common tags applied to the movie 'The Matrix (1999)'?", "Tags + movies join + group by tag."),
    ("q018", "join-aggregate", "How many distinct movies has user 123 tagged?", "COUNT DISTINCT movieId in tags where userId."),
    ("q019", "genre-string", "How many movies include 'Horror' as one of their genres?", "Must handle pipe-separated multi-value column."),
    ("q020", "genre-string", "What is the highest-rated movie whose genres include both 'Action' and 'Comedy', with at least 500 ratings?", "Two LIKE clauses + having."),
    ("q021", "genre-string", "Count movies tagged as having no genres listed.", "Literal string '(no genres listed)', not NULL."),
    ("q022", "date-timestamp", "How many ratings were submitted in 2015?", "Needs 'unixepoch' modifier on strftime."),
    ("q023", "date-timestamp", "What was the earliest rating in the dataset, and what movie was it for?", "MIN timestamp + join."),
    ("q024", "date-timestamp", "How many ratings per year were submitted, from 2000 through 2010?", "Group by year, BETWEEN clause."),
    ("q025", "tricky-ties-nulls", "Which movie or movies have the highest average rating among all movies with exactly 1 rating?", "Ties expected; return all tied rows."),
    ("q026", "tricky-ties-nulls", "List all movies that have no tags in the tags table.", "LEFT JOIN with IS NULL check."),
    ("q027", "tricky-ties-nulls", "Find the user who gave the most 5.0 ratings. If there's a tie, return all tied users.", "Explicit tie handling."),
    ("q028", "tricky-ties-nulls", "For each movie that has at least 50 ratings, what percentage of its ratings are 5.0? List the top 5.", "Conditional aggregate; avoid integer division."),
    ("q029", "tricky-ties-nulls", "Which users have rated every movie in the Toy Story series (Toy Story, Toy Story 2, Toy Story 3, Toy Story 4)?", "Set-containment via HAVING COUNT DISTINCT."),
    ("q030", "unanswerable-schema", "What is the age of user 42?", "No users demographics table in ML-25M."),
    ("q031", "unanswerable-schema", "Which director has the most movies in the database?", "No director data in MovieLens."),
    ("q032", "unanswerable-schema", "What is the box office revenue of the highest-grossing Comedy?", "No revenue column."),
]

data = [
    {
        "id": qid,
        "category": cat,
        "question": question,
        "gold_sql": "",
        "expected_rows": [],
        "notes": notes,
    }
    for qid, cat, question, notes in Q
]

out = Path("tests/questions.json")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {out} with {len(data)} questions.")