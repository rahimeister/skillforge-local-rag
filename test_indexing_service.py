from services.database_service import get_all_chunks
from services.indexing_service import index_document


cv_text = """
Yönetim Bilişim Sistemleri öğrencisiyim.

Python, Django, SQL ve Git teknolojileriyle çalışıyorum.
Django kullanarak web uygulamaları geliştiriyorum.

PyQt5 ile masaüstü uygulamalar geliştirdim.

Veri yapıları ve algoritmalar konusunda çalışmalar yapıyorum.

Backend geliştirme ve siber güvenlik alanlarında
kendimi geliştirmeyi hedefliyorum.
"""


count = index_document(
    source="sample_cv.txt",
    text=cv_text,
)

print("Oluşturulan chunk sayısı:", count)

chunks = get_all_chunks()

print("\nToplam veritabanı kaydı:", len(chunks))

print("\nRAW CHUNKS:")
print(chunks)

print("\nVeritabanındaki TÜM kayıtlar:")
print("-" * 60)

for chunk in chunks:
    print("ID:", chunk["id"])
    print("Kaynak:", chunk["source"])
    print("Metin:", chunk["text"])
    print("Embedding uzunluğu:", len(chunk["embedding"]))
    print("-" * 60)