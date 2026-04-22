from typing import Generator
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import streamlit as st


class CodeAgent:
    NAME = "Code Agent"
    ICON = "💻"
    MODEL_TAG = "Groq Llama 3.3 70B"

    def __init__(self):
        self.llm = ChatGroq(
            model=st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
            groq_api_key=st.secrets["GROQ_API_KEY"],
            temperature=0.1,
            streaming=True,
        )
        self.system = """You are an elite software engineer and debugging expert.
- Write clean, efficient, well-documented code in any language
- Debug issues with precise step-by-step explanations
- Always use proper markdown code blocks with language tags
- Suggest optimizations and best practices
Think carefully before writing any code."""

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        msgs = [SystemMessage(content=self.system)]
        for h in history[-12:]:
            if h["role"] == "user":
                msgs.append(HumanMessage(content=h["content"]))
            else:
                msgs.append(AIMessage(content=h["content"]))
        msgs.append(HumanMessage(content=message))
        for chunk in self.llm.stream(msgs):
            if chunk.content:
                yield chunk.content
