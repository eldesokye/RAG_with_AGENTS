import requests
from config import API_URL

def upload_pdfs(files):
    files_payload = [
        ('files', (file.name, file.getvalue(), file.type))
        for file in files
    ]

    response = requests.post(f"{API_URL}/upload_pdfs/", files=files_payload)
    return response.json()

def ask_question(question):
    payload = {"question": question}
    response = requests.post(f"{API_URL}/ask/", data=payload)
    return response.json()