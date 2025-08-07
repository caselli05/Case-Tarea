# Estudo de Caso: Chatbot RAG para Análise de Documentos PDF

Este projeto foi desenvolvido como parte do estudo de caso para o processo seletivo de Estágio em Dados e IA. A solução implementa um sistema de **Retrieval-Augmented Generation (RAG)** capaz de processar uma coleção de documentos PDF, extrair seu conteúdo, e permitir que o usuário faça perguntas sobre eles através de uma interface de chat interativa.

## 🎯 Objetivo Geral

O objetivo é desenvolver uma aplicação que consiga ler, classificar e interagir com o conteúdo de múltiplos documentos PDF de forma inteligente. A entrega final consiste neste repositório e em uma apresentação online. [cite_start]O prazo para entrega é **11 de agosto de 2025**[cite: 122].

## ✨ Funcionalidades

- [cite_start]**Extração de Texto:** Extrai conteúdo textual de arquivos PDF, com suporte a OCR para documentos baseados em imagem. [cite: 128]
- [cite_start]**Classificação Automática:** Classifica cada documento em categorias (ex: Lei, Portaria, Resolução) com base em palavras-chave encontradas no texto. [cite: 129]
- [cite_start]**Busca Semântica:** Permite que o usuário encontre os trechos de texto mais relevantes para uma pergunta feita em linguagem natural, utilizando embeddings e similaridade de cosseno. [cite: 130]
- [cite_start]**Chat Interativo com LLM:** Oferece uma interface de chat onde um Modelo de Linguagem (LLM) local responde às perguntas do usuário com base no contexto extraído dos documentos. [cite: 131, 132]

## 🛠️ Stack de Tecnologias

- **Linguagem:** Python 3.10+
- **Interface Web:** Streamlit
- **Orquestração RAG:** LangChain
- **LLM Local:** Ollama (com o modelo Mistral 7B)
- **Embeddings:** Sentence-Transformers (`paraphrase-multilingual-mpnet-base-v2`)
- **Processamento de PDF:** PyMuPDF (OCR com Pytesseract)
- **Manipulação de Dados:** NumPy, Scikit-learn

## ⚙️ Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **Python 3.10 ou superior.**
2.  **Git** para clonar o repositório.
3.  **Ollama:** A aplicação deve estar instalada e rodando em sua máquina para servir o LLM.
    - Faça o download em: [ollama.com](https://ollama.com/)

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio

### 2. Configurar o Ambiente Virtual
É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

- **Windows:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
- **macOS / Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 3. Instalar as Dependências
Instale todas as bibliotecas Python necessárias com um único comando.
```bash
pip install -r requirements.txt

### 4. Baixar o Modelo de Linguagem (LLM)
Com o Ollama já instalado e em execução, baixe o modelo `mistral` através do seu terminal. Isso só precisa ser feito uma vez.
```bash
ollama pull mistral

### 5. Preparar os Dados (Gerar Embeddings)
Este passo lê todos os PDFs da pasta `/data`, os divide em chunks, gera os embeddings e salva tudo em um arquivo JSON.

- Primeiro, coloque os 10 arquivos PDF fornecidos na pasta `/data`.
- Em seguida, execute o script de preparação:
    ```bash
    python encode_pdfs.py
    ```
Ao final, um arquivo chamado `embedding.json` será criado na pasta `/data`.

### 6. Iniciar a Aplicação Web
Com os embeddings gerados e o Ollama rodando, inicie a interface de chat do Streamlit.
```bash
streamlit run app.py
A aplicação será aberta automaticamente no seu navegador em um endereço local (ex: http://localhost:8501).

## 📁 Estrutura do Projeto
```
.
├── 📄 .gitignore
├── 📄 README.md
├── 📄 app.py                  # Script principal da aplicação Streamlit (interface)
├── 📄 encode_pdfs.py          # Script para processar os PDFs e criar os embeddings
├── 📄 rag.py                  # Contém as funções de lógica do RAG (busca, resposta, etc.)
├── 📄 requirements.txt        # Lista de dependências Python
└── 📁 data/
    ├── 📄 Lei_14945_31072024.pdf # (e outros 9 arquivos PDF)
    └── 📄 embedding.json        # Arquivo gerado pelo encode_pdfs.py
```