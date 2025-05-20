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

# Inicializa o contador para a chave do uploader (para forçar reset)
if 'uploader_key_counter' not in st.session_state:
    st.session_state.uploader_key_counter = 0

# Inicializa estados dos widgets para permitir reset controlado
if 'search_terms_textarea' not in st.session_state:
    st.session_state.search_terms_textarea = ""
if 'case_sensitive_checkbox' not in st.session_state:
    st.session_state.case_sensitive_checkbox = False
if 'whole_word_checkbox' not in st.session_state:
    st.session_state.whole_word_checkbox = True
# Variável de estado para controlar se os resultados foram exibidos (para a mensagem inicial)
if 'results_displayed' not in st.session_state:
    st.session_state.results_displayed = False
# Variável de estado para controlar a exibição da área de texto para copiar
if 'show_copy_area' not in st.session_state:
    st.session_state.show_copy_area = False

# --- NOVAS VARIÁVEIS DE SESSÃO PARA ARMAZENAR OS RESULTADOS ---
if 'last_found_terms' not in st.session_state:
    st.session_state.last_found_terms = None
if 'last_snippets' not in st.session_state:
    st.session_state.last_snippets = None
if 'last_term_occurrences' not in st.session_state:
    st.session_state.last_term_occurrences = None
if 'last_total_words' not in st.session_state:
    st.session_state.last_total_words = None


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

search_terms_input = st.text_area(
    get_text("search_terms_input_label"),
    height=150,
    placeholder=get_text("search_terms_input_placeholder"),
    key="search_terms_textarea"
)

# --- NOVAS OPÇÕES DE BUSCA ---
st.subheader(get_text("search_options_header"))
col1, col2 = st.columns(2)
with col1:
    case_sensitive = st.checkbox(get_text("case_sensitive_checkbox"), key="case_sensitive_checkbox")
with col2:
    whole_word_only = st.checkbox(get_text("whole_word_checkbox"), key="whole_word_checkbox")

uploaded_file = st.file_uploader(get_text("file_uploader_label"), type="pdf", key=f"pdf_uploader_{st.session_state.uploader_key_counter}")


# --- BOTÃO LIMPAR TUDO ---
def clear_all_state():
    st.session_state.search_terms_textarea = ""
    st.session_state.case_sensitive_checkbox = False
    st.session_state.whole_word_checkbox = True
    st.session_state.uploader_key_counter += 1
    st.session_state.results_displayed = False
    st.session_state.show_copy_area = False
    # Limpa os resultados armazenados na sessão
    st.session_state.last_found_terms = None
    st.session_state.last_snippets = None
    st.session_state.last_term_occurrences = None
    st.session_state.last_total_words = None
    # Não precisa de st.rerun() aqui, a alteração dos valores de sessão já o faz

# Determina se o botão "Limpar Tudo" deve estar desabilitado
is_app_in_initial_state = (uploaded_file is None and
                           st.session_state.search_terms_textarea == "" and
                           not st.session_state.case_sensitive_checkbox and
                           st.session_state.whole_word_checkbox)

st.button(get_text("clear_button_label"), on_click=clear_all_state, disabled=is_app_in_initial_state)

# --- BOTÃO PROCESSAR BUSCA ---
search_terms_list = [term.strip() for term in st.session_state.search_terms_textarea.split('\n') if term.strip()]

process_button_disabled = not uploaded_file or not search_terms_list
process_button_clicked = st.button(get_text("process_button_label"), disabled=process_button_disabled)


# --- Lógica de Processamento ativada apenas pelo clique do botão ---
if process_button_clicked:
    st.session_state.show_copy_area = False # Esconde a área de cópia ao iniciar um novo processamento
    st.session_state.results_displayed = False # Reseta o flag de exibição de resultados para um novo processamento

    if not uploaded_file:
        st.warning(get_text("please_upload_file"))
    if not search_terms_list:
        st.warning(get_text("please_enter_terms"))

    if uploaded_file and search_terms_list:
        with st.spinner(get_text("processing_spinner")):
            full_text_combined, pages_data = extract_text_from_pdf(uploaded_file, MESSAGES[st.session_state.lang])

        if full_text_combined and pages_data:
            found_terms, snippets, term_occurrences, total_words = \
                find_matches_and_snippets(pages_data, search_terms_list, case_sensitive, whole_word_only)

            # --- ARMAZENA OS RESULTADOS NA SESSÃO ---
            st.session_state.last_found_terms = found_terms
            st.session_state.last_snippets = snippets
            st.session_state.last_term_occurrences = term_occurrences
            st.session_state.last_total_words = total_words
            st.session_state.results_displayed = True # Marca que resultados foram exibidos

# --- EXIBIÇÃO DOS RESULTADOS (agora baseada nos dados da sessão) ---
if st.session_state.results_displayed:
    # Recupera os resultados da sessão
    found_terms = st.session_state.last_found_terms
    snippets = st.session_state.last_snippets
    term_occurrences = st.session_state.last_term_occurrences
    total_words = st.session_state.last_total_words

    st.subheader(get_text("results_header"))

    if found_terms:
        # --- ESTATÍSTICAS DO DOCUMENTO ---
        st.subheader(get_text("stats_header"))
        st.write(f"{get_text('total_words_count')} **{total_words}**")

        st.write(get_text("term_occurrences"))
        for term, count in term_occurrences.items():
            st.write(f"- `{term}`: **{count}** ocorrência(s)")

        # --- RESULTADOS DA BUSCA E DOWNLOAD/COPIAR ---
        st.write(get_text("terms_found_header"))
        st.markdown(", ".join([f"`{term}`" for term in found_terms]))

        st.subheader(get_text("relevant_snippets_header"))
        if snippets:
            # Prepara o conteúdo para download/cópia
            download_content = ""
            download_content += f"{get_text('stats_header')}\n"
            download_content += f"{get_text('total_words_count')} {total_words}\n"
            download_content += f"{get_text('term_occurrences')}\n"
            for term, count in term_occurrences.items():
                download_content += f"- {term}: {count} ocorrência(s)\n"
            download_content += "\n" + "="*50 + "\n\n"
            download_content += f"{get_text('relevant_snippets_header')}\n\n"
            for item in snippets:
                download_content += f"Termo encontrado: {item['term']} ({get_text('page_number_label')} {item['page_num']})\n"
                download_content += f"Trecho: {item['original_text']}\n"
                download_content += "-"*20 + "\n\n"

            # Botões de Download e Copiar Lado a Lado
            col_dl, col_copy = st.columns(2)
            with col_dl:
                st.download_button(
                    label=get_text("download_results_button"),
                    data=download_content,
                    file_name=get_text("download_filename"),
                    mime="text/plain"
                )
            with col_copy:
                # O botão de copiar simplesmente define um estado para exibir a área de texto
                if st.button(get_text("copy_results_button")):
                    st.session_state.show_copy_area = True

            # Área de texto para copiar (exibida somente se o botão for clicado)
            if st.session_state.show_copy_area:
                st.info(get_text("copy_instructions"))
                st.text_area(
                    label="",
                    value=download_content,
                    height=300,
                    key="copy_text_area",
                    help="Selecione o texto e copie (Ctrl+C ou Cmd+C)"
                )

            # Exibe os trechos na interface
            unique_snippets_displayed = set()
            for item in snippets:
                snippet_text = item['snippet']
                if snippet_text not in unique_snippets_displayed:
                    st.markdown(f"**{get_text('terms_found_header').replace(':', '')}:** `{item['term']}` ({get_text('page_number_label')} {item['page_num']})")
                    st.markdown(f"...{item['snippet']}...", unsafe_allow_html=True)
                    st.markdown("---")
                    unique_snippets_displayed.add(snippet_text)
        else:
            st.info(get_text("no_snippets_found"))
    else:
        st.warning(get_text("no_terms_found"))
# Caso a extração do PDF falhe (full_text_combined é None), a mensagem de erro já foi exibida

# Mensagem inicial ou de orientação (exibida se nenhum resultado foi processado ainda)
if not st.session_state.results_displayed:
    st.info(get_text("initial_guidance"))
