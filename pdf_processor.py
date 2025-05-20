import fitz
import io
import re
import streamlit as st
from collections import Counter
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_file, messages, try_ocr_on_fail=False, progress_callback=None):
    full_text = ""
    pages_data = []
    file_name = pdf_file.name
    try:
        pdf_document = fitz.open(stream=pdf_file.getvalue(), filetype="pdf")
        total_pages = pdf_document.page_count

        for page_num in range(total_pages):
            if progress_callback:
                progress_callback(page_num + 1, total_pages, file_name)

            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            if not page_text and try_ocr_on_fail:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                page_text = pytesseract.image_to_string(img, lang='por+eng')
            full_text += page_text
            pages_data.append({"text": page_text, "page_num": page_num + 1})
        pdf_document.close()
    except Exception as e:
        st.error(f"{messages['error_reading_pdf']} '{file_name}': {e}")
        st.warning(messages['pdf_corruption_warning'])
        if not try_ocr_on_fail:
            st.info(messages['pdf_manual_conversion_guidance'])
        else:
            st.warning(messages['ocr_failure_warning'])
        return None, None, None
    return full_text, pages_data, file_name

def find_matches_and_snippets(pages_data, search_terms, case_sensitive=False, whole_word_only=True, file_name="", is_regex=False):
    found_terms = set()
    snippets_with_terms = []
    term_counts = Counter()
    total_words = 0

    for page_info in pages_data:
        page_text = page_info["text"]
        page_num = page_info["page_num"]

        total_words += len(re.findall(r'\b\w+\b', page_text.lower()))

        paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n|\n\s*', page_text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        for term in search_terms:
            if not term.strip():
                continue

            if is_regex:
                pattern = term.strip()
            else:
                term_escaped = re.escape(term.strip())
                if whole_word_only:
                    pattern = r'\b' + term_escaped + r'\b'
                else:
                    pattern = r'' + term_escaped

            flags = 0
            if not case_sensitive:
                flags |= re.IGNORECASE

            try:
                regex = re.compile(pattern, flags)
            except re.error as e:
                st.warning(f"Erro na expressão regular '{term}': {e}. Este termo será ignorado.")
                continue

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
                        "page_num": page_num,
                        "file_name": file_name
                    })

    unique_snippets_list = []
    seen_snippets = set()
    for item in snippets_with_terms:
        unique_key = (item['original_text'], item['page_num'], item['file_name'])
        if unique_key not in seen_snippets:
            unique_snippets_list.append(item)
            seen_snippets.add(unique_key)

    return list(found_terms), unique_snippets_list, dict(term_counts), total_words
