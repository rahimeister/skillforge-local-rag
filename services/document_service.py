def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[str]:
    """
    Uzun bir metni küçük parçalara (chunk) böler.

    chunk_size:
        Her parçanın yaklaşık karakter uzunluğu.

    overlap:
        Ardışık parçaların bir miktar ortak metin
        içermesini sağlar.
    """

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap, chunk_size değerinden küçük olmalıdır."
        )

    # Fazla boşlukları ve satır sonlarını temizle
    cleaned_text = " ".join(text.split())

    chunks = []

    start = 0

    while start < len(cleaned_text):

        end = start + chunk_size

        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks