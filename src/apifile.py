from requests import Session
from src.db import Document, DocumentText
from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from datetime import datetime
from celery import Celery

router = APIRouter()

@router.post("/upload_doc")
async def upload_doc(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = f"/home/reedieboi/Docs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    new_doc = Document(psth=file_path, date=str(datetime.utcnow()))
    Session.add(new_doc)
    Session.commit()
    return {"id": new_doc.id, "filename": file.filename}

app.include_router(router)

@router.delete("/doc_delete/{doc_id}")
async def doc_delete(doc_id: int):
    doc = Session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if os.path.exists(doc.psth):
        os.remove(doc.psth)
    Session.delete(doc)
    Session.commit()
    return {"message": "Document deleted"}

celery_app = Celery("tasks", broker="pyamqp://guest@localhost//")

@router.post("/doc_analyse/{doc_id}")
async def doc_analyse(doc_id: int):
    task = celery_app.send_task('analyse_document', args=[doc_id])
    return {"task_id": task.id}

@celery_app.task
def analyse_document(doc_id):
    doc = Session.get(Document, doc_id)
    text = tesseract_extract_text(doc.psth)  # Вы должны определить эту функцию
    new_text = DocumentText(id_doc=doc_id, text=text)
    Session.add(new_text)
    Session.commit()