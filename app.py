import os
import tempfile

import streamlit as st
from openai import OpenAI

from services.document_service import extract_text
client = OpenAI(
    base_url="http://127.0.0.1:9120/v1",
    api_key="not-needed",
)
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "cv_ready" not in st.session_state:
    st.session_state.cv_ready = False

st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 SkillForge AI")
st.caption("Yerel yapay zekâ destekli kariyer ve öğrenme asistanı")

st.sidebar.title("Menü")

page = st.sidebar.radio(
    "Bölüm seç",
    ["Ana Sayfa", "CV Analizi", "Öğrenme Planı", "Mülakat"],
)


if page == "Ana Sayfa":
    st.header("Kariyer yolculuğunu yapay zekâ ile planla")

    st.write(
        "SkillForge AI ile CV'ni analiz et, kişisel öğrenme planını oluştur "
        "ve mülakat pratiği yap."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("CV Analizi")
        st.write("CV'ni yükle, becerilerini ve gelişim alanlarını keşfet.")

    with col2:
        st.subheader("Öğrenme Planı")
        st.write("Hedef pozisyonuna göre öğrenme yol haritanı oluştur.")

    with col3:
        st.subheader("Mülakat")
        st.write("Teknik ve İK mülakatlarına hazırlan.")


elif page == "CV Analizi":
    st.header("CV Analizi")

    uploaded_file = st.file_uploader(
        "CV veya belge yükle",
        type=["pdf", "txt"],
    )

    if uploaded_file is not None:
        st.write(f"**Yüklenen dosya:** {uploaded_file.name}")

        if st.button("CV'yi Yapay Zekâ Analizine Hazırla", type="primary"):
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.cv_ready = True

            st.success("CV yapay zekâ analizine hazırlandı.")

    if st.session_state.cv_ready:

        if st.button("Yeni CV Yükle / Analizi Temizle"):
            st.session_state.uploaded_file_name = None
            st.session_state.cv_ready = False
            st.rerun()

        if uploaded_file is not None:

            suffix = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_path = temp_file.name

            try:
                text = extract_text(temp_path)

                st.success("Dosya başarıyla okundu.")

                st.subheader("Metin Önizleme")

                st.text_area(
                    "Çıkarılan metin",
                    value=text,
                    height=400,
                )

                st.subheader("🤖 Yapay Zekâ CV Analizi")

                if st.button("CV'yi Analiz Et", type="primary"):

                    with st.spinner("Qwen3-4B CV'ni analiz ediyor..."):

                        response = client.chat.completions.create(
                            model="qwen3-4b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Sen bir kariyer ve CV analiz asistanısın. "
                                        "CV'yi Türkçe analiz et. "
                                        "Adayın güçlü yönlerini, teknik becerilerini, "
                                        "eksiklerini ve geliştirme önerilerini belirt."
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": f"""
Aşağıdaki CV'yi analiz et:

{text}

Şu başlıklarla cevap ver:

1. Güçlü Yönler
2. Teknik Beceriler
3. Eksik veya Geliştirilmesi Gereken Alanlar
4. Kariyer Önerileri
5. Genel Değerlendirme
""",
                                },
                            ],
                            temperature=0.2,
                        )

                        analysis = response.choices[0].message.content

                        st.markdown("### 📊 Analiz Sonucu")
                        st.write(analysis)

                st.subheader("📄 Belge Bilgisi")
                st.write(f"Dosya adı: **{uploaded_file.name}**")
                st.write(f"Karakter sayısı: **{len(text)}**")

                st.subheader("🔍 İlk Değerlendirme")

                if len(text) > 1000:
                    st.success("CV yeterli miktarda metin içeriyor.")
                else:
                    st.warning("CV'deki metin oldukça kısa görünüyor.")

            except Exception as error:
                st.error(f"Dosya okunamadı: {error}")

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)


elif page == "Öğrenme Planı":
    st.header("Öğrenme Planı")
    st.write("Kariyer hedeflerine uygun kişiselleştirilmiş bir öğrenme planı oluştur.")

    target_position = st.text_input(
        "Hedef pozisyon",
        placeholder="Örn: Backend Developer"
    )

    current_level = st.selectbox(
        "Mevcut seviyen",
        ["Başlangıç", "Orta", "İleri"]
    )

    weekly_hours = st.selectbox(
        "Haftalık ayırabileceğin süre",
        ["3 saat", "5 saat", "7 saat", "10+ saat"]
    )

    plan_duration = st.selectbox(
        "Plan süresi",
        ["4 hafta", "8 hafta", "12 hafta"]
    )

    if st.button("Öğrenme Planı Oluştur", type="primary"):
        if not target_position.strip():
            st.warning("Lütfen hedef pozisyonunu gir.")
        else:
            st.success("Bilgiler alındı.")
            st.info("Öğrenme planı servisi bağlanacak.")

            st.subheader("Güçlü Yönler")
            st.info("Backend servisi bağlandığında burada gösterilecek.")

            st.subheader("Eksikler")
            st.info("Backend servisi bağlandığında burada gösterilecek.")

            st.subheader("Yol Haritası")
            st.info("Backend servisi bağlandığında burada gösterilecek.")

            st.subheader("Önerilen Projeler")
            st.info("Backend servisi bağlandığında burada gösterilecek.")


elif page == "Mülakat":
    st.header("Mülakat")
    st.write("Kariyer hedeflerine uygun bir mülakat simülasyonu başlat.")

    position = st.text_input(
        "Pozisyon",
        placeholder="Örn: Python Developer"
    )

    interview_type = st.selectbox(
        "Mülakat türü",
        ["Teknik", "İK", "Karma"]
    )

    difficulty = st.selectbox(
        "Zorluk seviyesi",
        ["Başlangıç", "Orta", "İleri"]
    )

    question_count = st.selectbox(
        "Soru sayısı",
        [5, 10, 15]
    )

    if st.button("Mülakatı Başlat", type="primary"):
        if not position.strip():
            st.warning("Lütfen pozisyon gir.")
        else:
            st.success("Mülakat bilgileri hazırlandı.")

            st.subheader("Soru")

            st.info(
                "Mülakat servisi bağlandığında soru burada gösterilecek."
            )

            answer = st.text_area(
                "Cevabınız",
                placeholder="Cevabınızı buraya yazın...",
                height=150,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.button("Sonraki Soru")

            with col2:
                st.button("Bitir")

            st.divider()

            st.subheader("Değerlendirme Sonucu")

            st.write("**Güçlü Yanlar**")
            st.info("Değerlendirme servisi bağlandığında burada gösterilecek.")

            st.write("**Geliştirilecek Noktalar**")
            st.info("Değerlendirme servisi bağlandığında burada gösterilecek.")

            st.write("**Örnek Daha İyi Cevap**")
            st.info("Değerlendirme servisi bağlandığında burada gösterilecek.")