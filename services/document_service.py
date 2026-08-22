from pathlib import Path
from pypdf import PdfReader


def extract_text_from_txt(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    return path.read_text(encoding="utf-8")


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    reader = PdfReader(str(path))

    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_text(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    if suffix == ".txt":
        return extract_text_from_txt(file_path)

    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError("Yalnızca .txt ve .pdf dosyaları destekleniyor.")


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[str]:
    """
    Uzun bir metni küçük parçalara böler.
    """

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap, chunk_size değerinden küçük olmalıdır."
        )

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