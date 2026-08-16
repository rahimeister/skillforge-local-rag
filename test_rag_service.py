from services.rag_service import ask_document


question = "Bu aday hangi teknolojilerle çalışıyor?"

print("\nSORU:")
print(question)

print("\nRAG CEVABI:")
print("-" * 60)

answer = ask_document(question)

print(answer)

print("-" * 60)