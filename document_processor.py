from PyPDF2 import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def process_document(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    else:
        with open(file_path, 'r') as file:
            text = file.read()

    sentences = sent_tokenize(text)
    summary = ' '.join(sentences[:3])
    return summary
