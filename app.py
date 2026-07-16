import streamlit as st
import time
from groq import Groq
from tavily import TavilyClient



groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tavily_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

GROQ_MODEL = "llama-3.3-70b-versatile"

st.set_page_config(page_title="Fake News Fact-Checker", page_icon="📰", layout="centered")



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fallback: same gradient directly on html/body in case a Streamlit
   version renames the outer wrapper class. Harmless if .stApp already works. */
html, body {
    background:
        radial-gradient(circle at 15% 20%, rgba(255,61,127,0.35), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(198,31,168,0.40), transparent 50%),
        radial-gradient(circle at 50% 90%, rgba(74,15,122,0.55), transparent 55%),
        linear-gradient(160deg, #3B0A66 0%, #7A1B8F 45%, #C61FA8 75%, #FF3D7F 100%) !important;
    background-attachment: fixed !important;
}

/* The gradient + grid lives on the outermost app wrapper... */
.stApp {
    background:
        linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px) 0 0 / 42px 42px,
        linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px) 0 0 / 42px 42px,
        radial-gradient(circle at 15% 20%, rgba(255,61,127,0.35), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(198,31,168,0.40), transparent 50%),
        radial-gradient(circle at 50% 90%, rgba(74,15,122,0.55), transparent 55%),
        linear-gradient(160deg, #3B0A66 0%, #7A1B8F 45%, #C61FA8 75%, #FF3D7F 100%) !important;
    background-attachment: fixed !important;
}
/* ...and EVERY container Streamlit nests inside it must be transparent,
   otherwise its own default background paints over the gradient completely. */
[data-testid="stHeader"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stBottomBlockContainer"],
[data-testid="stVerticalBlock"],
section.main,
.main .block-container,
.block-container {
    background: transparent !important;
    background-color: transparent !important;
}

/* Hero header block */
.hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.75rem;
    color: #F3D9F0;
    opacity: 0.85;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    line-height: 1.15;
    color: #FFFFFF;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    font-size: 1.05rem;
    color: #F3D9F0;
    opacity: 0.9;
    margin-bottom: 1.8rem;
}

/* Glass card wrapper used around inputs/results */
.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* Verdict pills */
.pill {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 0.8rem;
}
.pill-true { background: rgba(94, 234, 172, 0.18); color: #5EEAAC; border: 1px solid rgba(94,234,172,0.4); }
.pill-false { background: rgba(255, 90, 90, 0.18); color: #FF8080; border: 1px solid rgba(255,90,90,0.4); }
.pill-unclear { background: rgba(255, 209, 102, 0.18); color: #FFD166; border: 1px solid rgba(255,209,102,0.4); }

/* Streamlit widget overrides */
h1, h2, h3, .stMarkdown p, label, .stRadio label, .stSelectbox label {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif;
}
.stTextArea textarea,
.stTextArea [data-baseweb="textarea"],
.stTextArea [data-baseweb="base-input"],
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.10) !important;
    background-color: rgba(255,255,255,0.10) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
.stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.55) !important;
}
.stTextArea textarea:focus,
.stTextArea [data-baseweb="base-input"]:focus-within {
    border: 1px solid rgba(255,61,127,0.7) !important;
    box-shadow: 0 0 0 2px rgba(255,61,127,0.25) !important;
}
.stButton button {
    background: linear-gradient(90deg, #FF3D7F, #C61FA8) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.6rem !important;
    box-shadow: 0 4px 18px rgba(198,31,168,0.45);
}
.stButton button:hover {
    box-shadow: 0 6px 22px rgba(255,61,127,0.55);
    transform: translateY(-1px);
}
a { color: #FFB3D9 !important; }
hr { border-color: rgba(255,255,255,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# Hero header
st.markdown("""
<div class="hero-eyebrow">AI-Powered Verification</div>
<div class="hero-title">Truth Scan</div>
<div class="hero-sub">Checks claims in Hindi &amp; English against real web sources — not just language patterns.</div>
""", unsafe_allow_html=True)




def call_groq(messages, max_tokens=400, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                max_tokens=max_tokens,
                messages=messages,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate" in str(e).lower() and attempt < max_retries - 1:
                st.info("Rate limit hit, waiting a few seconds and retrying...")
                time.sleep(5)
            else:
                st.error(f"Error talking to Groq: {e}")
                return None
    return None




def extract_claim(text):
    prompt = f"""Extract the core factual claim from this text (it may be in Hindi, English, or Hinglish).
Translate it to English if needed. Be concise — respond with ONE sentence only, nothing else.

Text: "{text}"
"""
    return call_groq([{"role": "user", "content": prompt}], max_tokens=100)




def search_evidence(claim):
    try:
        results = tavily_client.search(query=claim, max_results=5, search_depth="advanced")
        return results.get("results", [])
    except Exception as e:
        st.error(f"Error searching the web: {e}")
        return []




def synthesize_verdict(claim, evidence):
    sources_text = "\n\n".join(
        f"Source: {e['url']}\nContent: {e['content'][:500]}"
        for e in evidence
    )
    prompt = f"""Claim to verify: "{claim}"

Evidence gathered from web search:
{sources_text}

Based ONLY on the evidence above, respond in exactly this format:
VERDICT: [SUPPORTED / CONTRADICTED / NO_CLEAR_EVIDENCE]
CONFIDENCE: [a number from 0 to 100]
EXPLANATION: [2-3 sentences explaining the verdict, referencing the evidence]

If the evidence is thin, unclear, or low quality, say NO_CLEAR_EVIDENCE rather than guessing.
"""
    return call_groq([{"role": "user", "content": prompt}], max_tokens=400)




def surface_warning_signs(text):
    flags = []
    lowered = text.lower()
    if any(w in lowered for w in ["miracle", "cure", "guaranteed", "shocking", "banned forever"]):
        flags.append("Sensational or exaggerated language detected")
    if any(w in lowered for w in ["forward this", "share immediately", "before it's deleted"]):
        flags.append("Phrasing common in viral forwarded messages")
    if text.count("!") >= 3 or (text.isupper() and len(text) > 15):
        flags.append("Excessive exclamation marks or all-caps text")
    return flags




st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Enter News Text")
input_method = st.radio("Choose input method:", ["Text Box", "Example News"])

if input_method == "Text Box":
    user_input = st.text_area("Paste news article or headline:", height=150)
else:
    examples = [
        "Mumbai receives heavy rainfall, local train services affected",
        "Eating onions cures COVID-19 completely",
        "Government to ban all social media from next month",
        "Stock market closes higher, Sensex gains 500 points",
        "WhatsApp will start charging fees from tomorrow",
        "Sarkar sare social media band karegi agle mahine se",
        "Bharat ne Australia ko 6 wicket se haraya cricket match mein",
    ]
    user_input = st.selectbox("Select an example:", examples)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Analyze News"):
    if not user_input:
        st.warning("Please enter some text to analyze")
    else:
        # Step A: extract the claim
        with st.spinner("Reading the claim..."):
            claim = extract_claim(user_input)

        if not claim:
            st.markdown('<span class="pill pill-false">Could not process this text</span>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"**Claim identified:** {claim}")

            # Step B: search the web
            with st.spinner("Searching the web for evidence..."):
                evidence = search_evidence(claim)

            if not evidence:
                st.markdown(
                    '<span class="pill pill-unclear">⚠️ No sources found — cannot verify</span>'
                    '<p style="color:#F3D9F0;">This claim may be too new, too obscure, or hard to '
                    'match to news coverage. Please check trusted sources manually.</p>',
                    unsafe_allow_html=True,
                )
            else:
                # Step C: get the verdict
                with st.spinner("Weighing the evidence..."):
                    verdict_text = synthesize_verdict(claim, evidence)

                if verdict_text:
                    # Simple display based on keywords in the AI's answer
                    if "CONTRADICTED" in verdict_text:
                        st.markdown('<span class="pill pill-false">🚨 This claim appears to be FALSE</span>', unsafe_allow_html=True)
                    elif "SUPPORTED" in verdict_text:
                        st.markdown('<span class="pill pill-true">✅ This claim appears to be TRUE</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="pill pill-unclear">❔ Not enough clear evidence</span>', unsafe_allow_html=True)

                    st.markdown(f'<p style="color:#F3D9F0; white-space: pre-wrap;">{verdict_text}</p>', unsafe_allow_html=True)

                st.markdown("**Sources checked**")
                for e in evidence:
                    title = e.get("title", e["url"])
                    st.markdown(f"- [{title}]({e['url']})")

            st.markdown('</div>', unsafe_allow_html=True)

            # Step D: cheap surface-level signals (always shown, doesn't need internet)
            flags = surface_warning_signs(user_input)
            if flags:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**⚠️ Additional Warning Signs**")
                for f in flags:
                    st.write(f"- {f}")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Fact-Checking Tips**")
        st.write("✓ Verify from multiple trusted news sources")
        st.write("✓ Check the publication date and author")
        st.write("✓ Look for official confirmations")
        st.write("✓ Be skeptical of sensational claims")
        st.write("✓ Don't forward unverified information")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<p style="color:#F3D9F0; opacity:0.7; font-size:0.85rem; margin-top:1.5rem;">'
    "This tool checks claims against web search results using AI reasoning. "
    "It is not a substitute for professional fact-checking — always verify "
    "important claims yourself before sharing.</p>",
    unsafe_allow_html=True,
)
