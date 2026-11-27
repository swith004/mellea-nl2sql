
import csv
import sqlite3
from pathlib import Path

# File locations
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_DIR = DATA_DIR / "ml-latest-small"
DB_PATH = DATA_DIR / "movielens.db"


def read_csv(filename, columns):
    """Read CSV records and convert fields to SQLite-compatible types."""
    with (CSV_DIR / filename).open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield tuple(
                convert(row[column]) if row[column] != "" else None
                for column, convert in columns.items()
            )


def main():
    if not CSV_DIR.is_dir():
        raise FileNotFoundError(
            "MovieLens CSV files not found. Download and extract "
            "ml-latest-small.zip into the data/ directory."
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        # Recreate the database tables
        conn.executescript("""
            DROP TABLE IF EXISTS ratings;
            DROP TABLE IF EXISTS tags;
            DROP TABLE IF EXISTS links;
            DROP TABLE IF EXISTS movies;

            CREATE TABLE movies (
                movieId INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                genres TEXT NOT NULL
            );

            CREATE TABLE ratings (
                userId INTEGER NOT NULL,
                movieId INTEGER NOT NULL,
                rating REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                PRIMARY KEY (userId, movieId),
                FOREIGN KEY (movieId) REFERENCES movies(movieId)
            );

            CREATE TABLE tags (
                userId INTEGER NOT NULL,
                movieId INTEGER NOT NULL,
                tag TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (movieId) REFERENCES movies(movieId)
            );

            CREATE TABLE links (
                movieId INTEGER PRIMARY KEY,
                imdbId TEXT,
                tmdbId INTEGER,
                FOREIGN KEY (movieId) REFERENCES movies(movieId)
            );
        """)

        # CSV filenames and their field types
        tables = {
            "movies": ("movies.csv", {
                "movieId": int, "title": str, "genres": str
            }),
            "ratings": ("ratings.csv", {
                "userId": int, "movieId": int,
                "rating": float, "timestamp": int
            }),
            "tags": ("tags.csv", {
                "userId": int, "movieId": int,
                "tag": str, "timestamp": int
            }),
            "links": ("links.csv", {
                "movieId": int, "imdbId": str, "tmdbId": int
            }),
        }

        # Import CSV data into SQLite
        for table, (filename, columns) in tables.items():
            field_names = ", ".join(columns)
            placeholders = ", ".join("?" for _ in columns)

            conn.executemany(
                f"INSERT INTO {table} ({field_names}) "
                f"VALUES ({placeholders})",
                read_csv(filename, columns)
            )

        # Create indexes to speed up movie lookups
        conn.execute(
            "CREATE INDEX idx_ratings_movieId ON ratings(movieId)"
        )
        conn.execute(
            "CREATE INDEX idx_tags_movieId ON tags(movieId)"
        )

        conn.commit()

        # Verify connection and print all tables
        print(f"Connected to SQLite database: {DB_PATH}")
        print("\nDatabase tables:")

        cursor = conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """)

        for (table_name,) in cursor:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]
            print(f"  {table_name}: {count:,} rows")

        # Verify a known movie exists
        result = conn.execute(
            "SELECT title FROM movies WHERE movieId = ?",
            (1,)
        ).fetchone()

        print("\nSample movie:", result[0] if result else "Not found")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
