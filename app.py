import os
import tempfile

import streamlit as st

from services.document_service import extract_text
from services.indexing_service import index_document
from services.rag_service import ask_document


st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🤖",
    layout="wide",
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""

if "cv_source" not in st.session_state:
    st.session_state.cv_source = ""

if "cv_indexed" not in st.session_state:
    st.session_state.cv_indexed = False


# -------------------------------------------------
# ANA BAŞLIK
# -------------------------------------------------

st.title("🤖 SkillForge AI")

st.caption(
    "Yerel yapay zekâ destekli kariyer ve öğrenme asistanı"
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("Menü")

page = st.sidebar.radio(
    "Bölüm seç",
    [
        "Ana Sayfa",
        "CV Analizi",
        "Öğrenme Planı",
        "Mülakat",
    ],
)


# -------------------------------------------------
# ANA SAYFA
# -------------------------------------------------

if page == "Ana Sayfa":

    st.header(
        "Kariyer yolculuğunu yapay zekâ ile planla"
    )

    st.write(
        "SkillForge AI; CV analizi, kişiselleştirilmiş "
        "öğrenme planı ve teknik mülakat desteği "
        "sunmak için geliştirilmektedir."
    )

    st.markdown(
        """
        ### SkillForge AI ile neler yapabilirsin?

        - CV veya belge yükleyebilirsin.
        - CV'ndeki becerileri analiz edebilirsin.
        - CV hakkında sorular sorabilirsin.
        - Kariyer hedeflerine yönelik öğrenme planı oluşturabilirsin.
        - Teknik mülakatlara hazırlanabilirsin.
        """
    )


# -------------------------------------------------
# CV ANALİZİ
# -------------------------------------------------

elif page == "CV Analizi":

    st.header("📄 CV Analizi")

    uploaded_file = st.file_uploader(
        "CV veya belge yükle",
        type=["pdf", "txt"],
    )

    if uploaded_file is not None:

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        try:

            # CV metnini çıkar
            text = extract_text(temp_path)

            st.session_state.cv_text = text
            st.session_state.cv_source = uploaded_file.name

            st.success(
                "Dosya başarıyla okundu."
            )

            # -------------------------------------
            # METİN ÖNİZLEME
            # -------------------------------------

            st.subheader("Metin Önizleme")

            st.text_area(
                "Çıkarılan metin",
                value=text[:5000],
                height=300,
            )

            # -------------------------------------
            # CV'Yİ RAG İÇİN İNDEKSLE
            # -------------------------------------

            if st.button(
                "CV'yi Yapay Zekâ Analizine Hazırla"
            ):

                with st.spinner(
                    "CV analiz için hazırlanıyor..."
                ):

                    chunk_count = index_document(
                        source=uploaded_file.name,
                        text=text,
                    )

                    st.session_state.cv_indexed = True

                st.success(
                    f"CV başarıyla hazırlandı. "
                    f"{chunk_count} metin parçası oluşturuldu."
                )

        except Exception as error:

            st.error(
                f"Dosya okunamadı: {error}"
            )

        finally:

            if os.path.exists(temp_path):
                os.remove(temp_path)


    # -------------------------------------------------
    # RAG SORU - CEVAP
    # -------------------------------------------------

    if st.session_state.cv_indexed:

        st.divider()

        st.subheader(
            "💬 CV Hakkında Yapay Zekâya Sor"
        )

        question = st.text_input(
            "CV hakkında bir soru yaz",
            placeholder=(
                "Örneğin: Bu aday hangi "
                "teknolojilerle çalışıyor?"
            ),
        )

        if st.button("Sor"):

            if not question.strip():

                st.warning(
                    "Lütfen bir soru yaz."
                )

            else:

                with st.spinner(
                    "SkillForge AI düşünüyor..."
                ):

                    try:

                        answer = ask_document(
                            question=question,
                            source=st.session_state.cv_source,
                        )

                        st.subheader(
                            "SkillForge AI Cevabı"
                        )

                        st.write(answer)

                    except Exception as error:

                        st.error(
                            "Yapay zekâ cevabı "
                            "oluşturulurken hata oluştu."
                        )

                        st.code(str(error))


# -------------------------------------------------
# ÖĞRENME PLANI
# -------------------------------------------------

elif page == "Öğrenme Planı":

    st.header("📚 Öğrenme Planı")

    st.info(
        "Bu bölüm geliştirme aşamasındadır."
    )


# -------------------------------------------------
# MÜLAKAT
# -------------------------------------------------

elif page == "Mülakat":

    st.header("🎯 Teknik Mülakat")

    st.info(
        "Bu bölüm geliştirme aşamasındadır."
    )