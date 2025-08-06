import PyPDF2
import fitz
import pytesseract
from PIL import Image  
import os

# Some setup 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'


def main():
    print("Insert the file path:")
    print("data/", end='')
    path = input()
    
    try:
        file = open(f"data/{path}", "rb")
    except FileNotFoundError:
        print("File not found")
        return
    
    reader = PyPDF2.PdfReader(file)
    
    num_of_pages = len(reader.pages)
    print("No of pages: ", num_of_pages)
    for i in range(num_of_pages):    
        page = reader.pages[i]
        print(page.extract_text())


def read_all(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text() + '\n'
    return text


def read_first(file) -> str:
    reader = PyPDF2.PdfReader(file)
    return reader.pages[0].extract_text()


def read_all_image(path):
    text = ""

    try:
        doc = fitz.open(path)

        for i, page in enumerate(doc.pages()):
            pix = page.get_pixmap(dpi=300)

            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            page_text = pytesseract.image_to_string(img, lang='por')
            
            text += page_text + "\n"

        doc.close()
        return text

    except Exception as e:
        return f"There was an error: {e}\n\nVerify if Tesseract is correctly installed."



def read_first_image(path):
    try:
        doc = fitz.open(path)

        if not doc.page_count:
            doc.close()
            return "Error: The PDF document is empty."

        first_page = doc[0]
        
        pix = first_page.get_pixmap(dpi=300)
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        text = pytesseract.image_to_string(img, lang='por')
        
        doc.close()
        return text.strip()

    except Exception as e:
        return f"An error occurred: {e}"



if __name__ == '__main__':
    main()