from typing import Generator
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st


class DeepResearcherAgent:
    NAME = "Deep Researcher"
    ICON = "🔬"
    MODEL_TAG = "Gemini 2.5 + Web"

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash-preview-04-17"),
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=0.4,
            streaming=True,
        )
        self.system = """You are an expert research analyst.
Synthesize web sources into a comprehensive, well-structured markdown report.
Always cite sources, highlight key insights, and be thorough yet concise."""

    def _search(self, query: str, n: int = 5) -> list:
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=n))
        except Exception:
            return []

    def _scrape(self, url: str) -> str:
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
            soup = BeautifulSoup(r.text, "html.parser")
            for t in soup(["script", "style", "nav", "header", "footer"]):
                t.decompose()
            return soup.get_text(separator=" ", strip=True)[:2500]
        except Exception:
            return ""

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        yield f"🔍 **Researching:** {message}\n\n"
        yield "📡 Searching the web...\n\n"

        results = self._search(message)
        if not results:
            yield "❌ No results found. Try rephrasing your query."
            return

        yield f"✅ Found **{len(results)} sources** — scraping content...\n\n"

        scraped = []
        for i, r in enumerate(results[:4], 1):
            url = r.get("href", "")
            title = r.get("title", "Unknown")
            snippet = r.get("body", "")
            yield f"📄 Reading source {i}: *{title[:60]}*\n"
            content = self._scrape(url) or snippet
            scraped.append({"title": title, "url": url, "content": content})

        yield "\n---\n\n🧠 **Synthesizing research report...**\n\n"

        sources_block = "\n\n".join(
            f"**Source {i+1}**: {s['title']}\n**URL**: {s['url']}\n**Content**: {s['content']}"
            for i, s in enumerate(scraped)
        )

        prompt = f"""Research Query: {message}

Web Sources:
{sources_block}

Write a comprehensive research report with these sections:
## Executive Summary
## Key Findings
## Detailed Analysis
## Sources & References
## Conclusion"""

        for chunk in self.llm.stream([
            SystemMessage(content=self.system),
            HumanMessage(content=prompt),
        ]):
            if chunk.content:
                yield chunk.content
