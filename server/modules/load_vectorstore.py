# import os
# import time
# from pathlib import Path
# from dotenv import load_dotenv
# from tqdm.auto import tqdm
# from pinecone import Pinecone, ServerlessSpec
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings

# # Load environment variables
# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = "us-east-1"
# PINECONE_INDEX_NAME = "medical-index"

# UPLOAD_DIR = "./uploaded_pdfs"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Initialize Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)
# spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
# existing_indexes = [i["name"] for i in pc.list_indexes()]

# if PINECONE_INDEX_NAME not in existing_indexes:
#     pc.create_index(
#         name=PINECONE_INDEX_NAME,
#         dimension=384,  # all-MiniLM-L6-v2 output size
#         metric="dotproduct",
#         spec=spec
#     )
#     while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
#         time.sleep(1)

# index = pc.Index(PINECONE_INDEX_NAME)

# # Load, split, embed and upsert PDF content
# def load_vectorstore(uploaded_files):
#     embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     file_paths = []

#     for file in uploaded_files:
#         save_path = Path(UPLOAD_DIR) / file.filename
#         with open(save_path, "wb") as f:
#             f.write(file.file.read())
#         file_paths.append(str(save_path))

#     for file_path in file_paths:
#         loader = PyPDFLoader(file_path)
#         documents = loader.load()

#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         chunks = splitter.split_documents(documents)

#         texts = [chunk.page_content for chunk in chunks]
#         metadatas = [chunk.metadata for chunk in chunks]
#         ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

#         print(f"🔍 Embedding {len(texts)} chunks...")
#         embeddings = embed_model.embed_documents(texts)

#         # Build proper list of (id, vector, metadata) dicts for Pinecone
#         vectors = [
#             {"id": id_, "values": emb, "metadata": meta}
#             for id_, emb, meta in zip(ids, embeddings, metadatas)
#         ]

#         print("📤 Uploading to Pinecone...")
#         batch_size = 100
#         for i in tqdm(range(0, len(vectors), batch_size), desc="Upserting to Pinecone"):
#             batch = vectors[i : i + batch_size]
#             index.upsert(vectors=batch)

#         print(f"✅ Upload complete for {file_path}")




import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PERSIST_DIR = "./chroma_store"
UPLOAD_DIR = "./uploaded_pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_vectorstore(uploaded_files):

    file_paths = []

    for file in uploaded_files:

        save_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(str(save_path))

    docs = []

    for path in file_paths:
        loader = PyPDFLoader(path)
        documents = loader.load()
        docs.extend(documents)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    embed_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):

        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embed_model
        )

        vectorstore.add_documents(split_docs)
        vectorstore.persist()

    else:

        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embed_model,
            persist_directory=PERSIST_DIR
        )

    vectorstore.persist()

    return vectorstore