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
        "no_keywords_info": "Nenhuma palavra-chave encontrada (exceto stopwords e palavras curtas)."
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
        "no_keywords_info": "No keywords found (excluding stopwords and short words)."
    }
}

SUPPORTED_LANGUAGES = {
    "pt": "Português",
    "en": "English"
}
