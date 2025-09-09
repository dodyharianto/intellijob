from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

root_folder = 'docs'
docs = os.listdir(root_folder)
print(docs)

all_chunks = []
documents = []
for doc in docs:
    file_path = os.path.join(root_folder, doc)
    pdf_loader = PyPDFLoader(file_path)
    document = pdf_loader.load()
    documents.append(document)

    splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ' '],
        chunk_size=500,
        chunk_overlap=20
    )
    chunks = splitter.split_documents(document)
    all_chunks.extend(chunks)


embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma.from_documents(
    documents=all_chunks,
    embedding=embeddings,
    persist_directory='intellijob_embedding_db'
)

print(f'Added {len(all_chunks)} chunks to vector database.')