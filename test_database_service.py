from services.database_service import (
    create_tables,
    get_all_chunks,
    save_chunk,
)

from services.embedding_service import get_embedding


create_tables()

text = "Python ve Django ile backend uygulamaları geliştirdim."

embedding = get_embedding(text)

save_chunk(
    source="test_cv.txt",
    chunk_text=text,
    embedding=embedding,
)

chunks = get_all_chunks()

print("Veritabanındaki kayıt sayısı:")
print(len(chunks))

print("\nSon kayıt:")
print("ID:", chunks[-1]["id"])
print("Kaynak:", chunks[-1]["source"])
print("Metin:", chunks[-1]["text"])
print("Embedding uzunluğu:", len(chunks[-1]["embedding"]))
