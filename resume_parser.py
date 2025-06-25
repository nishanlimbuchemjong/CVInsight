import re
import docx2txt
import PyPDF2

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return " ".join([page.extract_text() or '' for page in reader.pages])
    elif file_path.endswith('.docx') or file_path.endswith('.doc'):
        return docx2txt.process(file_path)
    else:
        return ""

def extract_details(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'\+?\d[\d -]{8,}', text)
    skills = re.findall(r'\b(Python|Java|C\+\+|SQL|HTML|CSS|JavaScript|Flask|Django)\b', text, re.IGNORECASE)
    name = text.strip().split('\n')[0][:100]  # naive name guess
    return {
        'name': name,
        'email': email.group() if email else None,
        'phone': phone.group() if phone else None,
        'skills': ', '.join(set(skills))
    }
