from services.retrieval_service import retrieve_relevant_chunks
from services.foundry_service import generate_answer


def create_learning_plan(
    source: str,
    target_role: str,
    current_level: str,
    weekly_hours: int,
    duration_weeks: int,
    top_k: int = 5,
) -> str:
    """
    Kullanıcının CV bilgilerine ve hedef pozisyonuna göre
    kişiselleştirilmiş öğrenme planı oluşturur.
    """

    if not source.strip():
        return "Önce bir CV veya belge yükleyin."

    if not target_role.strip():
        return "Lütfen hedef pozisyonu girin."

    # Hedef pozisyonla ilgili CV parçalarını getir
    retrieval_question = (
        f"Bu adayın {target_role} pozisyonuyla ilgili "
        "becerileri, teknolojileri, projeleri ve deneyimleri nelerdir?"
    )

    results = retrieve_relevant_chunks(
        question=retrieval_question,
        source=source,
        top_k=top_k,
    )

    if not results:
        cv_context = (
            "CV'den hedef pozisyonla doğrudan ilişkili "
            "yeterli bilgi bulunamadı."
        )
    else:
        context_parts = []

        for result in results:
            context_parts.append(result["text"])

        cv_context = "\n\n".join(context_parts)

    prompt = f"""
Sen SkillForge AI adlı bir kariyer ve öğrenme planı asistanısın.

Kullanıcının CV bilgilerini ve kariyer hedefini kullanarak
kişiselleştirilmiş bir öğrenme planı oluştur.

CV BİLGİLERİ:
--------------------
{cv_context}
--------------------

HEDEF POZİSYON:
{target_role}

MEVCUT SEVİYE:
{current_level}

HAFTALIK AYRILABİLECEK SÜRE:
{weekly_hours} saat

PLAN SÜRESİ:
{duration_weeks} hafta

KURALLAR:

- CV'de açıkça bulunan becerileri "mevcut beceriler" olarak değerlendir.
- CV'de bulunmayan fakat hedef pozisyon için gerekli konuları
  öğrenme önerisi olarak sunabilirsin.
- CV'de bulunmayan bir beceriyi aday zaten biliyormuş gibi gösterme.
- Kullanıcının seviyesine uygun öneriler yap.
- Haftalık çalışma süresini dikkate al.
- Planı {duration_weeks} haftaya uygun şekilde oluştur.
- Gereksiz tekrar yapma.
- Gerçekçi ve uygulanabilir görevler öner.
- Çok genel tavsiyeler yerine somut konular öner.
- Türkçe yaz.
- Profesyonel ama anlaşılır bir dil kullan.

CEVAP YAPISI:

1. Mevcut Güçlü Yönler
CV'de hedef pozisyonla ilgili görülen mevcut becerileri kısaca yaz.

2. Geliştirilmesi Gereken Alanlar
Hedef pozisyona ulaşmak için öğrenilmesi veya geliştirilmesi gereken
önemli konuları yaz.

3. {duration_weeks} Haftalık Öğrenme Yol Haritası
Her hafta için:
- Öğrenilecek konu
- Yapılacak uygulama
- Yaklaşık çalışma süresi

4. Proje Önerileri
Hedef pozisyonla ilgili 2 küçük veya orta ölçekli proje öner.

5. Plan Sonunda Beklenen Kazanımlar
Plan tamamlandığında kullanıcının hangi alanlarda gelişmiş
olacağını kısa şekilde açıkla.

Yalnızca nihai öğrenme planını yaz.
"""

    answer = generate_answer(prompt)

    if not answer:
        return "Öğrenme planı oluşturulamadı."

    return answer.strip()