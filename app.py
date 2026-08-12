import os
import tempfile

import streamlit as st

from services.document_service import extract_text


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
        "SkillForge AI; CV analizi, kişiselleştirilmiş öğrenme planı "
        "ve teknik mülakat desteği sunmak için geliştirilmektedir."
    )


elif page == "CV Analizi":
    st.header("CV Analizi")

    uploaded_file = st.file_uploader(
        "CV veya belge yükle",
        type=["pdf", "txt"],
    )

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
                value=text[:5000],
                height=350,
            )

            st.info(
                "CV'nin yapay zekâ ile analiz edilmesi sonraki aşamada "
                "Foundry Local servisine bağlanacaktır."
            )

        except Exception as error:
            st.error(f"Dosya okunamadı: {error}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


elif page == "Öğrenme Planı":
    st.header("Öğrenme Planı")
    st.info("Bu bölüm geliştirme aşamasındadır.")


elif page == "Mülakat":
    st.header("Teknik Mülakat")
    st.info("Bu bölüm geliştirme aşamasındadır.")
    