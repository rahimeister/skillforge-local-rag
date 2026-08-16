import json
import sqlite3
from pathlib import Path


DB_PATH = Path("data/skillforge.db")


def get_connection():
    """SQLite veritabanı bağlantısı oluşturur."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DB_PATH)


def create_tables():
    """RAG için gerekli tabloyu oluşturur."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_chunk(
    source: str,
    chunk_text: str,
    embedding: list[float],
):
    """Bir metin parçasını ve embedding'ini veritabanına kaydeder."""

    connection = get_connection()
    cursor = connection.cursor()

    embedding_json = json.dumps(embedding)

    cursor.execute(
        """
        INSERT INTO document_chunks (
            source,
            chunk_text,
            embedding
        )
        VALUES (?, ?, ?)
        """,
        (
            source,
            chunk_text,
            embedding_json,
        ),
    )

    connection.commit()
    connection.close()


def get_all_chunks():
    """Veritabanındaki bütün chunk'ları getirir."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, source, chunk_text, embedding
        FROM document_chunks
        """
    )

    rows = cursor.fetchall()
    connection.close()

    results = []

    for row in rows:
        results.append(
            {
                "id": row[0],
                "source": row[1],
                "text": row[2],
                "embedding": json.loads(row[3]),
            }
        )

    return results


def delete_chunks_by_source(source: str):
    """
    Belirli bir kaynağa ait eski chunk'ları siler.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM document_chunks
        WHERE source = ?
        """,
        (source,),
    )

    connection.commit()
    connection.close()