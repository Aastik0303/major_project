from typing import Generator
import os, tempfile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
import streamlit as st

try:
    import docx2txt
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class DocumentRAGAgent:
    NAME = "Document RAG"
    ICON = "📄"
    MODEL_TAG = "Gemini 2.5 + FAISS"

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=0.2,
            streaming=True,
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=st.secrets["GOOGLE_API_KEY"],
        )
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vectorstore = None

    def ingest(self, uploaded_file) -> str:
        suffix = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(uploaded_file.read())
            tmp = f.name
        try:
            if suffix == ".pdf":
                docs = PyPDFLoader(tmp).load()
            elif suffix == ".docx" and HAS_DOCX:
                text = docx2txt.process(tmp)
                docs = [Document(page_content=text, metadata={"source": uploaded_file.name})]
            else:
                docs = TextLoader(tmp).load()
            chunks = self.splitter.split_documents(docs)
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
            else:
                self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            return f"✅ **{uploaded_file.name}** ingested — {len(chunks)} chunks indexed."
        finally:
            os.unlink(tmp)

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        if not self.vectorstore:
            yield "⚠️ No documents loaded yet. Upload a PDF, TXT, or DOCX in the sidebar."
            return
        docs = self.vectorstore.similarity_search(message, k=4)
        context = "\n\n".join(d.page_content for d in docs)
        prompt = f"""Answer based only on the document context below.
If the answer isn't there, say so clearly.

Context:
{context}

Question: {message}"""
        for chunk in self.llm.stream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content
