import streamlit as st
import os
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MUN Digital Platform",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Persistent state helpers ──────────────────────────────────────────────────
COMMENTS_FILE = "mun_comments.json"
UPLOADS_DIR   = "mun_uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_comments(comments):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ─ Global reset ─ */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #0b0f1a;
    color: #dce3f0;
}

/* ─ Hide Streamlit chrome ─ */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem 2rem; max-width: 1100px; margin: auto; }

/* ─ Hero header ─ */
.mun-hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2e46 50%, #0d1b2a 100%);
    border-bottom: 1px solid #2a4060;
    padding: 2.4rem 2rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.mun-hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 60% at 50% -10%, rgba(65,120,200,.18) 0%, transparent 70%);
    pointer-events: none;
}
.mun-emblem {
    font-size: 2.8rem;
    margin-bottom: .4rem;
    filter: drop-shadow(0 0 18px rgba(100,160,255,.5));
}
.mun-hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #e8f0ff;
    letter-spacing: .06em;
    margin: 0;
    line-height: 1.2;
}
.mun-hero .subtitle {
    font-size: .95rem;
    font-weight: 300;
    color: #7a9bbf;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-top: .5rem;
}
.mun-divider {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, #4a8fd4, transparent);
    margin: 1rem auto 0;
}

/* ─ Section heading ─ */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #c5d8f0;
    border-left: 3px solid #3a7bd5;
    padding-left: .75rem;
    margin: 2rem 0 1.2rem;
    letter-spacing: .03em;
}

/* ─ Video wrapper ─ */
.video-wrapper {
    background: #101828;
    border: 1px solid #1e3050;
    border-radius: 6px;
    padding: 1.2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
}

/* ─ Comment card ─ */
.comment-card {
    background: linear-gradient(135deg, #111c2e 0%, #14213a 100%);
    border: 1px solid #1e3256;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: .75rem;
    transition: border-color .2s;
}
.comment-card:hover { border-color: #3a6bbf; }
.comment-meta {
    display: flex; align-items: center; gap: .7rem;
    margin-bottom: .4rem;
}
.comment-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, #1e4d8c, #3a7bd5);
    display: flex; align-items: center; justify-content: center;
    font-size: .85rem; font-weight: 700; color: #e8f0ff;
    flex-shrink: 0;
}
.comment-name { font-weight: 600; color: #9ec4f0; font-size: .92rem; }
.comment-date { font-size: .75rem; color: #4a6888; margin-left: auto; }
.comment-text { font-size: .9rem; color: #c8d8e8; line-height: 1.55; }

/* ─ File item ─ */
.file-item {
    background: #111c2e;
    border: 1px solid #1e3256;
    border-radius: 6px;
    padding: .85rem 1.1rem;
    margin-bottom: .6rem;
    display: flex; align-items: center; gap: .9rem;
}
.file-icon { font-size: 1.4rem; flex-shrink: 0; }
.file-name { font-size: .88rem; color: #a8c4e0; font-weight: 400; word-break: break-all; }
.file-size { font-size: .75rem; color: #4a6888; margin-top: .15rem; }

/* ─ Inputs & buttons ─ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0e1a2e !important;
    border: 1px solid #1e3256 !important;
    color: #dce3f0 !important;
    border-radius: 5px !important;
    font-family: 'Source Sans 3', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,.18) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1a4d8c, #2f6dbf) !important;
    color: #e8f0ff !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
    padding: .5rem 1.6rem !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .88 !important; }

/* ─ File uploader ─ */
[data-testid="stFileUploader"] {
    background: #0e1a2e !important;
    border: 1px dashed #2a4875 !important;
    border-radius: 6px !important;
    padding: .8rem !important;
}

/* ─ Alert / info ─ */
.stAlert { border-radius: 5px !important; }

/* ─ Horizontal rule ─ */
hr { border-color: #1e3050 !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mun-hero">
    <div class="mun-emblem">🌐</div>
    <h1>Model United Nations</h1>
    <p class="subtitle">Digital Conference Platform &nbsp;·&nbsp; Geneva Committee</p>
    <div class="mun-divider"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Opening Ceremony Video
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">📽 Opening Ceremony</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)

    VIDEO_URL = st.text_input(
        "Video URL (YouTube / direct MP4 link)",
        value="http://www.youtube.com/watch?v=DnKpnojwz2M",
        placeholder="https://...",
        label_visibility="collapsed",
    )

    # Streamlit's st.video accepts YouTube URLs and direct video links
    if VIDEO_URL.strip():
        try:
            st.video(VIDEO_URL.strip())
        except Exception:
            st.warning("⚠️ Video could not be loaded. Please check the URL.")
    else:
        st.info("Paste a video URL above to begin the session.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Delegate Comments
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">💬 Delegate Floor Statements</p>', unsafe_allow_html=True)

with st.form("comment_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        name = st.text_input("Delegate Name", placeholder="e.g. Amara Osei")
    with col2:
        comment = st.text_area("Statement / Comment", placeholder="Address the committee…", height=90)
    submitted = st.form_submit_button("📤  Submit Statement")

if submitted:
    name    = name.strip()
    comment = comment.strip()
    if not name or not comment:
        st.warning("Please provide both your name and a statement.")
    else:
        comments = load_comments()
        comments.append({
            "name":    name,
            "comment": comment,
            "date":    datetime.now().strftime("%d %b %Y, %H:%M"),
        })
        save_comments(comments)
        st.success("✅ Statement submitted successfully.")
        st.rerun()

# Display comments newest → oldest
comments = load_comments()
if comments:
    st.markdown(f"<p style='font-size:.82rem;color:#4a6888;margin-bottom:1rem;'>"
                f"{len(comments)} statement(s) recorded</p>", unsafe_allow_html=True)
    for c in reversed(comments):
        initial = c["name"][0].upper() if c["name"] else "?"
        st.markdown(f"""
        <div class="comment-card">
            <div class="comment-meta">
                <div class="comment-avatar">{initial}</div>
                <span class="comment-name">{c['name']}</span>
                <span class="comment-date">{c['date']}</span>
            </div>
            <div class="comment-text">{c['comment']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No statements yet. Be the first delegate to address the committee.")

st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Document Upload & Download
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">📁 Position Papers & Working Documents</p>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload your position paper or resolution draft (PDF only)",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="visible",
)

if uploaded:
    for f in uploaded:
        save_path = os.path.join(UPLOADS_DIR, f.name)
        with open(save_path, "wb") as out:
            out.write(f.read())
    st.success(f"✅ {len(uploaded)} document(s) uploaded.")

# List all uploaded files
pdf_files = sorted(
    [fn for fn in os.listdir(UPLOADS_DIR) if fn.lower().endswith(".pdf")]
)

if pdf_files:
    st.markdown(
        f"<p style='font-size:.82rem;color:#4a6888;margin:1rem 0 .8rem;'>"
        f"{len(pdf_files)} document(s) available for download</p>",
        unsafe_allow_html=True,
    )
    for fn in pdf_files:
        fp   = os.path.join(UPLOADS_DIR, fn)
        size = os.path.getsize(fp)
        size_str = f"{size/1024:.1f} KB" if size < 1_048_576 else f"{size/1_048_576:.2f} MB"

        col_info, col_dl = st.columns([5, 1])
        with col_info:
            st.markdown(f"""
            <div class="file-item">
                <div class="file-icon">📄</div>
                <div>
                    <div class="file-name">{fn}</div>
                    <div class="file-size">{size_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_dl:
            with open(fp, "rb") as dl_file:
                st.download_button(
                    label="⬇ Download",
                    data=dl_file.read(),
                    file_name=fn,
                    mime="application/pdf",
                    key=f"dl_{fn}",
                )
else:
    st.info("No documents uploaded yet. Delegates may upload PDF position papers above.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style='text-align:center;font-size:.75rem;color:#2a4060;letter-spacing:.1em;padding-bottom:1rem;'>
    MODEL UNITED NATIONS DIGITAL PLATFORM &nbsp;·&nbsp; CONFIDENTIAL &nbsp;·&nbsp; FOR COMMITTEE USE ONLY
</p>
""", unsafe_allow_html=True)