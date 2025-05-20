import streamlit as st

def initialize_session_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    if 'uploader_key_counter' not in st.session_state:
        st.session_state.uploader_key_counter = 0
    if 'search_terms_textarea' not in st.session_state:
        st.session_state.search_terms_textarea = ""
    if 'case_sensitive_checkbox' not in st.session_state:
        st.session_state.case_sensitive_checkbox = False
    if 'whole_word_checkbox' not in st.session_state:
        st.session_state.whole_word_checkbox = True
    if 'enable_regex_checkbox' not in st.session_state:
        st.session_state.enable_regex_checkbox = False
    if 'enable_ocr_fallback_checkbox' not in st.session_state:
        st.session_state.enable_ocr_fallback_checkbox = False
    if 'results_displayed' not in st.session_state:
        st.session_state.results_displayed = False
    if 'show_copy_area' not in st.session_state:
        st.session_state.show_copy_area = False
    if 'last_processed_results' not in st.session_state:
        st.session_state.last_processed_results = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

def clear_all_state():
    """Limpa todas as variáveis de estado relacionadas à busca e resultados."""
    st.session_state.search_terms_textarea = ""
    st.session_state.case_sensitive_checkbox = False
    st.session_state.whole_word_checkbox = True
    st.session_state.enable_regex_checkbox = False
    st.session_state.enable_ocr_fallback_checkbox = False
    st.session_state.uploader_key_counter += 1
    st.session_state.results_displayed = False
    st.session_state.show_copy_area = False
    st.session_state.last_processed_results = None
    st.session_state.current_page = 1 # Resetar paginação
