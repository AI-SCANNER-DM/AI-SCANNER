# app.py
"""
Streamlit front-end for AI-SCANNER.

Run with:
    streamlit run app.py

Expects your existing project structure:
    ai/hybrid_ocr.py        -> hybrid_extract(image_path) -> (raw_text, cleaned_text)
    formatter/pdf_generator.py -> PDFGenerator().generate(text, output_path)
    scanner/document_detector.py (optional) -> detect_document(image_path) -> processed_path
"""

import os
import time
import tempfile
import traceback

import streamlit as st
from PIL import Image
import cv2

# ---- Project imports ----
from ai.hybrid_ocr import hybrid_extract
from formatter.pdf_generator import PDFGenerator

pdf_generator = PDFGenerator()

try:
    from scanner.document_detector import detect_document
    HAS_DETECTOR = True
except ImportError:
    HAS_DETECTOR = False


# ---------------- Page config ----------------
st.set_page_config(
    page_title="AI Scanner",
    page_icon="📝",
    layout="wide",
)

# ---------------- Session state ----------------
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "cleaned_text" not in st.session_state:
    st.session_state.cleaned_text = ""
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
if "processed" not in st.session_state:
    st.session_state.processed = False


# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("⚙️ Settings")
    use_detector = st.checkbox(
        "Auto-crop / deskew page (if available)",
        value=HAS_DETECTOR,
        disabled=not HAS_DETECTOR,
        help="Uses scanner/document_detector.py to straighten and crop the page before OCR."
        if HAS_DETECTOR else "document_detector.py not found — skipping this step.",
    )
    text_choice = st.radio(
        "Text version to use for PDF",
        options=["Cleaned (LangChain)", "Raw OCR"],
        index=0,
    )
    st.markdown("---")
    st.caption(
        "Pipeline: EasyOCR line detection → TrOCR handwriting recognition "
        "→ LangChain cleanup → PDF"
    )


# ---------------- Main layout ----------------
st.title("📝 AI Scanner")
st.write("Upload a photo or scan of handwritten notes and convert it into a clean, printable PDF.")

col_upload, col_preview = st.columns([1, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"],
        help="A single page works best — clear lighting, minimal skew.",
    )

    run_button = st.button("🚀 Run OCR", type="primary", disabled=uploaded_file is None)

with col_preview:
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded image", use_container_width=True)


# ---------------- Processing ----------------
if run_button and uploaded_file is not None:
    st.session_state.processed = False
    st.session_state.raw_text = ""
    st.session_state.cleaned_text = ""
    st.session_state.pdf_path = None

    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = os.path.join(tmp_dir, uploaded_file.name)
        image.save(input_path)

        status = st.status("Processing image...", expanded=True)

        try:
            processed_path = input_path

            if use_detector and HAS_DETECTOR:
                status.write("Detecting and straightening document...")
                img_array = cv2.imread(input_path)
                detected_array = detect_document(img_array)
                processed_path = os.path.join(tmp_dir, "_processed.jpg")
                cv2.imwrite(processed_path, detected_array)

            status.write("Running EasyOCR line detection + TrOCR recognition...")
            raw_text, cleaned_text = hybrid_extract(processed_path)

            status.write("Generating PDF...")
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            pdf_filename = f"scanned_document_{int(time.time())}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)

            final_text = cleaned_text if (text_choice.startswith("Cleaned") and cleaned_text.strip()) else raw_text
            pdf_generator.generate(final_text, pdf_path)

            st.session_state.raw_text = raw_text
            st.session_state.cleaned_text = cleaned_text
            st.session_state.pdf_path = pdf_path
            st.session_state.processed = True

            status.update(label="Done!", state="complete", expanded=False)

        except Exception:
            status.update(label="Failed", state="error")
            st.error("Something went wrong during processing:")
            st.code(traceback.format_exc())


# ---------------- Results ----------------
if st.session_state.processed:
    st.markdown("---")
    st.subheader("📄 Recognized Text")

    tab_cleaned, tab_raw = st.tabs(["Cleaned", "Raw"])
    with tab_cleaned:
        st.text_area(
            "Cleaned text (LangChain)",
            value=st.session_state.cleaned_text,
            height=300,
            label_visibility="collapsed",
        )
    with tab_raw:
        st.text_area(
            "Raw OCR output",
            value=st.session_state.raw_text,
            height=300,
            label_visibility="collapsed",
        )

    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=os.path.basename(st.session_state.pdf_path),
                mime="application/pdf",
            )
