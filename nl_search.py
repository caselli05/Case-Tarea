import json
import numpy as np
from pdf_reader import read_all, read_all_image
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def main():
    sentences = 'Alou'
    embeddings = model.encode(sentences)

    print(embeddings)


def encode_pdfs():
    pdfs_names = ['Lei_9394_20121996.pdf', 'Lei_9784_29011999.pdf', 'Lei_14945_31072024.pdf',
                  'Portaria_44_28052025.pdf', 'Portaria_81_25082015.pdf', 'Portaria_2140_04072025.pdf',
                  'Resolucao_99_156202023.pdf', 'Resolucao_909_28032022.pdf', 'Resolucao_2430_21052025.pdf', 'Resolucao_2434_03072025.pdf']
    
    for pdf_name in pdfs_names:
        data = []
        path = f'data/{pdf_name}'
        try:
            file = open(f"{path}", "rb")
        except FileNotFoundError:
            return "File not found"

        text = read_all(file)    
        if text == "":
            text = read_all_image(path)
        print(f'Read file {pdf_name}')

        sentences = re.split('.\n', text)
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
    
    json_path = 'data/embedding.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data stored in {json_path}")
    
















if __name__ == '__main__':
    encode_pdfs()
    # main()