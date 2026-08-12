from pathlib import Path
from pypdf import PdfReader


def extract_text_from_txt(file_path: str) -> str:
    """TXT dosyasındaki metni UTF-8 olarak okur."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    return path.read_text(encoding="utf-8")


def extract_text_from_pdf(file_path: str) -> str:
    """PDF dosyasındaki yazıları çıkarır."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    reader = PdfReader(str(path))
    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n".join(pages)


def extract_text(file_path: str) -> str:
    """Dosya uzantısına göre uygun okuma fonksiyonunu çalıştırır."""
    suffix = Path(file_path).suffix.lower()

    if suffix == ".txt":
        return extract_text_from_txt(file_path)

    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError("Yalnızca .txt ve .pdf dosyaları destekleniyor.")
