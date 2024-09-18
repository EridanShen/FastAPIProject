from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    date = Column(String, index=True)
    texts = relationship("DocumentText", back_populates="document")

class DocumentText(Base):
    __tablename__ = 'document_texts'
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    text = Column(String, index=True)
    document = relationship("Document", back_populates="texts")


