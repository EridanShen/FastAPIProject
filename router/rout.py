from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.db import Document, DocumentText
from src.depends import get_session
import os
from datetime import datetime

router = APIRouter()

@router.post("/upload_doc")
async def upload_doc(file: UploadFile = File(...), session: Session = Depends(get_session)):
    file_path = f"/home/reedieboi/Docs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    new_doc = Document(path=file_path, date=str(datetime.utcnow()))
    session.add(new_doc)
    session.commit()
    return {"id": new_doc.id, "filename": file.filename}

@router.delete("/doc_delete/{doc_id}")
async def doc_delete(doc_id: int, session: Session = Depends(get_session)):
    doc = session.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if os.path.exists(doc.path):
        os.remove(doc.path)
    session.delete(doc)
    session.commit()
    return {"message": "Document deleted"}

@router.get("/get_text/{doc_id}")
async def get_text(doc_id: int, session: Session = Depends(get_session)):
    texts = session.query(DocumentText).filter(DocumentText.document_id == doc_id).all()
    if not texts:
        raise HTTPException(status_code=404, detail="Text not found")
    return {"texts": [text.text for text in texts]}
