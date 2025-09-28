from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from chromadb import PersistentClient
import os
from dotenv import load_dotenv
from memory import get_current_timestamp

load_dotenv()
embedding_dir = os.environ.get("EMBEDDING_DB_DIR")

def clear_collection(collection_name):
    client = PersistentClient(path=embedding_dir)
    collection = client.get_collection(name=collection_name)
    print(f'Found collection {collection_name}')

    document_ids = collection.get()['ids']
    if len(document_ids) > 0:
        collection.delete(ids=document_ids)
    print(f'Collection {collection_name} successfully cleared.')
    
def embed_documents(collection_name, root_folder='docs'):
    clear_collection(collection_name)
    docs = os.listdir(root_folder)
    print(docs)

    all_chunks = []
    for doc in docs:
        file_path = os.path.join(root_folder, doc)
        pdf_loader = PyPDFLoader(file_path)
        document = pdf_loader.load()

        splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n'],
            chunk_size=300,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(document)
        now = get_current_timestamp()
        for idx, chunk in enumerate(chunks):
            chunk.metadata.update({
                'chunk_id': idx,
                'creation_date': now.strftime('%Y-%m-%d %H:%M:%S'),
            })

        all_chunks.extend(chunks)

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vector_store = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=embedding_dir,
        collection_name=collection_name
    )

    print(f'Added {len(all_chunks)} chunks to vector database.')

def retrieve_chunks(collection_name, query, k=3):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=embedding_dir,
        collection_name=collection_name
    )

    results = vector_store.similarity_search(query, k=k)
    return results