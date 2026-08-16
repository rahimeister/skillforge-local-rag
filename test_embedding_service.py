from services.embedding_service import get_embedding


text = "Python ve Django ile backend geliştirme öğreniyorum."

embedding = get_embedding(text)

print("Metin:")
print(text)

print("\nEmbedding uzunluğu:")
print(len(embedding))

print("\nİlk 10 değer:")
print(embedding[:10])