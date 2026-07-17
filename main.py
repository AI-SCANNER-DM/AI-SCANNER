from ai.trocr import recognize_text
from formatter.pdf_generator import PDFGenerator
import os


def main():

    image_path = "assets/handwriting.jpg"

    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: '{image_path}' not found.")
        return

    print("Loading image...")
    print("Running AI OCR...\n")

    # OCR
    text = recognize_text(image_path)

    print("========== RECOGNIZED TEXT ==========\n")
    print(text)
    print("\n=====================================\n")

    # Generate PDF
    pdf = PDFGenerator()
    pdf_path = pdf.generate(text)

    print("\nProject completed successfully!")
    print(f"PDF saved at: {pdf_path}")


if __name__ == "__main__":
    main()