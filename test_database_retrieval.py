from services.retrieval_service import retrieve_relevant_chunks


question = "Backend geliştirme konusunda hangi deneyimlerim var?"

results = retrieve_relevant_chunks(
    question=question,
    top_k=3,
)

print(f"Soru: {question}")
print("-" * 60)

for index, result in enumerate(results, start=1):
    print(f"{index}. Benzerlik: {result['score']:.4f}")
    print(f"Kaynak: {result['source']}")
    print(f"Metin: {result['text']}")
    print()