from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    psth = Column(String)
    date = Column(Date)

class DocumentText(Base):
    __tablename__ = 'documents_text'
    id = Column(Integer, primary_key=True)
    id_doc = Column(Integer, ForeignKey('documents.id'))
    text = Column(String)
    document = relationship("Document", back_populates="texts")

Document.texts = relationship("DocumentText", order_by=DocumentText.id, back_populates="document")

engine = create_engine("postgresql+psycopg2://postgres:posgtres@localhost/testapi", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


