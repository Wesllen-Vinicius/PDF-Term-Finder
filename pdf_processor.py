# pdf_processor.py

import fitz  # PyMuPDF
import io
import re

def extract_text_from_pdf(pdf_file, messages):
    """
    Extrai texto de um arquivo PDF usando PyMuPDF.
    Retorna o texto extraído ou None em caso de erro.
    """
    text = ""
    try:
        # A forma original que você testou e deseja manter.
        # pdf_file.getvalue() retorna o conteúdo do arquivo como bytes.
        pdf_document = fitz.open(stream=pdf_file.getvalue(), filetype="pdf")
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
    except Exception as e:
        # Usando as mensagens do arquivo de configuração
        st.error(f"{messages['error_reading_pdf']} {e}")
        st.warning(messages['pdf_corruption_warning'])
        return None
    return text

def find_matches_and_snippets(text, search_terms):
    """
    Encontra termos de busca e seus trechos relevantes no texto.
    Retorna uma lista de termos encontrados e uma lista de snippets.
    """
    found_terms = set()
    snippets = []
    # Divide o texto em sentenças. Ajustado para ser mais robusto com pontuações
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    for term in search_terms:
        if not term.strip():
            continue # Pula termos vazios

        # Prepara o padrão regex para busca case-insensitive e captura exata da palavra/frase
        term_escaped = re.escape(term.strip())

        # Usa word boundaries (\b) para palavras inteiras, mas não para frases
        if ' ' in term_escaped:
            pattern = r'' + term_escaped
        else:
            pattern = r'\b' + term_escaped + r'\b'

        regex = re.compile(pattern, re.IGNORECASE)

        for sentence in sentences:
            if regex.search(sentence):
                found_terms.add(term.strip())
                # Destaca o termo na sentença encontrada usando HTML <mark>
                highlighted_sentence = regex.sub(lambda m: f'<mark>{m.group(0)}</mark>', sentence)
                snippets.append({"term": term.strip(), "snippet": highlighted_sentence.strip()})

    return list(found_terms), snippets
