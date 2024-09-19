from pydantic import BaseModel
from requests import Session
from src.db import Document, DocumentText
from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from datetime import datetime
from src.main import app
from celery_worker import process_document

router = APIRouter()


class DocumentTextSchema(BaseModel):
    id: int
    id_doc: int
    text: str

    class Config:
        orm_mode = True

@app.get("/get_text/{doc_id}", response_model=DocumentTextSchema, summary="Retrieve document text",
         description="Returns the extracted text of a given document by its ID.")
async def get_text(doc_id: int):
    doc_text = Session.query(DocumentText).filter(DocumentText.id_doc == doc_id).first()
    if doc_text:
        return doc_text
    else:
        raise HTTPException(status_code=404, detail="Text not found")



@app.get("/get_text/{doc_id}", response_model=DocumentTextSchema)
async def get_text(doc_id: int):
        doc_text = Session.query(DocumentText).filter(DocumentText.id_doc == doc_id).first()
        if doc_text:
            return doc_text
        else:
            raise HTTPException(status_code=404, detail="Text not found")


@app.post("/upload_doc")
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

@app.delete("/doc_delete/{doc_id}")
async def doc_delete(doc_id: int):
    doc = Session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if os.path.exists(doc.psth):
        os.remove(doc.psth)
    Session.delete(doc)
    Session.commit()
    return {"message": "Document deleted"}



@app.post("/doc_analyse/{doc_id}")
async def doc_analyse(doc_id: int):
    result = process_document.delay(doc_id)
    return {"message": "Processing started", "task_id": result.task_id}
