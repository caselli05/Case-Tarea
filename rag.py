from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from nl_search import check_similarity

llm = Ollama(model="mistral")

def main():
    print("Qual a sua pergunta?")
    user_question = input()

    (response, sources) = answer_question(user_question)

    print(response)
    print(f"Sources: {sources}")


def answer_question(user_question:str,
                    top_k=5, 
                    loaded_data=None, 
                    model=llm,
                    embedding_model=None) -> tuple[str, str]:
    (relevant_context, sources) = check_similarity(user_question, top_k, loaded_data, embedding_model=embedding_model)

    prompt_template = ChatPromptTemplate.from_template(
        """Use os seguintes trechos de um documento para responder à pergunta no final. Se a resposta não estiver contida nos trechos, diga 'A informação não foi encontrada nos documentos fornecidos.'

    TRECHOS:
    {context}

    PERGUNTA:
    {question}
    """
    )

    chain = prompt_template | model

    response = chain.invoke({"context": relevant_context, "question": user_question})

    sources_str = ", ".join(list(sources))
    
    return (response, f"Fontes: {sources_str}")
