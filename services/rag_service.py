from services.retrieval_service import retrieve_relevant_chunks
from services.foundry_service import generate_answer


def normalize_candidate_text(text: str) -> str:
    """
    CV içindeki birinci tekil şahıs ifadelerini
    aday anlatımına uygun üçüncü tekil şahıs diline çevirir.
    """

    replacements = {
        "kendimi": "kendisini",
        "çalışıyorum": "çalışmaktadır",
        "geliştiriyorum": "geliştirmektedir",
        "hedefliyorum": "hedeflemektedir",
        "biliyorum": "bilmektedir",
        "yapıyorum": "yapmaktadır",
        "öğreniyorum": "öğrenmektedir",
        "kullanıyorum": "kullanmaktadır",
        "ilgileniyorum": "ilgilenmektedir",
    }

    normalized_text = text

    for old, new in replacements.items():
        normalized_text = normalized_text.replace(old, new)

    return normalized_text


def clean_model_answer(answer: str) -> str:
    """
    Model cevabındaki gereksiz think etiketlerini temizler.
    """

    answer = answer.replace("<think>", "")
    answer = answer.replace("</think>", "")

    return answer.strip()


def ask_document(
    question: str,
    top_k: int = 3,
) -> str:
    """
    Kullanıcının sorusuyla en alakalı belge parçalarını bulur,
    bunları context olarak Foundry Local modeline gönderir
    ve kaynaklara dayalı cevap üretir.
    """

    if not question.strip():
        return "Lütfen bir soru girin."

    results = retrieve_relevant_chunks(
        question=question,
        top_k=top_k,
    )

    if not results:
        return "Bu soruya cevap verebilmek için ilgili belge bulunamadı."

    context_parts = []

    for result in results:
        normalized_text = normalize_candidate_text(
            result["text"]
        )

        context_parts.append(
            f"Kaynak: {result['source']}\n"
            f"Metin: {normalized_text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
Sen SkillForge AI isimli bir CV analiz ve kariyer asistanısın.

Aşağıdaki KAYNAKLAR, kullanıcının yüklediği CV veya belgelerden
alınmış metin parçalarıdır.

KAYNAKLAR:
--------------------
{context}
--------------------

KULLANICI SORUSU:
{question}

KESİN KURALLAR:

1. Cevabını yalnızca yukarıdaki KAYNAKLAR bölümünde bulunan
   bilgilere dayanarak oluştur.

2. Kaynaklarda olmayan hiçbir teknoloji, beceri, deneyim,
   eğitim veya kişisel bilgi ekleme.

3. Kaynaklarda soruyu cevaplayabilecek en az bir bilgi varsa
   doğrudan cevabı ver.

4. Soruyu cevaplayabilecek hiçbir bilgi kaynaklarda yoksa
   yalnızca:
   "Bu bilgi belgede bulunmuyor."
   şeklinde cevap ver.

5. Kaynaklarda bilgi bulunduğu durumda
   "Bu bilgi belgede bulunmuyor."
   ifadesini kesinlikle kullanma.

6. Adaydan her zaman üçüncü tekil şahıs olarak bahset.

7. "Ben", "kendimi", "çalışıyorum", "biliyorum",
   "hedefliyorum" gibi birinci tekil şahıs ifadeleri kullanma.

8. Kaynak metinde birinci tekil şahıs kullanılmış olsa bile
   cevabı aday diliyle yeniden yaz.

9. Türkçe cevap ver.

10. Kısa, doğal, açık ve doğrudan cevap ver.

11. Gereksiz tekrar yapma.

12. Gereksiz kapanış cümlesi ekleme.

13. "Bu bilgiler belgede yer almaktadır",
    "Kaynaklara göre",
    "Belgedeki bilgilere göre"
    gibi gereksiz açıklamalar ekleme.

14. Sadece kullanıcının sorusunu cevapla.

15. Kullanıcının sorduğu bilgi türünün dışına çıkma.
    Örneğin kullanıcı yalnızca teknolojileri soruyorsa,
    kariyer hedefleri veya ilgi alanları hakkında ek bilgi verme.

CEVAP:
"""

    answer = generate_answer(prompt)

    return clean_model_answer(answer)