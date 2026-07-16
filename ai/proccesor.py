# ai/proccesor.py

from scanner.preprocess import preprocess_image
from ai.trocr import extract_text          # adjust function name if yours differs
from ai.cleanup import clean_ocr_output
from formatter.font_convertor import convert_font
from formatter.pdf_generator import generate_pdf

def run_pipeline(image_path: str, chosen_font: str):

    processed_img = preprocess_image(image_path)

    raw_text = extract_text(processed_img)

    cleaned_text = clean_ocr_output(raw_text)

    formatted_text = convert_font(cleaned_text, chosen_font)

    generate_pdf(formatted_text)

    return cleaned_text 
if __name__ == "__main__":
    test_image = r"C:\Users\user\Documents\ai document scanner\AI-SCANNER\assets\handwriting.jpg"
    result_text = run_pipeline(test_image, chosen_font="Arial")
    print("Pipeline finished. Extracted & cleaned text:")
    print(result_text)