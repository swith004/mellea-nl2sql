
import sqlite3
from pathlib import Path
import mellea

DB_PATH = Path(__file__).resolve().parent / "data" / "movielens.db"

QUESTION = "Show the movie IDs and titles of the first 5 movies, ordered by movieId."

def main():
    if not DB_PATH.exists():
        print("Database not found. Run load_movielens.py first.")
        return

    # Connect to Ollama using Granite
    session = mellea.start_session(
        backend_name="ollama",
        model_id="granite4.1:3b"
    )

    # Give the model the database schema and question
    prompt = f"""
    You are writing a query for a SQLite database.

    The database contains this table:
    movies (
        movieId INTEGER PRIMARY KEY,
        title TEXT,
        genres TEXT
    )

    Question: {QUESTION}

    Write a SQL SELECT statement to answer the question.
    Return exactly two columns: movieId and title.
    Order by movieId ascending and return only 5 rows.
    Return only SQL, with no explanation or markdown.
    Start the response with SELECT.
    """

    response = session.instruct(prompt)
    sql = str(response).strip()

    # Remove markdown formatting if the model includes it
    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    print("Question:", QUESTION)
    print("\nGenerated SQL:")
    print(sql)

    # Only allow read-only SELECT queries
    if not sql.upper().startswith("SELECT "):
        raise ValueError("The model did not generate a SELECT query.")

    # Connect to SQLite and run the generated query
    with sqlite3.connect(DB_PATH.as_uri() + "?mode=ro", uri=True) as conn:
        rows = conn.execute(sql).fetchall()

    print("\nResults:")
    for movie_id, title in rows:
        print(f"{movie_id}: {title}")

    # Verify the results are correct
    expected = [
        (1, "Toy Story (1995)"),
        (2, "Jumanji (1995)"),
        (3, "Grumpier Old Men (1995)"),
        (4, "Waiting to Exhale (1995)"),
        (5, "Father of the Bride Part II (1995)")
    ]

    if rows != expected:
        raise AssertionError("Query results did not match the expected rows.")

    print("\nResults verified successfully.")


if __name__ == "__main__":
    main()
