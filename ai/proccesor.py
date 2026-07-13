from trocr import extract_text          # your existing OCR function
from cleanup import clean_ocr_output    # Step 4
from formatter.font_convertor import convert_font
from formatter.pdf_generator import generate_pdf

def run_pipeline(image_path, chosen_font):
    raw_text = extract_text(image_path)
    cleaned_text = clean_ocr_output(raw_text)
    formatted_text = convert_font(cleaned_text, chosen_font)
    generate_pdf(formatted_text)