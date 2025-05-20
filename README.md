# Localizador de Termos em PDFs

Este é um aplicativo web interativo, construído com Streamlit, que permite extrair texto de arquivos PDF, buscar por termos (palavras, frases, tópicos) definidos pelo usuário e exibir trechos relevantes onde esses termos são encontrados. O aplicativo suporta múltiplos idiomas para a interface.

## Funcionalidades

- **Upload de PDF:** Carregue facilmente seus arquivos PDF através da interface.
- **Busca por Termos Personalizados:** Insira uma lista de termos (um por linha) que o sistema irá procurar no conteúdo do PDF.
- **Extração de Trechos Relevantes:** Visualize sentenças ou parágrafos que contêm os termos buscados, com os termos destacados.
- **Interface Multilíngue:** Alterne entre Português e Inglês para a interface do usuário.
- **Modular:** O código é organizado em módulos (`app.py`, `pdf_processor.py`, `config.py`) para melhor manutenção e legibilidade.

## Pré-requisitos

Antes de começar, certifique-se de ter o Python instalado em sua máquina. Este projeto foi testado com Python 3.8+.

## Configuração do Ambiente

1.  **Crie a Estrutura de Pastas:**
    Crie uma pasta para o seu projeto (ex: `pdf_finder_app`) e, dentro dela, crie os três arquivos Python: `app.py`, `pdf_processor.py`, e `config.py`.

    ```
    pdf_finder_app/
    ├── app.py
    ├── pdf_processor.py
    └── config.py
    ```

2.  **Copie o Código:**

    - **`config.py`**: Cole o conteúdo fornecido no bloco "Arquivo 1: `config.py`".
    - **`pdf_processor.py`**: Cole o conteúdo fornecido no bloco "Arquivo 2: `pdf_processor.py`".
    - **`app.py`**: Cole o conteúdo fornecido no bloco "Arquivo 3: `app.py`".

3.  **Instale as Dependências Python:**
    Navegue até a pasta `pdf_finder_app` no seu terminal e instale as bibliotecas necessárias usando `pip`:

    ```bash
    pip install streamlit PyMuPDF
    ```

    **(Opcional, mas recomendado) Ambiente Virtual:**
    Para isolar as dependências do seu projeto, você pode criar e ativar um ambiente virtual antes de instalar as dependências:

    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

## Como Executar

1.  No seu terminal, certifique-se de estar dentro da pasta `pdf_finder_app`.
2.  Execute o aplicativo Streamlit:

    ```bash
    streamlit run app.py
    ```

3.  Um navegador será aberto automaticamente, exibindo a interface do aplicativo. Você pode então carregar seus PDFs e inserir os termos de busca.

---

# PDF Term Finder

This is an interactive web application, built with Streamlit, that allows you to extract text from PDF files, search for user-defined terms (words, phrases, topics), and display relevant snippets where these terms are found. The application supports multiple languages for the user interface.

## Features

- **PDF Upload:** Easily upload your PDF files through the interface.
- **Custom Term Search:** Enter a list of terms (one per line) that the system will search for within the PDF content.
- **Relevant Snippet Extraction:** View sentences or paragraphs containing the searched terms, with the terms highlighted.
- **Multilingual Interface:** Switch between Portuguese and English for the user interface.
- **Modular Design:** The code is organized into modules (`app.py`, `pdf_processor.py`, `config.py`) for better maintainability and readability.

## Prerequisites

Before you begin, ensure you have Python installed on your machine. This project has been tested with Python 3.8+.

## Environment Setup

1.  **Create Folder Structure:**
    Create a folder for your project (e.g., `pdf_finder_app`) and, inside it, create the three Python files: `app.py`, `pdf_processor.py`, and `config.py`.

    ```
    pdf_finder_app/
    ├── app.py
    ├── pdf_processor.py
    └── config.py
    ```

2.  **Copy the Code:**

    - **`config.py`**: Paste the content provided in the "File 1: `config.py`" block.
    - **`pdf_processor.py`**: Paste the content provided in the "File 2: `pdf_processor.py`" block.
    - **`app.py`**: Paste the content provided in the "File 3: `app.py`" block.

3.  **Install Python Dependencies:**
    Navigate to your `pdf_finder_app` folder in your terminal and install the required libraries using `pip`:

    ```bash
    pip install streamlit PyMuPDF
    ```

    **(Optional, but recommended) Virtual Environment:**
    To isolate your project's dependencies, you can create and activate a virtual environment before installing dependencies:

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

## How to Run

1.  In your terminal, make sure you are inside the `pdf_finder_app` folder.
2.  Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

3.  A web browser will automatically open, displaying the application interface. You can then upload your PDFs and enter your search terms.
