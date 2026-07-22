# main.py
import os
from ai.hybrid_ocr import hybrid_extract
from formatter.pdf_generator import generate_pdf


def main():
    image_path = r"assets\handwriting.jpg"
    output_path = r"output\scanned_document.pdf"

    if not os.path.exists(image_path):
        print(f"ERROR: Input image not found at {image_path}")
        return

    print("Loading image...")
    print("Running AI OCR...")

    raw_text, cleaned_text = hybrid_extract(image_path)

    print("========== RECOGNIZED TEXT ==========")
    print(cleaned_text if cleaned_text.strip() else raw_text)
    print("=====================================")

    final_text = cleaned_text if cleaned_text.strip() else raw_text

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generate_pdf(final_text, output_path)

    print("✅ PDF Generated Successfully")
    print(f"Saved at: {os.path.abspath(output_path)}")
    print("Project completed successfully!")
    print(f"PDF saved at: {output_path}")


if __name__ == "__main__":
    main()