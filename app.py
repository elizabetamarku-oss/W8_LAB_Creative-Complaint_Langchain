import os
import random
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

# ── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Downside-Up Complaint Bureau",
    page_icon="🙃",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet"/>
<style>

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
.main .block-container {
    background-color: #050505 !important;
    color: #d4b896 !important;
    max-width: 780px !important;
    padding-top: 0 !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    background: transparent !important;
    display: none !important;
}
section[data-testid="stSidebar"] { display: none !important; }
footer { display: none !important; }

/* ── Hero banner ── */
.hero {
    position: relative;
    width: 100%;
    min-height: 260px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem 1rem 2rem;
    overflow: hidden;
    margin-bottom: 0;
}
.hero-bg {
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% 40%, rgba(120,10,10,0.55) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 30% 70%, rgba(80,5,5,0.4) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 70% 20%, rgba(60,0,0,0.35) 0%, transparent 60%),
        linear-gradient(180deg, #0a0000 0%, #050505 100%);
    z-index: 0;
}
/* floating vine/particle specks */
.hero-bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle 1px at 15% 25%, rgba(200,30,30,0.6) 0%, transparent 100%),
        radial-gradient(circle 1px at 42% 60%, rgba(200,30,30,0.4) 0%, transparent 100%),
        radial-gradient(circle 2px at 68% 35%, rgba(200,30,30,0.5) 0%, transparent 100%),
        radial-gradient(circle 1px at 85% 70%, rgba(200,30,30,0.35) 0%, transparent 100%),
        radial-gradient(circle 1px at 25% 80%, rgba(200,30,30,0.4) 0%, transparent 100%),
        radial-gradient(circle 2px at 55% 15%, rgba(200,30,30,0.45) 0%, transparent 100%);
}
.hero-content { position: relative; z-index: 1; text-align: center; width: 100%; }

.hero-rule {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #cc1a18 25%, #ff4040 50%, #cc1a18 75%, transparent 100%);
    box-shadow: 0 0 12px #cc1a18, 0 0 30px rgba(200,25,25,0.4);
    margin: 0.5rem auto;
    width: 65%;
}
.hero-eyebrow {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.5em;
    color: #803030;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(2.8rem, 10vw, 5.5rem);
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #cc1a18;
    text-shadow:
        0 0 7px #ff2020,
        0 0 20px #cc1a18,
        0 0 50px #880000,
        0 0 90px rgba(100,0,0,0.6);
    line-height: 1;
    margin: 0;
    animation: flicker 7s infinite;
}
.hero-title span {
    color: #ff3030;
    text-shadow:
        0 0 5px #ff5050,
        0 0 15px #ff2020,
        0 0 40px #cc0000,
        0 0 80px rgba(150,0,0,0.7);
}
.hero-sub {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(0.6rem, 2vw, 0.85rem);
    letter-spacing: 0.45em;
    color: #7a3535;
    text-shadow: 0 0 10px rgba(180,40,40,0.5);
    margin-top: 0.5rem;
    text-transform: uppercase;
}

/* mist at bottom of hero */
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60px;
    background: linear-gradient(0deg, #050505 0%, transparent 100%);
    z-index: 2;
}

/* ── Section label ── */
.section-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    color: #602020;
    text-transform: uppercase;
    margin: 1.8rem 0 0.5rem;
    padding-left: 0.2rem;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: #0a0000 !important;
    border: 1px solid #3a0a0a !important;
    border-radius: 2px !important;
    color: #d4b896 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    caret-color: #cc1a18;
    box-shadow: inset 0 0 20px rgba(100,5,5,0.2) !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #880000 !important;
    box-shadow: inset 0 0 20px rgba(150,10,10,0.25), 0 0 15px rgba(180,20,20,0.2) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #3a1a1a !important; }
label[data-testid="stWidgetLabel"] { display: none !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #660000 !important;
    color: #cc1a18 !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.35em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.2rem !important;
    border-radius: 2px !important;
    box-shadow: 0 0 8px rgba(180,20,20,0.2) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(150,10,10,0.15) !important;
    border-color: #cc1a18 !important;
    box-shadow: 0 0 18px rgba(200,25,25,0.45), inset 0 0 10px rgba(180,20,20,0.1) !important;
    color: #ff5050 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #2a0808, transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ── Tool steps ── */
.steps-wrap { margin: 1rem 0 0.5rem; }
.step-row {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #160505;
}
.step-icon {
    font-size: 0.7rem;
    color: #601010;
    font-family: 'Share Tech Mono', monospace;
    white-space: nowrap;
    padding-top: 2px;
    min-width: 28px;
}
.step-body { flex: 1; }
.step-name {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #992020;
    margin-bottom: 2px;
}
.step-result {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: #4a2a2a;
    line-height: 1.4;
}

/* ── Response card ── */
.response-card {
    margin-top: 1.2rem;
    border: 1px solid #3a0a0a;
    border-left: 3px solid #cc1a18;
    background: linear-gradient(135deg, #0a0000 0%, #060000 100%);
    padding: 1.4rem 1.6rem;
    border-radius: 2px;
    box-shadow: 0 0 30px rgba(150,10,10,0.12), inset 0 0 40px rgba(80,0,0,0.08);
    position: relative;
    overflow: hidden;
}
.response-card::before {
    content: 'CLASSIFIED TRANSMISSION';
    position: absolute;
    top: 0.5rem; right: 0.8rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.3em;
    color: #2a0808;
}
.response-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #c8a880;
    white-space: pre-wrap;
}

/* ── History ── */
.history-wrap { margin-top: 0.5rem; }
.history-card {
    padding: 0.9rem 0;
    border-bottom: 1px solid #160505;
    position: relative;
}
.history-q {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: #602020;
    margin-bottom: 0.3rem;
}
.history-a {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #5a3535;
    line-height: 1.5;
}
.history-tools {
    margin-top: 0.3rem;
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}
.history-badge {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    color: #441818;
    border: 1px solid #2a0808;
    padding: 1px 6px;
    border-radius: 2px;
}

/* ── Spinner ── */
.stSpinner > div > div { border-top-color: #cc1a18 !important; }

/* ── Animations ── */
@keyframes flicker {
    0%, 89%, 91%, 93%, 95%, 100% { opacity: 1; }
    90%, 92%, 94%                 { opacity: 0.82; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 30px rgba(150,10,10,0.12), inset 0 0 40px rgba(80,0,0,0.08); }
    50%       { box-shadow: 0 0 40px rgba(180,15,15,0.2),  inset 0 0 50px rgba(100,0,0,0.12); }
}
.response-card { animation: pulse-glow 4s ease-in-out infinite; }

/* ── CRT scanlines ── */
body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(0,0,0,0.06) 3px,
        rgba(0,0,0,0.06) 4px
    );
    pointer-events: none;
    z-index: 99999;
}

/* ── Vignette ── */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%);
    pointer-events: none;
    z-index: 99998;
}

/* ── Alert/warning overrides ── */
[data-testid="stAlert"] {
    background: #0a0000 !important;
    border: 1px solid #440000 !important;
    color: #cc4444 !important;
    border-radius: 2px !important;
}

</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">Hawkins, Indiana &nbsp;·&nbsp; Est. 1983</div>
    <hr class="hero-rule"/>
    <div class="hero-title">DOWNSIDE<span>·</span>UP</div>
    <div class="hero-sub">Complaint Bureau &nbsp;//&nbsp; Classified Division</div>
    <hr class="hero-rule"/>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Validate API key from .env ────────────────────────────────────────────────
if not OPENAI_API_KEY:
    st.error("⚠  OPENAI_API_KEY not found. Add it to your .env file and restart.")
    st.stop()

# ── Tools ─────────────────────────────────────────────────────────────────────
@tool
def consult_demogorgon(complaint: str) -> str:
    """Get the Demogorgon's perspective on a complaint about the Upside Down."""
    responses = [
        f"The Demogorgon tilts its head at '{complaint}'. Perhaps you're thinking in too few dimensions?",
        f"The Demogorgon makes a sound that might be agreement. The problem is temporal — time works differently in the Upside Down.",
        f"The Demogorgon appears to be eating something. Consistency doesn't seem to be a priority in its dimension.",
    ]
    return random.choice(responses)

@tool
def check_hawkins_records(query: str) -> str:
    """Search Hawkins historical records for patterns and explanations."""
    records = {
        "portal":      "Records show portals open with no clear schedule. Electromagnetic activity and emotional intensity both seem involved.",
        "monsters":    "Creature behaviour varies by time of day, emotional proximity, and unknown environmental factors.",
        "psychics":    "Psychic abilities vary greatly — linked to emotional state, energy, and origin of powers.",
        "electricity": "Hawkins has a long history of electrical anomalies strongly correlated with Upside Down activity.",
    }
    for key, value in records.items():
        if key in query.lower():
            return value
    return f"No specific records for '{query}', but unexplained events in Hawkins are extensively documented."

@tool
def cast_interdimensional_spell(problem: str, creativity_level: str = "medium") -> str:
    """Suggest a creative interdimensional spell or ritual."""
    n = {"low": 1, "medium": 2, "high": 3}.get(creativity_level, 2)
    spells = [
        f"Chant 'Bemca Becma Becma' three times holding a Walkman to recalibrate interdimensional frequencies for: {problem}",
        f"Place a compass in a salt circle — magnetic anomalies may stabilise: {problem}",
        f"Play 'Running Up That Hill' backwards at the site of the issue. Temporal resonance could resolve: {problem}",
        f"Arrange a lighter, a compass, and a personal item in a triangle while focusing on: {problem}",
    ]
    return "\n".join(random.sample(spells, min(n, len(spells))))

@tool
def gather_party_wisdom(question: str) -> str:
    """Ask the D&D party (Mike, Dustin, Lucas, Will) for collective insight."""
    party = {
        "portal":      "Mike: 'Portals open near strong emotions or EM disturbances.' Dustin: 'And they track the Mind Flayer's activity.'",
        "monsters":    "Lucas: 'Demogorgons are territorial but opportunistic.' Will: 'They sense fear — explains the inconsistency.'",
        "psychics":    "Mike: 'El's powers depend on her emotional state.' Dustin: 'Limited by mental energy — she can't do everything.'",
        "electricity": "Lucas: 'The Upside Down disrupts electrical systems.' Dustin: 'But it also creates feedback loops — two-way interference.'",
    }
    for key, response in party.items():
        if key in question.lower():
            return response
    return "The party huddles. Mike: 'Tough one.' Dustin: 'Need more info.' Lucas: 'Think it through.' Will: 'Try other sources.'"

tools     = [consult_demogorgon, check_hawkins_records, cast_interdimensional_spell, gather_party_wisdom]
tool_map  = {t.name: t for t in tools}

SYSTEM_PROMPT = """You are Becma, head of the Downside-Up Complaint Bureau.
Handle complaints about the Normal Objects universe creatively.
Use tools in any order you judge best.
Be entertaining, combine tool results, embrace the chaos, end with an actionable recommendation."""

# ── Agent ─────────────────────────────────────────────────────────────────────
def run_agent(complaint: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=complaint)]
    steps = []
    for _ in range(6):
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        if not response.tool_calls:
            return response.content, steps
        for tc in response.tool_calls:
            name, args, tid = tc["name"], tc["args"], tc["id"]
            result = tool_map[name].invoke(args) if name in tool_map else f"Unknown tool: {name}"
            steps.append((name, args, str(result)))
            messages.append(ToolMessage(content=str(result), tool_call_id=tid))
    return "Max iterations reached.", steps

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Input area ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">// File a complaint</div>', unsafe_allow_html=True)

complaint_text = st.text_area(
    label="complaint",
    placeholder="Describe the inconsistency you have witnessed in Hawkins...\n\n— Why do demogorgons sometimes eat people and sometimes don't?\n— The portal opens on different days. Is there a schedule?\n— Why do power lines react to creatures?",
    height=148,
    key="complaint_input",
    label_visibility="collapsed",
)

col1, col2 = st.columns([4, 1])
with col1:
    submit = st.button("▶  TRANSMIT TO BUREAU", use_container_width=True)
with col2:
    clear = st.button("✕ CLEAR", use_container_width=True)

if clear:
    st.session_state.history = []
    st.rerun()

# ── Submit ────────────────────────────────────────────────────────────────────
if submit:
    if not complaint_text.strip():
        st.warning("Enter a complaint before transmitting.")
    else:
        with st.spinner("Consulting the Upside Down..."):
            try:
                answer, steps = run_agent(complaint_text.strip())
                st.session_state.history.insert(0, {
                    "complaint": complaint_text.strip(),
                    "answer": answer,
                    "steps": steps,
                })
            except Exception as e:
                st.error(f"Transmission failed: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[0]

    # Tool steps
    if latest["steps"]:
        st.markdown('<div class="section-label">// Intelligence gathered</div>', unsafe_allow_html=True)
        rows = ""
        for i, (name, args, result) in enumerate(latest["steps"], 1):
            arg_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
            rows += f"""
<div class="step-row">
  <div class="step-icon">[{i:02d}]</div>
  <div class="step-body">
    <div class="step-name">{name}({arg_str})</div>
    <div class="step-result">{result[:180]}{'…' if len(result) > 180 else ''}</div>
  </div>
</div>"""
        st.markdown(f'<div class="steps-wrap">{rows}</div>', unsafe_allow_html=True)

    # Response
    st.markdown('<div class="section-label">// Bureau response</div>', unsafe_allow_html=True)
    safe_answer = latest["answer"].replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f'<div class="response-card"><div class="response-text">{safe_answer}</div></div>',
                unsafe_allow_html=True)

    # History
    if len(st.session_state.history) > 1:
        st.markdown('<div class="section-label" style="margin-top:2.5rem;">// Previous transmissions</div>',
                    unsafe_allow_html=True)
        cards = ""
        for item in st.session_state.history[1:]:
            badges = "".join(f'<span class="history-badge">{s[0]}</span>' for s in item["steps"])
            safe_q = item["complaint"][:90].replace("<","&lt;").replace(">","&gt;")
            safe_a = item["answer"][:200].replace("<","&lt;").replace(">","&gt;")
            cards += f"""
<div class="history-card">
  <div class="history-q">▸ {safe_q}{'…' if len(item['complaint'])>90 else ''}</div>
  <div class="history-a">{safe_a}{'…' if len(item['answer'])>200 else ''}</div>
  <div class="history-tools">{badges}</div>
</div>"""
        st.markdown(f'<div class="history-wrap">{cards}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding-bottom:2rem;
     font-family:'Share Tech Mono',monospace;font-size:0.6rem;
     letter-spacing:0.35em;color:#1e0505;">
  HAWKINS NATIONAL LABORATORY &nbsp;·&nbsp; LEVEL 5 CLEARANCE REQUIRED &nbsp;·&nbsp; DO NOT DISTRIBUTE
</div>
""", unsafe_allow_html=True)