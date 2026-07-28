import os
import streamlit as st
from ai.hybrid_ocr import hybrid_extract
from ai.chatbot import build_qa_chain
from formatter.pdf_generator import generate_pdf

st.set_page_config(page_title="AI Scanner", page_icon="📄", layout="wide")

st.markdown("""
<div class="hero-title">
    <h1>📄 AI Document Scanner</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ---------- Light theme base ---------- */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(160deg, #FDF2F8 0%, #ECFEFF 50%, #F0FDF4 100%) !important;
    color: #1F2937 !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #1F2937;
}

/* ---------- Overall page: push content to edges, add breathing room ---------- */
.block-container {
    max-width: 100% !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
    padding-top: 2rem !important;
}

/* ---------- Hero heading with border + hover (kept centered) ---------- */
.hero-title {
    max-width: 850px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    padding: 1.2rem 2rem;
    background: linear-gradient(90deg, #FCE7F3, #CFFAFE, #DCFCE7);
    border: 2px solid #06B6D4;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}
.hero-title:hover {
    border-color: #EC4899;
    box-shadow: 0 0 24px rgba(236, 72, 153, 0.25);
    transform: scale(1.01);
}
.hero-title h1 {
    margin: 0;
    color: #0E7490;
}

/* ---------- Everything else: left-aligned, bigger text ---------- */
.stMarkdown p {
    font-size: 1.05rem;
}
h3 {
    font-size: 1.6rem !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 1.05rem !important;
}

/* ---------- Uploader: bigger text to match wider layout ---------- */
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stFileUploaderDropzone"] span {
    font-size: 1.05rem;
}

/* ---------- Selectbox text ---------- */
[data-baseweb="select"] div {
    font-size: 1.05rem !important;
}

/* ---------- Generate PDF button (light green) ---------- */
.stButton > button {
    background: linear-gradient(90deg, #86EFAC, #4ADE80);
    color: #14532D;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 2rem;
    font-size: 1.05rem;
    font-weight: 600;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(74, 222, 128, 0.4);
    background: linear-gradient(90deg, #4ADE80, #86EFAC);
}
.stButton > button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.5), 0 4px 10px rgba(74, 222, 128, 0.3);
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98);
}

/* ---------- Fix Generate PDF button fading on click/running state ---------- */
.stButton > button:disabled,
.stButton > button[disabled] {
    background: linear-gradient(90deg, #86EFAC, #4ADE80) !important;
    color: #14532D !important;
    opacity: 0.85 !important;
}
.stButton > button:disabled p,
.stButton > button[disabled] p {
    color: #14532D !important;
    opacity: 1 !important;
}

/* ---------- Download PDF button (pink) ---------- */
.stDownloadButton > button {
    background: linear-gradient(90deg, #F9A8D4, #EC4899);
    color: #831843;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 2rem;
    font-size: 1.05rem;
    font-weight: 600;
    transition: all 0.25s ease;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(236, 72, 153, 0.4);
}
.stDownloadButton > button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.5), 0 6px 18px rgba(236, 72, 153, 0.4);
}
.stDownloadButton > button:active {
    transform: translateY(0px) scale(0.98);
}

/* ---------- File uploader: hover + focus + transform + shadow ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    border: 1.5px solid #A5F3FC;
    border-radius: 12px;
    transition: all 0.25s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #06B6D4;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.25);
    transform: translateY(-2px);
}
[data-testid="stFileUploaderDropzone"]:focus-within {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25), 0 0 18px rgba(6, 182, 212, 0.2);
    transform: translateY(-2px);
}

/* ---------- Selectbox (Choose a font): full glow-up ---------- */
[data-baseweb="select"] {
    border-radius: 10px !important;
    transition: all 0.25s ease;
}
[data-baseweb="select"] > div {
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.06), rgba(6, 182, 212, 0.06)) !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    transition: all 0.25s ease;
}
[data-baseweb="select"]:hover > div {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.2);
    transform: translateY(-2px);
}
[data-baseweb="select"]:focus-within > div {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25), 0 0 18px rgba(6, 182, 212, 0.2);
    transform: translateY(-2px);
}

/* ---------- Divider between uploader and font ---------- */
hr {
    border: none;
    border-top: 1px solid #06B6D4;
    opacity: 0.4;
    transition: all 0.3s ease;
}

/* ---------- Bordered section boxes: light pink ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FDF2F8 !important;
    border-color: #F9A8D4 !important;
    transition: all 0.3s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 0 16px rgba(249, 168, 212, 0.35);
}

/* ---------- Remove default blue focus outline on containers ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:focus,
div[data-testid="stVerticalBlockBorderWrapper"]:focus-visible,
div[data-testid="stVerticalBlock"]:focus,
div[data-testid="stVerticalBlock"]:focus-visible,
[tabindex]:focus,
[tabindex]:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

st.write("Upload a handwritten or typed image to extract, clean, and export the text as a PDF.")

FONT_MAP = {
    "Arial": "Helvetica",
    "Times New Roman": "Times-Roman",
    "Courier New": "Courier",
}

st.subheader("1. Upload & Font")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
st.markdown("<hr style='margin: 1.2rem 0;'>", unsafe_allow_html=True)
chosen_font = st.selectbox("Choose a font:", ["Arial", "Times New Roman", "Courier New"])

if uploaded_file is not None:
    os.makedirs("assets", exist_ok=True)
    image_path = os.path.join("assets", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.container(border=True):
        st.subheader("2. Preview")
        st.image(image_path, caption="Uploaded Image", use_container_width=True)

    if "final_text" not in st.session_state or st.session_state.get("last_file") != uploaded_file.name:
        with st.spinner("Running AI OCR..."):
            raw_text, cleaned_text = hybrid_extract(image_path)
        st.session_state.final_text = cleaned_text if cleaned_text.strip() else raw_text
        st.session_state.last_file = uploaded_file.name

    final_text = st.session_state.final_text

    with st.container(border=True):
        st.subheader("3. Recognized Text")
        edited_text = st.text_area("Output (editable)", final_text, height=300)

    output_path = os.path.join("output", "scanned_document.pdf")
    os.makedirs("output", exist_ok=True)

    with st.container(border=True):
        st.subheader("4. Export")
        if st.button("Generate PDF"):
            pdf_font = FONT_MAP.get(chosen_font, "Helvetica")
            generate_pdf(edited_text, output_path, font=pdf_font)
            st.success("PDF Generated Successfully")
            with open(output_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="scanned_document.pdf")

            # --- Chatbot integration ---
            if "last_pdf_path" not in st.session_state or st.session_state.last_pdf_path != output_path:
                with st.spinner("Preparing chatbot..."):
                    st.session_state.qa_chain = build_qa_chain(output_path)
                st.session_state.last_pdf_path = output_path
                st.session_state.chat_history = []

# Chatbot UI — shown once a PDF has been generated at least once
if "qa_chain" in st.session_state:
    with st.container(border=True):
        st.subheader("💬 Ask questions about this document")

        question = st.text_input("Your question:")
        if question:
            with st.spinner("Thinking..."):
                result = st.session_state.qa_chain.invoke({"input": question})
                answer = result["answer"]
            st.session_state.chat_history.append((question, answer))

        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Bot:** {a}")