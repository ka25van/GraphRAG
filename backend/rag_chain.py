from langchain_community.llms.ollama import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from pydantic import Field
from typing import List
from graph_builder import query_graph
from utils import extract_text_from_pdf, extract_entities

class SimpleRetriever(BaseRetriever):
    docs: List[Document] = Field(default_factory=list)

    def _get_relevant_documents(self, query: str):
        return self.docs

    async def _aget_relevant_documents(self, query: str):
        return self._get_relevant_documents(query)

def answer_question(query: str):
    entities = extract_entities(query)
    print("Received query:", entities)
    docs = query_graph(entities)
    embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")
    docsearch = FAISS.from_documents(docs, embedding)

    
    retriever = SimpleRetriever(docs=docs)
    
    llm = Ollama(model="llama3.2:latest")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain.run(query)
