import streamlit as st
import json
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama
from rag import answer_question

@st.cache_resource
def load_models():
    embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    llm_model = Ollama(model="mistral")
    return embedding_model, llm_model
model, llm = load_models()

@st.cache_data 
def load_embeddings():
    with open('data/embedding-pt.json', 'r', encoding='utf-8') as f:
        return json.load(f)
loaded_data = load_embeddings()



st.set_page_config(page_title="Chat com Documentos", page_icon="📄")
st.title("Chatbot de Análise de Documentos 💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Faça uma pergunta sobre os documentos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando documentos..."):
            response, sources = answer_question(user_question=prompt, top_k=3, loaded_data=loaded_data, model=llm, embedding_model=model)
            
            full_response = f"{response}\n\n---\n*{sources}*"
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})