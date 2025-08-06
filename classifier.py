from pdf_reader import read_first, read_first_image
import re

def main():
    print("Insert the file path:")
    print("data/", end='')
    path = input()
    
    print(classify(f'data/{path}'))
    

def classify(path) -> str:
    try:
        file = open(f"{path}", "rb")
    except FileNotFoundError:
        return "File not found"
    
    pattern = r'\b(Lei|Portaria|Resolução)\b'

    text = read_first(file)    
    if text == "":
        text = read_first_image(path)

    matches = re.findall(pattern, text, re.IGNORECASE)
    clusters = ['Lei', 'Portaria', 'Resolução']

    if not matches:
        return 'Unable to Classify this file'
    
    first_match = matches[0]
    for cluster in clusters:
        if first_match.lower() == cluster.lower():
            return cluster
        
    return 'Unable to Classify this file'


if __name__ == '__main__':
    main()