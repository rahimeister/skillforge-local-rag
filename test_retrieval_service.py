from services.retrieval_service import retrieve_from_texts


texts = [
    "Python ve Django ile web uygulamaları geliştirdim.",
    "Photoshop kullanarak grafik tasarım çalışmaları yaptım.",
    "SQL ve PostgreSQL veritabanları üzerinde çalıştım.",
    "Git ve GitHub kullanarak projelerimi versiyon kontrolünde tuttum.",
]

question = "Backend geliştirme konusunda hangi deneyimlerim var?"

results = retrieve_from_texts(
    question=question,
    texts=texts,
    top_k=3,
)

print(f"Soru: {question}")
print("-" * 60)

for index, result in enumerate(results, start=1):
    print(
        f"{index}. Benzerlik: {result['score']:.4f}"
    )
    print(result["text"])
    print()