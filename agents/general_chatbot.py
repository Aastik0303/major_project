from typing import Generator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import streamlit as st


class GeneralChatbotAgent:
    NAME = "General Chatbot"
    ICON = "🤖"
    MODEL_TAG = "Gemini 2.5 Flash"

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=0.7,
            streaming=True,
        )
        self.system = (
            "You are a brilliant, warm, and knowledgeable AI assistant. "
            "Respond thoughtfully and clearly. Use markdown formatting when helpful."
        )

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
