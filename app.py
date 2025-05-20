import streamlit as st
import io
import re
from collections import Counter

# Importa as funções e configurações dos outros módulos
from pdf_processor import extract_text_from_pdf, find_matches_and_snippets
from config import APP_NAME, MESSAGES, SUPPORTED_LANGUAGES
from session_state_manager import initialize_session_state, clear_all_state # Novo

# --- Configuração da Página (DEVE SER O PRIMEIRO COMANDO STREAMLIT) ---
st.set_page_config(
    layout="wide",
    page_title=APP_NAME['pt'],
    page_icon=MESSAGES['pt']['favicon_icon']
)

# --- Inicialização e Seleção de Idioma ---
initialize_session_state() # Chama a função do novo módulo

# --- FUNÇÃO AUXILIAR get_text ---
def get_text(key):
    return MESSAGES[st.session_state.lang][key]

# --- SEÇÃO SOBRE / AJUDA NA BARRA LATERAL ---
with st.sidebar.expander(get_text("about_header")):
    st.markdown(get_text("about_content_1"))
    st.markdown(get_text("about_content_2"))
    st.markdown(get_text("about_limitations"))

# --- SELEÇÃO DE IDIOMA ---
current_lang_options = list(SUPPORTED_LANGUAGES.keys())
current_lang_index = current_lang_options.index(st.session_state.lang)

st.sidebar.radio(
    get_text("select_language"),
    options=current_lang_options,
    index=current_lang_index,
    format_func=lambda x: SUPPORTED_LANGUAGES[x],
    key="lang_selector",
    on_change=lambda: st.session_state.update(lang=st.session_state.lang_selector)
)

# --- Interface do Aplicativo ---
st.title(APP_NAME[st.session_state.lang])

st.markdown(get_text("upload_instructions"))

st.divider()

# --- SEÇÃO DE INPUTS EM COLUNAS ---
input_col_terms, input_col_uploader = st.columns([2, 1])

with input_col_terms:
    search_terms_input = st.text_area(
        get_text("search_terms_input_label"),
        height=150,
        placeholder=get_text("search_terms_input_placeholder"),
        key="search_terms_textarea"
    )

with input_col_uploader:
    st.markdown("<br><br>", unsafe_allow_html=True)
    uploaded_files_list = st.file_uploader(get_text("file_uploader_label"), type="pdf", accept_multiple_files=True, key=f"pdf_uploader_{st.session_state.uploader_key_counter}")

# --- OPÇÕES DE BUSCA DENTRO DE UM EXPANDER ---
with st.expander(get_text("search_options_header")):
    col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4) # Mais uma coluna
    with col_opt1:
        case_sensitive = st.checkbox(get_text("case_sensitive_checkbox"), key="case_sensitive_checkbox")
    with col_opt2:
        whole_word_only = st.checkbox(get_text("whole_word_checkbox"), key="whole_word_checkbox")
    with col_opt3:
        enable_regex = st.checkbox(get_text("enable_regex_checkbox"), key="enable_regex_checkbox", help=get_text("regex_help_text"))
    with col_opt4:
        enable_ocr_fallback = st.checkbox(get_text("enable_ocr_fallback_checkbox"), key="enable_ocr_fallback_checkbox", help=get_text("ocr_help_text")) # Nova opção

st.divider()

# Determina se o botão "Limpar Tudo" deve estar desabilitado
is_app_in_initial_state = ( (uploaded_files_list is None or len(uploaded_files_list) == 0) and
                           st.session_state.search_terms_textarea == "" and
                           not st.session_state.case_sensitive_checkbox and
                           st.session_state.whole_word_checkbox and
                           not st.session_state.enable_regex_checkbox and
                           not st.session_state.enable_ocr_fallback_checkbox ) # Adicionado novo checkbox

st.button(get_text("clear_button_label"), on_click=clear_all_state, disabled=is_app_in_initial_state)

# --- BOTÃO PROCESSAR BUSCA ---
search_terms_list = [term.strip() for term in st.session_state.search_terms_textarea.split('\n') if term.strip()]

process_button_disabled = (uploaded_files_list is None or len(uploaded_files_list) == 0) or not search_terms_list
process_button_clicked = st.button(get_text("process_button_label"), disabled=process_button_disabled, on_click=lambda: st.session_state.update({"_process_clicked": True}), icon=get_text("process_button_icon"))

# --- Lógica de Processamento ativada apenas pelo clique do botão ---
if st.session_state.get("_process_clicked", False):
    st.session_state["_process_clicked"] = False

    st.session_state.show_copy_area = False
    st.session_state.results_displayed = False
    st.session_state.last_processed_results = None
    st.session_state.current_page = 1 # Resetar página ao processar nova busca

    if (uploaded_files_list is None or len(uploaded_files_list) == 0):
        st.warning(get_text("please_upload_file"))
    if not search_terms_list:
        st.warning(get_text("please_enter_terms"))

    if uploaded_files_list and search_terms_list:
        all_found_terms = set()
        all_snippets = []
        overall_term_occurrences = Counter()
        overall_total_words = 0

        with st.spinner(get_text("processing_spinner")):
            for uploaded_file in uploaded_files_list:
                progress_text = st.empty() # Placeholder para o texto de progresso

                def update_progress(current, total, file):
                    progress_text.text(f"{get_text('processing_file')} '{file}': {get_text('page_progress').format(current=current, total=total)}")

                st.info(f"{get_text('processing_file')} '{uploaded_file.name}'...")
                full_text_combined, pages_data, file_name = extract_text_from_pdf(uploaded_file, MESSAGES[st.session_state.lang], enable_ocr_fallback, update_progress)
                progress_text.empty() # Limpa o texto de progresso após o processamento do arquivo

                if full_text_combined and pages_data:
                    found_terms_file, snippets_file, term_occurrences_file, total_words_file = \
                        find_matches_and_snippets(pages_data, search_terms_list, case_sensitive, whole_word_only, file_name, enable_regex)

                    all_found_terms.update(found_terms_file)
                    all_snippets.extend(snippets_file)
                    overall_term_occurrences.update(term_occurrences_file)
                    overall_total_words += total_words_file

        st.session_state.last_processed_results = {
            "found_terms": list(all_found_terms),
            "snippets": all_snippets,
            "term_occurrences": dict(overall_term_occurrences),
            "total_words": overall_total_words
        }
        st.session_state.results_displayed = True


# --- EXIBIÇÃO DOS RESULTADOS (agora baseada nos dados da sessão e agrupados por arquivo) ---
if st.session_state.results_displayed and st.session_state.last_processed_results:
    found_terms = st.session_state.last_processed_results["found_terms"]
    snippets = st.session_state.last_processed_results["snippets"]
    term_occurrences = st.session_state.last_processed_results["term_occurrences"]
    total_words = st.session_state.last_processed_results["total_words"]

    st.subheader(get_text("results_header"))

    if found_terms:
        # --- ESTATÍSTICAS DO DOCUMENTO ---
        st.subheader(get_text("stats_header"))
        st.write(f"{get_text('total_words_count')} **{total_words}**")

        st.write(get_text("term_occurrences"))
        for term, count in term_occurrences.items():
            st.write(f"- `{term}`: **{count}** ocorrência(s)")

        # --- OPÇÕES DE FILTRAGEM E ORDENAÇÃO DE TRECHOS ---
        st.subheader(get_text("relevant_snippets_header"))

        filter_col, sort_col = st.columns(2)
        with filter_col:
            filter_options = [get_text("all_terms_filter")] + sorted(found_terms)
            selected_filter_term = st.selectbox(
                get_text("filter_snippets_label"),
                options=filter_options,
                key="snippet_filter"
            )

        with sort_col:
            sort_options = {
                get_text("sort_option_page"): "page",
                get_text("sort_option_file_page"): "file_page"
            }
            selected_sort_option_label = st.selectbox(
                get_text("sort_snippets_label"),
                options=list(sort_options.keys()),
                key="snippet_sort_option"
            )
            selected_sort_option_key = sort_options[selected_sort_option_label]

        # Aplica filtro e ordenação GLOBALMENTE
        filtered_snippets = snippets
        if selected_filter_term != get_text("all_terms_filter"):
            filtered_snippets = [s for s in snippets if s['term'] == selected_filter_term]

        if selected_sort_option_key == "page":
            filtered_snippets.sort(key=lambda x: (x['page_num'], x['file_name']))
        elif selected_sort_option_key == "file_page":
            filtered_snippets.sort(key=lambda x: (x['file_name'], x['page_num']))


        if filtered_snippets:
            # Prepara o conteúdo para download/cópia (usando os snippets originais, não filtrados/ordenados na UI)
            download_content = ""
            download_content += f"{get_text('stats_header')}\n"
            download_content += f"{get_text('total_words_count')} {total_words}\n"
            download_content += f"{get_text('term_occurrences')}\n"
            for term, count in term_occurrences.items():
                download_content += f"- {term}: {count} ocorrência(s)\n"
            download_content += "\n" + "="*50 + "\n\n"
            download_content += f"{get_text('relevant_snippets_header')}\n\n"

            snippets_for_download = sorted(snippets, key=lambda x: (x['file_name'], x['page_num']))

            for item in snippets_for_download:
                download_content += f"Termo encontrado: {item['term']} ({get_text('page_number_label')} {item['page_num']}) [{get_text('results_from_file')} {item['file_name']}]\n"
                download_content += f"Trecho: {item['original_text']}\n"
                download_content += "-"*20 + "\n\n"

            # Botões de Download e Copiar Lado a Lado
            col_dl, col_copy = st.columns(2)
            with col_dl:
                st.download_button(
                    label=get_text("download_results_button"),
                    data=download_content,
                    file_name=get_text("download_filename"),
                    mime="text/plain",
                    icon=get_text("download_button_icon")
                )
            with col_copy:
                if st.button(get_text("copy_results_button"), icon=get_text("copy_button_icon")):
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

            # --- Paginação ---
            snippets_per_page = 10
            total_snippets = len(filtered_snippets)
            total_pages = (total_snippets + snippets_per_page - 1) // snippets_per_page

            if 'current_page' not in st.session_state:
                st.session_state.current_page = 1

            # Garante que a página atual não exceda o total de páginas
            if st.session_state.current_page > total_pages and total_pages > 0:
                st.session_state.current_page = total_pages
            elif total_pages == 0:
                st.session_state.current_page = 0 # Nenhuma página se não há snippets

            if total_pages > 0: # Exibir botões de navegação apenas se houver páginas
                col_prev, col_page_info, col_next = st.columns([1,2,1])
                with col_prev:
                    if st.session_state.current_page > 1:
                        st.button(get_text("previous_page_button"), on_click=lambda: st.session_state.update(current_page=st.session_state.current_page - 1))
                with col_page_info:
                    st.markdown(f"<p style='text-align: center;'>{get_text('page_info').format(current=st.session_state.current_page, total=total_pages)}</p>", unsafe_allow_html=True)
                with col_next:
                    if st.session_state.current_page < total_pages:
                        st.button(get_text("next_page_button"), on_click=lambda: st.session_state.update(current_page=st.session_state.current_page + 1))
            else:
                st.info(get_text("no_snippets_found_on_page")) # Mensagem para quando não há snippets filtrados

            start_idx = (st.session_state.current_page - 1) * snippets_per_page
            end_idx = start_idx + snippets_per_page
            snippets_to_display = filtered_snippets[start_idx:end_idx]

            # --- EXIBIÇÃO AGRUPADA POR ARQUIVO (usando snippets_to_display) ---
            if snippets_to_display:
                unique_files_in_displayed_results = sorted(list(set(s['file_name'] for s in snippets_to_display)))
                for file_name in unique_files_in_displayed_results:
                    st.markdown(f"#### {get_text('results_from_file')} `{file_name}`")

                    snippets_for_this_file_and_page = [s for s in snippets_to_display if s['file_name'] == file_name]

                    for item in snippets_for_this_file_and_page:
                        st.markdown(f"**{get_text('terms_found_header').replace(':', '')}:** `{item['term']}` ({get_text('page_number_label')} {item['page_num']})")
                        st.markdown(f"...{item['snippet']}...", unsafe_allow_html=True)
                        st.markdown("---")
            elif total_pages > 0: # Se houver páginas mas a atual não tiver snippets (devido a filtro, por exemplo)
                st.info(get_text("no_snippets_found_on_page"))

        else: # Nenhum snippet após a filtragem/ordenação
            st.info(get_text("no_snippets_found"))
    else: # Nenhum termo de busca encontrado no documento
        st.warning(get_text("no_terms_found"))

# Mensagem inicial ou de orientação (exibida se nenhum resultado foi processado ainda)
if not st.session_state.results_displayed:
    st.info(get_text("initial_guidance"))
