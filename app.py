import streamlit as st
import uuid
import time
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuralNexus · AI Platform",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sky Theme CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root & Reset ── */
:root {
  --sky-void:   #030d1a;
  --sky-deep:   #06111f;
  --sky-card:   #0a1c35;
  --sky-panel:  #0d2040;
  --sky-border: #1a3a60;
  --sky-bright: #1e4a78;
  --cyan:       #38bdf8;
  --cyan-dim:   #0ea5e9;
  --cyan-glow:  rgba(56,189,248,0.15);
  --violet:     #818cf8;
  --violet-dim: #6366f1;
  --pink:       #f472b6;
  --green:      #34d399;
  --yellow:     #fbbf24;
  --red:        #f87171;
  --text-1:     #e2e8f0;
  --text-2:     #94a3b8;
  --text-3:     #475569;
  --font-hd:    'Orbitron', monospace;
  --font-body:  'Space Grotesk', sans-serif;
  --font-mono:  'JetBrains Mono', monospace;
}

/* Root backgrounds */
.stApp { background: var(--sky-void) !important; font-family: var(--font-body); }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060f1e 0%, #08162b 100%) !important;
  border-right: 1px solid var(--sky-border) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--sky-deep); }
::-webkit-scrollbar-thumb { background: var(--sky-bright); border-radius: 3px; }

/* ── Header bar ── */
.nn-header {
  background: linear-gradient(135deg, rgba(6,17,31,0.95), rgba(10,28,53,0.95));
  border-bottom: 1px solid var(--sky-border);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  gap: 14px;
  margin: -1rem -1rem 1.5rem -1rem;
  backdrop-filter: blur(20px);
}
.nn-logo {
  width: 42px; height: 42px; border-radius: 10px;
  background: linear-gradient(135deg, var(--cyan), var(--violet));
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 900; color: white;
  box-shadow: 0 0 20px rgba(56,189,248,0.5);
  flex-shrink: 0;
}
.nn-title {
  font-family: var(--font-hd);
  font-size: 18px; font-weight: 900; letter-spacing: 0.1em;
  background: linear-gradient(90deg, var(--cyan), var(--violet));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nn-sub {
  font-size: 10px; color: var(--text-3);
  font-family: var(--font-mono); letter-spacing: 0.2em; margin-top: 2px;
}
.nn-badge {
  padding: 3px 10px; border-radius: 20px; font-size: 10px;
  font-family: var(--font-mono); letter-spacing: 0.05em;
  border: 1px solid; margin-left: auto;
}
.nn-badge-cyan { border-color: var(--cyan); color: var(--cyan); background: rgba(56,189,248,0.07); }
.nn-badge-violet { border-color: var(--violet); color: var(--violet); background: rgba(129,140,248,0.07); }

/* ── Sidebar sections ── */
.sidebar-section {
  background: rgba(10,28,53,0.6);
  border: 1px solid var(--sky-border);
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 10px;
}
.sidebar-label {
  font-family: var(--font-mono); font-size: 9px;
  color: var(--text-3); letter-spacing: 0.2em;
  text-transform: uppercase; margin-bottom: 8px;
}
.chat-item {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 10px; border-radius: 8px; cursor: pointer;
  font-size: 12px; color: var(--text-2);
  border: 1px solid transparent;
  transition: all 0.15s;
  margin-bottom: 4px;
}
.chat-item:hover { background: rgba(56,189,248,0.08); border-color: var(--sky-bright); }
.chat-item.active {
  background: rgba(56,189,248,0.12); border-color: var(--cyan-dim);
  color: var(--cyan);
}
.chat-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--cyan); flex-shrink: 0;
  box-shadow: 0 0 6px var(--cyan);
}

/* ── Agent pill selector ── */
.agent-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.agent-pill {
  padding: 6px 12px; border-radius: 20px; font-size: 11px;
  border: 1px solid var(--sky-border); color: var(--text-2);
  background: transparent; cursor: pointer;
  font-family: var(--font-body); transition: all 0.15s;
}
.agent-pill:hover { border-color: var(--cyan); color: var(--cyan); }
.agent-pill.active {
  background: rgba(56,189,248,0.12);
  border-color: var(--cyan); color: var(--cyan);
}

/* ── Chat messages ── */
.msg-wrapper { animation: fadeSlideIn 0.3s ease; margin-bottom: 16px; }
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.msg-user {
  display: flex; justify-content: flex-end;
}
.msg-user-bubble {
  max-width: 72%; padding: 12px 16px;
  background: linear-gradient(135deg, rgba(129,140,248,0.2), rgba(56,189,248,0.12));
  border: 1px solid rgba(56,189,248,0.25);
  border-radius: 18px 18px 4px 18px;
  color: var(--text-1); font-size: 14px; line-height: 1.6;
}
.msg-ai { display: flex; gap: 12px; align-items: flex-start; }
.msg-avatar {
  width: 34px; height: 34px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0; margin-top: 2px;
}
.msg-agent-label {
  font-family: var(--font-mono); font-size: 9px;
  letter-spacing: 0.15em; margin-bottom: 5px;
  display: flex; align-items: center; gap: 5px;
}
.msg-dot {
  width: 5px; height: 5px; border-radius: 50%; display: inline-block;
}
.msg-ai-bubble {
  background: var(--sky-card); border: 1px solid var(--sky-border);
  border-radius: 4px 18px 18px 18px;
  padding: 14px 18px; font-size: 14px; line-height: 1.75;
  color: var(--text-1); flex: 1;
}
.msg-ai-bubble code {
  background: rgba(56,189,248,0.08); padding: 2px 6px;
  border-radius: 4px; font-family: var(--font-mono);
  font-size: 12px; color: var(--cyan);
}
.msg-ai-bubble pre {
  background: #020d1a; border: 1px solid var(--sky-border);
  border-radius: 8px; padding: 14px; overflow-x: auto;
  margin: 10px 0;
}
.msg-ai-bubble pre code { background: none; padding: 0; color: var(--text-1); }
.msg-ai-bubble table { border-collapse: collapse; width: 100%; margin: 10px 0; }
.msg-ai-bubble th {
  padding: 8px 12px; border-bottom: 1px solid var(--sky-bright);
  color: var(--cyan); font-family: var(--font-mono); font-size: 11px;
  text-align: left;
}
.msg-ai-bubble td { padding: 8px 12px; border-bottom: 1px solid var(--sky-border); color: var(--text-2); }
.msg-ai-bubble h1,h2,h3 { color: white; }
.msg-ai-bubble h2 { color: var(--cyan); font-size: 15px; margin: 14px 0 6px; }
.msg-ai-bubble h3 { color: var(--violet); font-size: 13px; margin: 10px 0 4px; }
.msg-ai-bubble a { color: var(--cyan); }
.msg-ai-bubble blockquote {
  border-left: 3px solid var(--violet);
  padding-left: 12px; color: var(--text-2); margin: 8px 0;
}
/* Latency shimmer on streaming */
.streaming-cursor {
  display: inline-block; width: 2px; height: 16px;
  background: var(--cyan); margin-left: 3px; vertical-align: middle;
  animation: blink 0.7s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* ── Input area ── */
.input-area {
  background: rgba(6,17,31,0.9); border-top: 1px solid var(--sky-border);
  padding: 14px 20px; margin: 0 -1rem -1rem;
  backdrop-filter: blur(20px);
}
.agent-routing-bar {
  font-family: var(--font-mono); font-size: 11px;
  margin-bottom: 8px; padding: 6px 12px;
  background: rgba(56,189,248,0.06);
  border: 1px solid rgba(56,189,248,0.2); border-radius: 6px;
  display: flex; align-items: center; gap: 6px;
}

/* ── Stat cards ── */
.stat-card {
  background: var(--sky-card); border: 1px solid var(--sky-border);
  border-radius: 10px; padding: 14px 16px;
  border-left-width: 3px; border-left-style: solid;
}
.stat-label { font-size: 9px; color: var(--text-3); letter-spacing: 0.15em; margin-bottom: 6px; }
.stat-value { font-size: 22px; font-weight: 700; font-family: var(--font-mono); }

/* ── Tab headers ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--sky-border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-3) !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  padding: 12px 24px !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
  color: var(--cyan) !important;
  border-bottom-color: var(--cyan) !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(129,140,248,0.15)) !important;
  border: 1px solid var(--sky-border) !important;
  color: var(--text-1) !important;
  font-family: var(--font-body) !important;
  border-radius: 8px !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  border-color: var(--cyan) !important;
  color: var(--cyan) !important;
  box-shadow: 0 0 12px rgba(56,189,248,0.2) !important;
}

/* ── Select/text inputs ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: var(--sky-panel) !important;
  border-color: var(--sky-border) !important;
  color: var(--text-1) !important;
  font-family: var(--font-body) !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 1px var(--cyan) !important;
}

/* ── Upload area ── */
.stFileUploader > div {
  background: var(--sky-panel) !important;
  border: 2px dashed var(--sky-bright) !important;
  border-radius: 10px !important;
}
.stFileUploader > div:hover { border-color: var(--cyan) !important; }

/* ── Chat input ── */
.stChatInput > div {
  background: var(--sky-panel) !important;
  border: 1px solid var(--sky-border) !important;
  border-radius: 12px !important;
}
.stChatInput > div:focus-within { border-color: var(--cyan) !important; }
.stChatInput input { color: var(--text-1) !important; }

/* ── Progress / spinner ── */
.stProgress > div > div { background: linear-gradient(90deg, var(--cyan), var(--violet)) !important; }

/* ── Metric ── */
[data-testid="metric-container"] {
  background: var(--sky-card) !important;
  border: 1px solid var(--sky-border) !important;
  border-radius: 10px !important; padding: 14px !important;
}
[data-testid="metric-container"] label { color: var(--text-3) !important; font-size: 11px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--cyan) !important; }

/* ── Dividers ── */
hr { border-color: var(--sky-border) !important; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Imports (deferred so secrets load first) ────────────────────────────────────
from agents import (GeneralChatbotAgent, CodeAgent,
                    DocumentRAGAgent, YouTubeRAGAgent, DeepResearcherAgent)
from orchestrator import route
import data_analysis as da

# ── Constants ──────────────────────────────────────────────────────────────────
AGENTS_META = {
    "auto":       {"name": "Auto Route",      "icon": "⚡", "color": "#38bdf8", "desc": "LangGraph Orchestrator"},
    "general":    {"name": "General Chatbot", "icon": "🤖", "color": "#38bdf8", "desc": "Gemini 2.5 Flash"},
    "code":       {"name": "Code Agent",      "icon": "💻", "color": "#818cf8", "desc": "Groq Llama 3.3 70B"},
    "document":   {"name": "Document RAG",    "icon": "📄", "color": "#34d399", "desc": "Gemini + FAISS"},
    "youtube":    {"name": "YouTube RAG",     "icon": "▶️", "color": "#f472b6", "desc": "Transcript + RAG"},
    "researcher": {"name": "Deep Researcher", "icon": "🔬", "color": "#fbbf24", "desc": "Web + Synthesis"},
}

# ── Session state init ─────────────────────────────────────────────────────────
def init_state():
    if "chats" not in st.session_state:
        cid = str(uuid.uuid4())[:8]
        st.session_state.chats = {
            cid: {"title": "Chat 1", "messages": [], "created": datetime.now()}
        }
        st.session_state.active_chat = cid

    if "agent_instances" not in st.session_state:
        st.session_state.agent_instances = {
            "general":    GeneralChatbotAgent(),
            "code":       CodeAgent(),
            "document":   DocumentRAGAgent(),
            "youtube":    YouTubeRAGAgent(),
            "researcher": DeepResearcherAgent(),
        }
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = "auto"
    if "data_df" not in st.session_state:
        st.session_state.data_df = None
    if "data_eda" not in st.session_state:
        st.session_state.data_eda = None
    if "last_agent_used" not in st.session_state:
        st.session_state.last_agent_used = None

init_state()

# ── Helper: get active messages ────────────────────────────────────────────────
def active_msgs():
    return st.session_state.chats[st.session_state.active_chat]["messages"]

def add_msg(role, content, agent=None):
    active_msgs().append({"role": role, "content": content, "agent": agent, "ts": datetime.now()})

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:18px 4px 12px; text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;border-radius:9px;
                    background:linear-gradient(135deg,#38bdf8,#818cf8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;font-weight:900;color:white;
                    box-shadow:0 0 16px rgba(56,189,248,0.5);">N</div>
        <div>
          <div style="font-family:'Orbitron',monospace;font-size:13px;font-weight:900;
                      background:linear-gradient(90deg,#38bdf8,#818cf8);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                      letter-spacing:0.1em;">NEURALNEXUS</div>
          <div style="font-size:9px;color:#475569;letter-spacing:0.15em;
                      font-family:'JetBrains Mono',monospace;">AI PLATFORM</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Chat memory management ──────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">💬 CHAT SESSIONS</div>', unsafe_allow_html=True)

    # New chat button
    if st.button("＋  New Chat", use_container_width=True):
        cid = str(uuid.uuid4())[:8]
        n = len(st.session_state.chats) + 1
        st.session_state.chats[cid] = {
            "title": f"Chat {n}",
            "messages": [],
            "created": datetime.now(),
        }
        st.session_state.active_chat = cid
        st.rerun()

    # Chat list
    for cid, chat in list(st.session_state.chats.items()):
        is_active = cid == st.session_state.active_chat
        msgs = chat["messages"]
        preview = msgs[-1]["content"][:28] + "…" if msgs else "Empty"
        label = f"{'●' if is_active else '○'}  {chat['title']}"

        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(label, key=f"chat_{cid}", use_container_width=True,
                         help=preview):
                st.session_state.active_chat = cid
                st.rerun()
        with col2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑", key=f"del_{cid}", help="Delete chat"):
                    del st.session_state.chats[cid]
                    if st.session_state.active_chat == cid:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()

    # ── Agent selector ──────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">🤖 AGENT</div>', unsafe_allow_html=True)

    agent_options = list(AGENTS_META.keys())
    agent_labels  = [f"{AGENTS_META[a]['icon']} {AGENTS_META[a]['name']}" for a in agent_options]

    sel_idx = agent_options.index(st.session_state.selected_agent)
    chosen  = st.selectbox("Select Agent", agent_labels, index=sel_idx, label_visibility="collapsed")
    st.session_state.selected_agent = agent_options[agent_labels.index(chosen)]

    meta = AGENTS_META[st.session_state.selected_agent]
    st.markdown(f"""
    <div style="font-size:10px;color:{meta['color']};font-family:'JetBrains Mono',monospace;
                margin-top:4px;padding:4px 8px;background:rgba(56,189,248,0.05);
                border-radius:6px;border:1px solid {meta['color']}30;">
      {meta['icon']} {meta['desc']}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Document upload (for Document RAG) ─────────────────────────────────────
    st.markdown('<div class="sidebar-label">📎 DOCUMENT RAG</div>', unsafe_allow_html=True)
    doc_file = st.file_uploader("Upload PDF / TXT / DOCX",
                                 type=["pdf", "txt", "docx"],
                                 label_visibility="collapsed")
    if doc_file:
        with st.spinner("Indexing document..."):
            msg = st.session_state.agent_instances["document"].ingest(doc_file)
        st.success(msg)
        add_msg("assistant", msg, "document")

    st.divider()

    # ── YouTube loader ──────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">▶️ YOUTUBE RAG</div>', unsafe_allow_html=True)
    yt_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...",
                            label_visibility="collapsed")
    if st.button("Load Video", use_container_width=True) and yt_url:
        with st.spinner("Fetching transcript..."):
            try:
                msg = st.session_state.agent_instances["youtube"].ingest(yt_url)
                st.success(msg)
                add_msg("assistant", msg, "youtube")
            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()

    # ── Clear current chat ──────────────────────────────────────────────────────
    if st.button("🧹  Clear Current Chat", use_container_width=True):
        st.session_state.chats[st.session_state.active_chat]["messages"] = []
        st.rerun()

# ── Main header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nn-header">
  <div class="nn-logo">N</div>
  <div>
    <div class="nn-title">NEURALNEXUS</div>
    <div class="nn-sub">MULTI-AGENT AI PLATFORM · LANGCHAIN + LANGGRAPH</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:8px;align-items:center;">
    <span class="nn-badge nn-badge-cyan">Gemini 2.5 Flash</span>
    <span class="nn-badge nn-badge-violet">Groq Llama 3.3</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────────────────
tab_chat, tab_data = st.tabs(["◈  Multi-Agent Chat", "◇  Data Analysis"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MULTI-AGENT CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab_chat:
    messages = active_msgs()
    chat_title = st.session_state.chats[st.session_state.active_chat]["title"]

    # Welcome if empty
    if not messages:
        st.markdown(f"""
        <div style="text-align:center;padding:48px 20px;">
          <div style="font-size:48px;margin-bottom:16px;">🌌</div>
          <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;
                      background:linear-gradient(90deg,#38bdf8,#818cf8);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                      margin-bottom:8px;">
            Welcome to NeuralNexus
          </div>
          <div style="color:#94a3b8;font-size:13px;max-width:480px;margin:0 auto;line-height:1.7;">
            5 specialized AI agents, auto-routed by LangGraph.<br>
            Select an agent in the sidebar or let <strong style="color:#38bdf8;">Auto Route</strong> decide.
          </div>
          <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:24px;">
            {"".join(f'<span style="padding:5px 14px;border-radius:20px;font-size:11px;border:1px solid {m["color"]}30;color:{m["color"]};background:{m["color"]}10;">{m["icon"]} {m["name"]}</span>' for k,m in AGENTS_META.items() if k!="auto")}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Render messages ─────────────────────────────────────────────────────────
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-wrapper msg-user">
              <div class="msg-user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            agent_key = msg.get("agent") or "general"
            if agent_key not in AGENTS_META:
                agent_key = "general"
            m = AGENTS_META[agent_key]
            st.markdown(f"""
            <div class="msg-wrapper msg-ai">
              <div class="msg-avatar"
                   style="background:{m['color']}18;border:1px solid {m['color']}35;">
                {m['icon']}
              </div>
              <div style="flex:1;min-width:0;">
                <div class="msg-agent-label" style="color:{m['color']};">
                  <span class="msg-dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
                  {m['name'].upper()} · {m['desc']}
                </div>
                <div class="msg-ai-bubble">{msg["content"]}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Chat input ──────────────────────────────────────────────────────────────
    sel_agent = st.session_state.selected_agent
    placeholder = (
        f"Message {AGENTS_META[sel_agent]['name']}..."
        if sel_agent != "auto"
        else "Message NeuralNexus... (auto-routes to best agent)"
    )

    if prompt := st.chat_input(placeholder):
        # Save user message
        add_msg("user", prompt)

        # Auto-title the chat from first message
        chat = st.session_state.chats[st.session_state.active_chat]
        if len(chat["messages"]) == 1:
            chat["title"] = prompt[:22] + ("…" if len(prompt) > 22 else "")

        # Route to agent
        agent_key = route(prompt, sel_agent if sel_agent != "auto" else None)
        st.session_state.last_agent_used = agent_key
        agent = st.session_state.agent_instances[agent_key]
        m = AGENTS_META[agent_key]

        # Stream response
        history = [{"role": h["role"], "content": h["content"]}
                   for h in active_msgs()[:-1]]

        with st.spinner(f"{m['icon']} {m['name']} is thinking..."):
            placeholder_el = st.empty()
            full_response = ""
            for chunk in agent.stream(prompt, history):
                full_response += chunk
                # Show with streaming cursor
                placeholder_el.markdown(f"""
                <div class="msg-wrapper msg-ai">
                  <div class="msg-avatar"
                       style="background:{m['color']}18;border:1px solid {m['color']}35;">
                    {m['icon']}
                  </div>
                  <div style="flex:1;min-width:0;">
                    <div class="msg-agent-label" style="color:{m['color']};">
                      <span class="msg-dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
                      {m['name'].upper()} · Streaming...
                    </div>
                    <div class="msg-ai-bubble">{full_response}<span class="streaming-cursor"></span></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            placeholder_el.empty()

        # Save final response
        add_msg("assistant", full_response, agent_key)
        st.rerun()

    # ── Status bar ─────────────────────────────────────────────────────────────
    last = st.session_state.last_agent_used
    if last:
        m = AGENTS_META[last]
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:{m['color']};text-align:center;padding:6px;
                    border-top:1px solid #1a3a60;margin-top:4px;">
          ENTER to send · SHIFT+ENTER for new line · Last routed → {m['icon']} {m['name']} · Session: {st.session_state.active_chat}
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#38bdf8;
                letter-spacing:0.12em;margin-bottom:16px;">
      ◇ DATA ANALYSIS · EDA &amp; VISUALIZATION
    </div>
    """, unsafe_allow_html=True)

    # Upload
    data_file = st.file_uploader("Upload CSV / TSV / XLSX",
                                  type=["csv", "tsv", "xlsx"],
                                  key="data_upload")
    if data_file:
        with st.spinner("Parsing dataset..."):
            try:
                st.session_state.data_df  = da.load_df(data_file)
                st.session_state.data_eda = da.get_eda(st.session_state.data_df)
                st.success(f"✅ Loaded **{data_file.name}** — "
                           f"{st.session_state.data_df.shape[0]:,} rows × "
                           f"{st.session_state.data_df.shape[1]} columns")
            except Exception as e:
                st.error(f"Failed to parse: {e}")

    df  = st.session_state.data_df
    eda = st.session_state.data_eda

    if df is not None:
        # ── Stat cards ────────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        cards = [
            (c1, "ROWS",       f"{df.shape[0]:,}",              "#38bdf8"),
            (c2, "COLUMNS",    str(df.shape[1]),                 "#818cf8"),
            (c3, "NUMERIC",    str(len(eda["num_cols"])),        "#34d399"),
            (c4, "MISSING",    str(sum(eda["nulls"].values())),  "#fbbf24"),
            (c5, "DUPLICATES", str(eda["duplicates"]),           "#f472b6"),
        ]
        for col, label, val, color in cards:
            with col:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color:{color};">
                  <div class="stat-label">{label}</div>
                  <div class="stat-value" style="color:{color};">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Sub-tabs ──────────────────────────────────────────────────────────
        dtab1, dtab2, dtab3 = st.tabs(["📋  Preview", "📈  EDA Stats", "🎨  Visualize"])

        # PREVIEW
        with dtab1:
            st.markdown(f"<div style='color:#475569;font-size:11px;margin-bottom:8px;'>"
                        f"Showing first 50 of {df.shape[0]:,} rows · Memory: {eda['memory']}</div>",
                        unsafe_allow_html=True)
            st.dataframe(
                df.head(50),
                use_container_width=True,
                height=400,
            )

        # EDA STATS
        with dtab2:
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**Null Values per Column**")
                nulls_df = (
                    df.isnull().sum().reset_index()
                    .rename(columns={"index": "Column", 0: "Nulls"})
                    .sort_values("Nulls", ascending=False)
                )
                st.dataframe(nulls_df, use_container_width=True, height=280)

            with col_b:
                st.markdown("**Column Data Types**")
                dtypes_df = df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"})
                dtypes_df["Type"] = dtypes_df["Type"].astype(str)
                st.dataframe(dtypes_df, use_container_width=True, height=280)

            if eda["corr"] is not None:
                st.markdown("**Correlation Matrix**")
                st.dataframe(eda["corr"], use_container_width=True, height=260)

            st.markdown("**Descriptive Statistics**")
            st.dataframe(df.describe(include="all").fillna(""),
                         use_container_width=True, height=260)

        # VISUALIZE
        with dtab3:
            all_cols = df.columns.tolist()
            num_cols = eda["num_cols"]
            cat_cols = eda["cat_cols"]

            PLOT_TYPES = ["Histogram", "Scatter", "Box Plot",
                          "Correlation Heatmap", "Bar Chart", "Line Chart", "Violin"]

            vc1, vc2, vc3, vc4 = st.columns([2, 2, 2, 1])
            with vc1:
                plot_type = st.selectbox("Plot Type", PLOT_TYPES)
            with vc2:
                x_col = st.selectbox("X Axis", ["—"] + all_cols) if plot_type not in ["Box Plot", "Violin", "Correlation Heatmap"] else "—"
            with vc3:
                y_col = st.selectbox("Y Axis", ["—"] + num_cols) if plot_type in ["Scatter", "Bar Chart", "Line Chart"] else "—"
            with vc4:
                hue_col = st.selectbox("Color By", ["—"] + cat_cols) if plot_type == "Scatter" else "—"

            if st.button("◇  Generate Plot", use_container_width=False):
                with st.spinner("Rendering visualization..."):
                    try:
                        img = da.make_plot(
                            df, plot_type,
                            x_col=x_col if x_col != "—" else None,
                            y_col=y_col if y_col != "—" else None,
                            hue_col=hue_col if hue_col != "—" else None,
                        )
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Plot error: {e}")
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#475569;">
          <div style="font-size:60px;margin-bottom:16px;opacity:0.3;">◇</div>
          <div style="font-family:'Orbitron',monospace;font-size:14px;letter-spacing:0.1em;">
            NO DATASET LOADED
          </div>
          <div style="font-size:12px;margin-top:8px;">
            Upload a CSV, TSV, or Excel file above to begin analysis
          </div>
        </div>
        """, unsafe_allow_html=True)
