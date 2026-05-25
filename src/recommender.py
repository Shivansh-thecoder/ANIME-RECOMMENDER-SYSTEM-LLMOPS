from importlib import import_module
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt


class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):

        # Dynamically import RetrievalQA to avoid static analyzer import resolution errors in editors
        try:
            RetrievalQA = import_module("langchain.chains").RetrievalQA
        except Exception as e:
            raise ImportError(
                "Could not import RetrievalQA from langchain.chains. "
                "Ensure 'langchain' is installed in the active environment (pip install langchain) "
                "and VS Code is using the correct Python interpreter."
            ) from e

        self.llm = ChatGroq(
            api_key=api_key,
            model=model_name,
            temperature=0
        )

        self.prompt = get_anime_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def get_recommendation(self, query: str):
        result = self.qa_chain({"query": query})
        return result["result"]