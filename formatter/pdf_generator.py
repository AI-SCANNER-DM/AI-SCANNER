from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os


class PDFGenerator:
    """
    Generates a PDF from recognized text.
    """

    def __init__(self):
        self.page_size = A4
        self.font = "Helvetica"
        self.font_size = 12
        self.margin = 1 * inch
        self.line_height = 18

    def generate(self, text, output_path="output/scanned_document.pdf"):

        os.makedirs("output", exist_ok=True)

        pdf = canvas.Canvas(output_path, pagesize=self.page_size)

        width, height = self.page_size

        pdf.setFont(self.font, self.font_size)

        x = self.margin
        y = height - self.margin

        words = text.split()
        line = ""

        max_chars = 95

        for word in words:

            if len(line + word) <= max_chars:
                line += word + " "

            else:
                pdf.drawString(x, y, line.strip())

                y -= self.line_height

                line = word + " "

                if y < self.margin:

                    pdf.showPage()

                    pdf.setFont(self.font, self.font_size)

                    y = height - self.margin

        if line:
            pdf.drawString(x, y, line.strip())

        pdf.save()

        print("\n✅ PDF Generated Successfully")
        print("Saved at:", os.path.abspath(output_path))

        return output_path