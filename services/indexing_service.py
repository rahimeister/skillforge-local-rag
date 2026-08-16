from services.database_service import (
    delete_chunks_by_source,
    save_chunk,
)
from services.document_service import split_text
from services.embedding_service import get_embedding


def index_document(
    source: str,
    text: str,
) -> int:
    """
    Belgeyi chunk'lara böler,
    embedding üretir
    ve SQLite'a kaydeder.
    """

    chunks = split_text(text)

    delete_chunks_by_source(source)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        save_chunk(
            source=source,
            chunk_text=chunk,
            embedding=embedding,
        )

    return len(chunks)