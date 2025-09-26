from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()
embedding_dir = os.environ.get("EMBEDDING_DB_DIR")

def embed_documents(root_folder='docs'):
    docs = os.listdir(root_folder)
    print(docs)

    all_chunks = []
    documents = []
    for doc in docs:
        file_path = os.path.join(root_folder, doc)
        pdf_loader = PyPDFLoader(file_path)
        document = pdf_loader.load()
        documents.extend(document)

        print(f'documents: {documents}')

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
        persist_directory=embedding_dir
    )

    print(f'Added {len(all_chunks)} chunks to vector database.')

def retrieve_chunks(query):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=embedding_dir
    )

    results = vector_store.similarity_search(query, k=3)
    return results

embed_documents('docs')