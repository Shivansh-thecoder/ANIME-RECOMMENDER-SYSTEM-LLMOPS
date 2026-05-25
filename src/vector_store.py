from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts):
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.model.encode(text)
        return embedding.tolist()


class VectorStoreBuilder:
    def __init__(
        self,
        csv_path: str,
        persist_dir: str = "chroma_db"
    ):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embedding = LocalEmbeddings()

    def build_and_store_vectorstore(self):

        loader = CSVLoader(
            file_path=self.csv_path,
            encoding="utf-8",
            metadata_columns=[]
        )

        data = loader.load()

        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )

        texts = splitter.split_documents(data)

        db = Chroma.from_documents(
            documents=texts,
            embedding=self.embedding,
            persist_directory=self.persist_dir
        )

        db.persist()

        return db

    def load_vectorstore(self):

        return Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedding
        )