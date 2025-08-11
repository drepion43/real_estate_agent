from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from typing import List, Any, Optional, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable

from dotenv import load_dotenv
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def format_docs(docs: List[Document]) -> str:
    """검색된 문서 리스트를 하나의 문자열로 병합"""
    return "\n".join([doc.page_content for doc in docs])

def create_retriever(file_path: str) -> Any:
    docs = []
    # for file_path in file_paths:
    #     loader = PyPDFLoader(file_path)
    #     doc_loader = loader.load()
    #     docs.extend(doc_loader)
    
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs_splitterd = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
    vector_db = Chroma.from_documents(documents=docs_splitterd, embedding=embeddings)
    retriever = vector_db.as_retriever()
    return retriever