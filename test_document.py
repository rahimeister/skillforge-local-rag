from services.document_service import extract_text

text = extract_text("data/documents/test_cv.txt")

print("DOSYADAN ÇIKARILAN METİN")
print("-" * 40)
print(text)