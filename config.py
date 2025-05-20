# config.py

APP_NAME = {
    "pt": "Localizador de Termos em PDFs",
    "en": "PDF Term Finder"
}

# Dicionário de mensagens para diferentes idiomas
MESSAGES = {
    "pt": {
        "upload_instructions": "Faça o upload de um arquivo PDF e insira os termos (palavras, frases, tópicos) que você deseja encontrar. Cada termo deve estar em uma nova linha na caixa de texto abaixo.",
        "search_terms_input_label": "Insira seus termos de busca (um por linha):",
        "search_terms_input_placeholder": "Exemplo:\nGovernança Corporativa\nLei Geral de Proteção de Dados\nRelatório Financeiro\nSustentabilidade",
        "file_uploader_label": "Escolha um arquivo PDF",
        "processing_spinner": "Processando PDF...",
        "results_header": "Resultados:",
        "terms_found_header": "Termos de busca encontrados no documento:",
        "relevant_snippets_header": "Trechos Relevantes:",
        "no_snippets_found": "Nenhum trecho encontrado para os termos especificados.",
        "no_terms_found": "Nenhum dos termos de busca foi encontrado no documento.",
        "please_enter_terms": "Por favor, insira os termos de busca na caixa de texto.",
        "please_upload_file": "Por favor, faça o upload de um arquivo PDF.",
        "error_reading_pdf": "Erro ao ler o PDF:",
        "pdf_corruption_warning": "Por favor, verifique se o arquivo PDF não está corrompido, protegido por senha ou em um formato inválido.",
        "select_language": "Selecione o Idioma:",
        "no_keywords_info": "Nenhuma palavra-chave encontrada (exceto stopwords e palavras curtas).",
        "search_options_header": "Opções de Busca:",
        "case_sensitive_checkbox": "Diferenciar maiúsculas/minúsculas",
        "whole_word_checkbox": "Apenas palavras inteiras",
        "stats_header": "Estatísticas do Documento:",
        "total_words_count": "Total de palavras no documento:",
        "term_occurrences": "Ocorrências dos Termos:",
        "download_results_button": "Baixar Resultados (.txt)",
        "download_filename": "resultados_busca.txt",
        "page_number_label": "Página:",
        "clear_button_label": "Limpar Tudo",
        "pdf_manual_conversion_guidance": "Se este erro persistir, o PDF pode ter uma proteção avançada. Tente converter o PDF para texto simples (TXT) usando uma ferramenta online (ex: 'PDF para TXT' do Smallpdf ou Adobe Acrobat online) e depois carregue o TXT no campo de texto para busca, ou use um PDF que não tenha essa proteção.",
        "process_button_label": "Processar Busca",
        "initial_guidance": "Faça o upload de um arquivo PDF e insira os termos de busca. Em seguida, clique em 'Processar Busca'.",
        # --- NOVAS MENSAGENS ---
        "copy_results_button": "Copiar Resultados",
        "copy_instructions": "Copie o texto abaixo:"
    },
    "en": {
        "upload_instructions": "Upload a PDF file and enter the terms (words, phrases, topics) you want to find. Each term should be on a new line in the text box below.",
        "search_terms_input_label": "Enter your search terms (one per line):",
        "search_terms_input_placeholder": "Example:\nCorporate Governance\nGeneral Data Protection Law\nFinancial Report\nSustainability",
        "file_uploader_label": "Choose a PDF file",
        "processing_spinner": "Processing PDF...",
        "results_header": "Results:",
        "terms_found_header": "Search terms found in the document:",
        "relevant_snippets_header": "Relevant Snippets:",
        "no_snippets_found": "No snippets found for the specified terms.",
        "no_terms_found": "None of the search terms were found in the document.",
        "please_enter_terms": "Please enter search terms in the text box.",
        "please_upload_file": "Please upload a PDF file.",
        "error_reading_pdf": "Error reading PDF:",
        "pdf_corruption_warning": "Please check if the PDF file is not corrupted, password-protected, or in an invalid format.",
        "select_language": "Select Language:",
        "no_keywords_info": "No keywords found (excluding stopwords and short words).",
        "search_options_header": "Search Options:",
        "case_sensitive_checkbox": "Case-sensitive search",
        "whole_word_checkbox": "Whole words only",
        "stats_header": "Document Statistics:",
        "total_words_count": "Total words in document:",
        "term_occurrences": "Term Occurrences:",
        "download_results_button": "Download Results (.txt)",
        "download_filename": "search_results.txt",
        "page_number_label": "Page:",
        "clear_button_label": "Clear All",
        "pdf_manual_conversion_guidance": "If this error persists, the PDF might have advanced protection. Try converting the PDF to plain text (TXT) using an online tool (e.g., Smallpdf 'PDF to TXT' or Adobe Acrobat online) and then upload the TXT to the text input field for searching, or use a PDF without such protection.",
        "process_button_label": "Process Search",
        "initial_guidance": "Upload a PDF file and enter search terms. Then click 'Process Search'.",
        # --- NOVAS MENSAGENS ---
        "copy_results_button": "Copy Results",
        "copy_instructions": "Copy the text below:"
    }
}

SUPPORTED_LANGUAGES = {
    "pt": "Português",
    "en": "English"
}
