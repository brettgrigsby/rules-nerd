import PyPDF2
import sys

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            
    return text

if len(sys.argv) > 1:
    file_path = sys.argv[1]
    text = extract_text_from_pdf(file_path)
    print(text)

    # TODO: create embeddings from text and store in vectorstore
else:
    print("Please provide a PDF file path as a command-line argument.")
