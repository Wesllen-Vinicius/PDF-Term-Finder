# pdf_processor.py

import fitz  # PyMuPDF
import io
import re
import streamlit as st
from collections import Counter

def extract_text_from_pdf(pdf_file, messages):
    """
    Extrai texto de um arquivo PDF usando PyMuPDF.
    Retorna uma tupla (texto_completo, lista_de_paginas) ou (None, None) em caso de erro.
    lista_de_paginas: [{"text": "conteúdo da página", "page_num": número_da_página}]
    """
    full_text = ""
    pages_data = []
    try:
        pdf_document = fitz.open(stream=pdf_file.getvalue(), filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            full_text += page_text
            pages_data.append({"text": page_text, "page_num": page_num + 1}) # page_num + 1 para começar em 1
        pdf_document.close()
    except Exception as e:
        st.error(f"{messages['error_reading_pdf']} {e}")
        st.warning(messages['pdf_corruption_warning'])
        st.info(messages['pdf_manual_conversion_guidance']) # Guia adicional para PDFs problemáticos
        return None, None # Retorna None para ambos em caso de erro
    return full_text, pages_data

def find_matches_and_snippets(pages_data, search_terms, case_sensitive=False, whole_word_only=True):
    """
    Encontra termos de busca e seus trechos relevantes nos dados das páginas do PDF,
    com opções de busca, contagem de ocorrências e trechos maiores (parágrafos) com número da página.
    """
    found_terms = set()
    snippets_with_terms = [] # Armazena {term: '', snippet: '', original_text: '', page_num: ''}
    term_counts = Counter()
    total_words = 0

    # Processa cada página individualmente para manter o contexto de página
    for page_info in pages_data:
        page_text = page_info["text"]
        page_num = page_info["page_num"]

        # Contagem total de palavras no documento (para estatísticas)
        total_words += len(re.findall(r'\b\w+\b', page_text.lower()))

        # Divide o texto da página em parágrafos para um contexto de trecho maior
        paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n|\n\s*', page_text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        for term in search_terms:
            if not term.strip():
                continue

            # Prepara o padrão regex baseado nas opções de busca
            term_escaped = re.escape(term.strip())

            if whole_word_only:
                pattern = r'\b' + term_escaped + r'\b'
            else:
                pattern = r'' + term_escaped

            flags = 0
            if not case_sensitive:
                flags |= re.IGNORECASE

            regex = re.compile(pattern, flags)

            for paragraph in paragraphs:
                matches_in_paragraph = list(regex.finditer(paragraph))
                if matches_in_paragraph:
                    found_terms.add(term.strip())

                    for _ in matches_in_paragraph:
                        term_counts[term.strip()] += 1

                    highlighted_paragraph = regex.sub(lambda m: f'<mark>{m.group(0)}</mark>', paragraph)

                    snippets_with_terms.append({
                        "term": term.strip(),
                        "snippet": highlighted_paragraph.strip(),
                        "original_text": paragraph.strip(),
                        "page_num": page_num # Adiciona o número da página
                    })

    # Filtra para exibir apenas snippets únicos (baseado no conteúdo original do parágrafo e página)
    unique_snippets_list = []
    seen_snippets = set()
    for item in snippets_with_terms:
        # Cria uma chave única combinando o texto original do trecho e o número da página
        unique_key = (item['original_text'], item['page_num'])
        if unique_key not in seen_snippets:
            unique_snippets_list.append(item)
            seen_snippets.add(unique_key)

    return list(found_terms), unique_snippets_list, dict(term_counts), total_words
