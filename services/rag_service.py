from services.retrieval_service import retrieve_relevant_chunks
from services.foundry_service import generate_answer


def normalize_candidate_text(text: str) -> str:
    """
    CV içindeki birinci tekil şahıs ifadelerini
    üçüncü tekil şahıs anlatımına dönüştürür.
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
        normalized_text = normalized_text.replace(
            old,
            new,
        )

    return normalized_text


def clean_model_answer(answer: str) -> str:
    """
    Model cevabındaki gereksiz reasoning etiketlerini temizler.
    """

    if not answer:
        return ""

    answer = answer.replace("<think>", "")
    answer = answer.replace("</think>", "")

    return answer.strip()


def ask_document(
    question: str,
    source: str,
    top_k: int = 3,
) -> str:
    """
    Kullanıcının sorusuyla alakalı CV parçalarını yalnızca
    belirtilen kaynaktan bulur ve Phi-4 Mini'ye gönderir.
    """


    if not question.strip():
        return "Lütfen bir soru girin."
        
    if not source.strip():
        return "Önce bir CV veya belge yükleyin."
        









    # Sadece aktif CV içinde retrieval yap
    results = retrieve_relevant_chunks(
        question=question,
        source=source,
        top_k=top_k,
    )

    if not results:
        return (
            "Bu soruyu cevaplayabilecek "
            "yeterli bilgi CV'de bulunamadı."
        )

    context_parts = []

    for result in results:
        text = normalize_candidate_text(
            result["text"]
        )

        context_parts.append(text)

    context = "\n\n".join(context_parts)

    prompt = f"""
Sen SkillForge AI adlı bir CV analiz ve kariyer asistanısın.

Aşağıdaki CV bilgilerine dayanarak kullanıcının sorusunu cevapla.

CV BİLGİLERİ:
--------------------
{context}
--------------------

SORU:
{question}

KURALLAR:

- Yalnızca yukarıdaki CV bilgilerini temel al.
- CV'de olmayan teknoloji, deneyim, proje veya becerileri uydurma.
- CV'deki ifadeleri olduğundan daha güçlü gösterme.
- "Çalışıyor" bilgisini "uzmandır" şeklinde yorumlama.
- "Öğreniyor" bilgisini "ileri seviyededir" şeklinde yorumlama.
- Kullanıcının sorusunu tekrar etme.
- "CV'ye göre" veya "CV'de belirtilen bilgilere göre"
  gibi gereksiz giriş cümleleri kullanma.
- Yalnızca sorulan konu hakkında cevap ver.
- Adaydan üçüncü şahıs olarak bahset.
- Türkçe, doğal ve profesyonel cevap ver.
- Gereksiz tekrar yapma.
- Düşünme sürecini açıklama.
- Yalnızca nihai cevabı yaz.
- "uzmanlaşmıştır", "uzmandır", "ileri düzeydedir" gibi
  CV'nin açıkça desteklemediği seviye ifadeleri kullanma.
- Proje deneyimini iş deneyimi olarak sunma.
- Cevabı mümkünse 150 kelimenin altında tut.


EEğer kullanıcı uygun pozisyon soruyorsa:
- Adayın öğrenci olduğunu ve kariyerinin başlangıç aşamasında olduğunu dikkate al.
- En uygun tam 3 pozisyonu öner.
- Pozisyon adlarında "Uzman", "Senior", "Lead", "Manager",
  "Architect" veya benzeri kıdemli unvanları KESİNLİKLE kullanma.
- Pozisyon adlarını yalnızca "Stajyer", "Junior" veya
  "Entry-Level" seviyesinde oluştur.
- "Junior/Entry-Level", "Stajyer/Junior" gibi iki seviyeyi
  aynı pozisyon adında birlikte kullanma.
- En güçlü eşleşmeyi ilk sıraya koy.
- Her pozisyon için yalnızca 1 kısa gerekçe yaz.
- Gerekçeyi CV'de açıkça bulunan teknoloji, proje,
  eğitim veya becerilere dayandır.
- "Potansiyeline sahiptir", "uzmanlaşmıştır",
  "ileri seviyededir" gibi çıkarımsal ifadeler kullanma.
- Proje deneyimini profesyonel iş deneyimi gibi gösterme.
- Soruyla doğrudan ilgisi olmayan ayrıntıları ekleme.

Örnek çıktı biçimi:

1. Junior Web Developer
   Python, Django, HTML5, CSS3 ve Bootstrap ile yaptığı
   çalışmalar bu pozisyonu desteklemektedir.

2. Veri Analizi Stajyeri
   Python ve SQL kullanması ve veri analizi çalışmaları
   bu pozisyonla uyumludur.

3. Siber Güvenlik Stajyeri
   Siber güvenlik eğitimleri ve bu alandaki çalışmaları
   bu pozisyonu desteklemektedir.

Örnekteki bilgileri kopyalama.
Gerçek cevapta yalnızca verilen CV bilgilerini kullan.
CEVAP:
"""

    answer = generate_answer(prompt)

    answer = clean_model_answer(answer)

    if not answer:
        return "Model geçerli bir cevap üretemedi."

    return answer