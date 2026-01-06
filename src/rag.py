from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
import os
from dotenv import load_dotenv
from memory import get_current_timestamp

load_dotenv()
EMBEDDING_DIR = os.environ.get("EMBEDDING_DB_DIR")
EMBEDDING_MODEL = OpenAIEmbeddings(model='text-embedding-3-small')

def get_vector_store(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        embedding_function=EMBEDDING_MODEL,
        persist_directory=EMBEDDING_DIR
    )
    
def embed_documents(document_dir: str = './docs', collection_name: str = 'user_profile') -> List[Document]:
    vector_store = get_vector_store(collection_name)
    existing_chunk_ids = vector_store.get()['ids']
    if existing_chunk_ids:
        vector_store.delete(ids=existing_chunk_ids)

    docs = os.listdir(document_dir)
    all_chunks = []
    for doc in docs:
        file_path = os.path.join(document_dir, doc)
        pdf_loader = PyPDFLoader(file_path)
        document = pdf_loader.load()

        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n'],
            chunk_size=700,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(document)
        now = get_current_timestamp()
        for idx, chunk in enumerate(chunks):
            chunk.metadata.update({
                'creationdate': now.strftime('%Y-%m-%d %H:%M:%S'),
                'moddate': now.strftime('%Y-%m-%d %H:%M:%S'),
            })

        vector_store.add_documents(chunks)
        all_chunks.extend(chunks)

    return all_chunks

def retrieve_chunks(query: str, k: int = 3, collection_name: str = 'user_profile') -> List[Document]:
    vector_store = get_vector_store(collection_name)
    results = vector_store.similarity_search(query, k=k)
    return results