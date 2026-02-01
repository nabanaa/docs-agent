import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=r"./db")
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name = "documents",
            embedding_function=self.ef
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100,
            length_function = len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def add_document(self, text:str, filename:str):

        chunks = self.text_splitter.split_text(text)

        ids = [f"{filename}_{i}" for i in range(len(chunks))]

        metadatas = [{"source": filename} for i in range(len(chunks))]

        self.collection.add(
            documents = chunks,
            metadatas = metadatas,
            ids = ids
        )

    def query_documents(self, query_text: str, n_results: int = 3):
        """Searches for most relevant text fragments"""
        result = self.collection.query(
            query_texts = [query_text],
            n_results = n_results
        )
        return result['documents'][0] if result['documents'] else []
    
    def query_with_metadata(self, query_text: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["documents", "metadatas"]
        )
        
        return {
            "documents": results['documents'][0] if results['documents'] else [],
            "metadatas": results['metadatas'][0] if results['metadatas'] else []
        }

rag_service = RAGService()