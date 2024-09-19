from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytesseract
from PIL import Image

app = Celery('tasks', broker='pyamqp://reedieboi@localhost//')

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.task
def process_document(doc_id):
    from db import Document, DocumentText
    doc = session.query(Document).get(doc_id)
    if doc:
        path = doc.psth
        text = pytesseract.image_to_string(Image.open(path))
        doc_text = DocumentText(id_doc=doc_id, text=text)
        session.add(doc_text)
        session.commit()
        return f'Text processed for document {doc_id}'
    else:
        return 'Document not found'
