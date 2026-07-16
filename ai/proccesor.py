# ai/proccesor.py

from scanner.preprocess import preprocess_image
from ai.trocr import recognize_text
from ai.cleanup import clean_ocr_output
from formatter.font_convertor import convert_font
from formatter.pdf_generator import generate_pdf
import cv2


def run_pipeline(image_path: str, chosen_font: str):
    # Step 1: Clean/deskew the raw image
    processed_img = preprocess_image(image_path)

    # Save the processed image so trocr.py can open it via PIL
    processed_path = "assets/_processed_temp.jpg"
    success = cv2.imwrite(processed_path, processed_img)
    if not success:
        print("WARNING: Failed to save processed image!")
    else:
        print(f"Processed image saved to {processed_path}")

    # Step 2: Extract text using TrOCR
    raw_text = recognize_text(processed_path)

    # Step 3: Fix OCR errors using LangChain + Groq
    cleaned_text = clean_ocr_output(raw_text)

    # Step 4: Apply chosen font
    formatted_text = convert_font(cleaned_text, chosen_font)

    # Step 5: Generate final PDF
    generate_pdf(formatted_text)

    return cleaned_text


if __name__ == "__main__":
    test_image = r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting_0.jpg"
    result_text = run_pipeline(test_image, chosen_font="Arial")
    print("Pipeline finished. Extracted & cleaned text:")
    print(result_text)