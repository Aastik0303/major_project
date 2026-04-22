from typing import Generator
import re
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.schema import HumanMessage, Document
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st


class YouTubeRAGAgent:
    NAME = "YouTube RAG"
    ICON = "▶️"
    MODEL_TAG = "Gemini 2.5 + Transcript"

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash-preview-04-17"),
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=0.3,
            streaming=True,
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=st.secrets["GOOGLE_API_KEY"],
        )
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        self.vectorstore = None
        self.loaded_url = None

    def _extract_id(self, url: str) -> str:
        m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})", url)
        if m:
            return m.group(1)
        raise ValueError(f"Cannot extract video ID from: {url}")

    def ingest(self, url: str) -> str:
        vid = self._extract_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(vid)
        text = TextFormatter().format_transcript(transcript)
        doc = Document(page_content=text, metadata={"source": url})
        chunks = self.splitter.split_documents([doc])
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.loaded_url = url
        return f"✅ YouTube video loaded — {len(chunks)} transcript chunks indexed."

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        if not self.vectorstore:
            yield "⚠️ No video loaded. Paste a YouTube URL in the sidebar and click Load."
            return
        docs = self.vectorstore.similarity_search(message, k=5)
        context = "\n\n".join(d.page_content for d in docs)
        prompt = f"""You are analyzing a YouTube video transcript. Answer based on the content.

Transcript Context:
{context}

Question: {message}"""
        for chunk in self.llm.stream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content
