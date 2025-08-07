import json
import numpy as np
from pdf_reader import read_all, read_all_image
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
json_name = "data/embedding-pt.json"


def main():
    print("Digite sua pergunta:")
    prompt = input()

    res = check_similarity(prompt)

    print(res)


def encode_pdfs():
    pdfs_names = ['Lei_9394_20121996.pdf', 'Lei_9784_29011999.pdf', 'Lei_14945_31072024.pdf',
                  'Portaria_44_28052025.pdf', 'Portaria_81_25082015.pdf', 'Portaria_2140_04072025.pdf',
                  'Resolucao_99_156202023.pdf', 'Resolucao_909_28032022.pdf', 'Resolucao_2430_21052025.pdf', 'Resolucao_2434_03072025.pdf']
    
    data = []
    for pdf_name in pdfs_names:
        path = f'data/{pdf_name}'
        try:
            file = open(f"{path}", "rb")
        except FileNotFoundError:
            return "File not found"

        text = read_all(file)    
        if text == "":
            text = read_all_image(path)
        print(f'Read file {pdf_name}')

        # --- Instanciando e configurando o splitter ---
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            
            chunk_overlap=200,
            length_function=len,
            
            is_separator_regex=False,
        )

        sentences = text_splitter.split_text(text)
        
        embeddings = model.encode(sentences)
        print(" Encoded sentences from this file")
        for i, sentence in enumerate(sentences):
            data.append({
                'path': pdf_name,
                'sentence': sentence,
                'embedding': embeddings[i].tolist()
            })

            if (i+1)%100 == 0:
                print(f'    Saved {i+1}/{len(sentences)}')
        print(" Finish saving sentences")
    
    json_path = json_name
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data stored in {json_path}")


def check_similarity(prompt:str, 
                     top_k:int = 5, 
                     loaded_data=None,
                     embedding_model=model) -> tuple[set, set[str]]:
    if not embedding_model:
        embedding_model=model
    if not loaded_data:
        embendding_json = json_name
        with open(embendding_json, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
    
    doc_embeddings = [np.array(item['embedding']) for item in loaded_data]
    doc_paragraphs = [item['sentence'] for item in loaded_data]
    doc_sources = [item['path'] for item in loaded_data]
    
    embedded_prompt = embedding_model.encode(prompt)

    similarity_scores = cosine_similarity(
        [embedded_prompt],
        doc_embeddings
    )

    scores = similarity_scores[0]
    top_idx = np.argsort(scores)[-top_k:][::-1]

    sources = set()
    res = ""
    for i, index in enumerate(top_idx):
        best_match_paragraph = doc_paragraphs[index]
        best_match_source = doc_sources[index]
        res = res + (f"Fonte: '{best_match_source}'\n"
                     f"Trecho: \"{best_match_paragraph}\"\n")

        best_match_score = scores[index]
        print(f"\n--- Resultado {i+1} ---\n"
                     f"Fonte: '{best_match_source}'\n"
                     f"Similaridade: {best_match_score:.2f}\n"
                     f"Trecho: \"{best_match_paragraph}\"\n")
        sources.add(best_match_source)

    print("\n\n")

    return (res, sources)








if __name__ == '__main__':
    # main()
    encode_pdfs()