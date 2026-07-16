from ai.trocr import recognize_text

text = recognize_text(
    "assets/handwriting.jpg"
)

print("\nRecognized Text:\n")
print(text)
from formatter.pdf_generator import PDFGenerator

pdf = PDFGenerator()

pdf.generate_pdf(
    text,
    "documents/output.pdf"
)