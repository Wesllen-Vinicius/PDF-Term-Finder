# app.py

import streamlit as st
import io
import re

# Importa as funções e configurações dos outros módulos
from pdf_processor import extract_text_from_pdf, find_matches_and_snippets
from config import APP_NAME, MESSAGES, SUPPORTED_LANGUAGES

# --- Configuração da Página (DEVE SER O PRIMEIRO COMANDO STREAMLIT) ---
initial_lang_for_page_title = st.session_state.get('lang', 'pt')
st.set_page_config(
    layout="wide",
    page_title=APP_NAME[initial_lang_for_page_title]
)

# --- Inicialização e Seleção de Idioma ---

if 'lang' not in st.session_state:
    st.session_state.lang = "pt"

def on_language_change():
    st.session_state.lang = st.session_state.lang_selector

current_lang_options = list(SUPPORTED_LANGUAGES.keys())
current_lang_index = current_lang_options.index(st.session_state.lang)

st.sidebar.radio(
    MESSAGES[st.session_state.lang]['select_language'],
    options=current_lang_options,
    index=current_lang_index,
    format_func=lambda x: SUPPORTED_LANGUAGES[x],
    key="lang_selector",
    on_change=on_language_change
)

def get_text(key):
    return MESSAGES[st.session_state.lang][key]

# --- Interface do Aplicativo ---
st.title(APP_NAME[st.session_state.lang])

st.markdown(get_text("upload_instructions"))

# --- VOLTANDO AO st.text_area PARA TERMOS DE BUSCA (UM POR LINHA) ---
search_terms_input = st.text_area(
    get_text("search_terms_input_label"),
    height=150,
    placeholder=get_text("search_terms_input_placeholder"),
    key="search_terms_textarea"
)

uploaded_file = st.file_uploader(get_text("file_uploader_label"), type="pdf", key="pdf_uploader")

# --- VOLTANDO À PARSEAR POR QUEBRA DE LINHA ---
search_terms_list = [term.strip() for term in search_terms_input.split('\n') if term.strip()]

if uploaded_file and search_terms_list:
    with st.spinner(get_text("processing_spinner")):
        full_text = extract_text_from_pdf(uploaded_file, MESSAGES[st.session_state.lang])

    if full_text:
        found_terms, snippets = find_matches_and_snippets(full_text, search_terms_list)

        st.subheader(get_text("results_header"))

        if found_terms:
            st.write(get_text("terms_found_header"))
            st.markdown(", ".join([f"`{term}`" for term in found_terms]))

            st.subheader(get_text("relevant_snippets_header"))
            if snippets:
                unique_snippets_displayed = set()
                for item in snippets:
                    snippet_text = item['snippet']
                    if snippet_text not in unique_snippets_displayed:
                        st.markdown(f"**{get_text('terms_found_header').replace(':', '')}:** `{item['term']}`")
                        st.markdown(f"...{item['snippet']}...", unsafe_allow_html=True)
                        st.markdown("---")
                        unique_snippets_displayed.add(snippet_text)
            else:
                st.info(get_text("no_snippets_found"))
        else:
            st.warning(get_text("no_terms_found"))

elif uploaded_file and not search_terms_list:
    st.info(get_text("please_enter_terms"))
elif not uploaded_file and search_terms_list:
    st.info(get_text("please_upload_file"))
elif not uploaded_file and not search_terms_list:
    st.info(get_text("please_upload_file") + " " + get_text("please_enter_terms"))
