import chromadb
from llama_index.core import Document
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from opendevin import config
from . import json

embedding_strategy = config.get("LLM_EMBEDDING_MODEL")

# FIXME: Temporarily dropped support for other Embedding models
from llama_index.embeddings.openai import OpenAIEmbedding
embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=config.get_or_error("LLM_API_KEY")
)

class LongTermMemory:
    """
    Responsible for storing information that the agent can call on later for better insights and context.
    Uses chromadb to store and search through memories.
    """

    def __init__(self):
        """
        Initialize the chromadb and set up ChromaVectorStore for later use.
        """
        db = chromadb.Client()
        self.collection = db.get_or_create_collection(name="memories")
        vector_store = ChromaVectorStore(chroma_collection=self.collection)
        self.index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
        self.thought_idx = 0

    def add_event(self, event: dict):
        """
        Adds a new event to the long term memory with a unique id.

        Parameters:
        - event (dict): The new event to be added to memory
        """
        id = ""
        t = ""
        if "action" in event:
            t = "action"
            id = event["action"]
        elif "observation" in event:
            t = "observation"
            id = event["observation"]
        doc = Document(
            text=json.dumps(event),
            doc_id=str(self.thought_idx),
            extra_info={
                "type": t,
                "id": id,
                "idx": self.thought_idx,
            },
        )
        self.thought_idx += 1
        self.index.insert(doc)

    def search(self, query: str, k: int=10):
        """
        Searches through the current memory using VectorIndexRetriever

        Parameters:
        - query (str): A query to match search results to
        - k (int): Number of top results to return

        Returns:
        - List[str]: List of top k results found in current memory
        """
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=k,
        )
        results = retriever.retrieve(query)
        return [r.get_text() for r in results]


