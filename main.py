import os
import streamlit as st
from ai.hybrid_ocr import hybrid_extract
from formatter.pdf_generator import generate_pdf

st.set_page_config(page_title="AI Scanner", page_icon="📄", layout="centered")

st.markdown("""<h1 style='text-align:center;'>📄 AI Document Scanner</h1> """, unsafe_allow_html=True)
st.write("Upload a handwritten or typed image to extract, clean, and export the text as a PDF.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Font selection — same options as your original Tkinter app
chosen_font = st.selectbox("Choose a font:", ["Arial", "Times New Roman", "Courier New"])

# Map display names to actual ReportLab base font names
FONT_MAP = {
    "Arial": "Helvetica",
    "Times New Roman": "Times-Roman",
    "Courier New": "Courier",
}

if uploaded_file is not None:
    os.makedirs("assets", exist_ok=True)
    image_path = os.path.join("assets", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    if "final_text" not in st.session_state or st.session_state.get("last_file") != uploaded_file.name:
        with st.spinner("Running AI OCR..."):
            raw_text, cleaned_text = hybrid_extract(image_path)
        st.session_state.final_text = cleaned_text if cleaned_text.strip() else raw_text
        st.session_state.last_file = uploaded_file.name

    final_text = st.session_state.final_text

    st.subheader("Recognized Text")
    edited_text = st.text_area("Output (editable)", final_text, height=300)

    output_path = os.path.join("output", "scanned_document.pdf")
    os.makedirs("output", exist_ok=True)

    if st.button("Generate PDF"):
        pdf_font = FONT_MAP.get(chosen_font, "Helvetica")
        generate_pdf(edited_text, output_path, font=pdf_font)
        st.success("✅ PDF Generated Successfully")
        with open(output_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="scanned_document.pdf")