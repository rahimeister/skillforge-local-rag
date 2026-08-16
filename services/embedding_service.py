from openai import OpenAI

BASE_URL = "http://127.0.0.1:61652/v1"
EMBEDDING_MODEL = "qwen3-embedding-0.6b-generic-cpu"


def get_embedding(text: str) -> list[float]:
    """
    Verilen metni embedding (sayısal vektör) haline dönüştürür.
    """

    client = OpenAI(
        base_url=BASE_URL,
        api_key="local",
    )

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding