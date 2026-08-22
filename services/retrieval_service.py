import math

from services.database_service import get_chunks_by_source
from services.embedding_service import get_embedding


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    İki embedding vektörü arasındaki cosine similarity
    değerini hesaplar.
    """

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def retrieve_relevant_chunks(
    question: str,
    source: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Soruyla en alakalı chunk'ları
    yalnızca belirtilen CV kaynağının içinden bulur.
    """

    if not question.strip():
        return []

    if not source.strip():
        return []

    # Sorunun embedding'ini oluştur
    question_embedding = get_embedding(question)

    # Yalnızca aktif CV'ye ait chunk'ları al
    chunks = get_chunks_by_source(source)

    if not chunks:
        return []

    results = []

    for chunk in chunks:
        score = cosine_similarity(
            question_embedding,
            chunk["embedding"],
        )

        results.append(
            {
                "id": chunk["id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            }
        )

    # En alakalı sonuçlar önce gelsin
    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]