from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_FOLDER = Path("uploads")

pdfs = list(UPLOAD_FOLDER.glob("*.pdf"))

print("PDFs found:", pdfs)

loader = PyPDFLoader(str(pdfs[0]))

docs = loader.load()

print("Pages:", len(docs))

print(docs[0].page_content[:1000])