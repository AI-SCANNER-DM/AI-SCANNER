from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

class PDFGenerator:
    def __init__(self, font="Helvetica"):
        self.page_size = A4
        self.font = font
        self.font_size = 12
        self.margin = 1 * inch
        self.line_height = 18

    def generate(self, text, output_path="output/scanned_document.pdf"):
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        pdf = canvas.Canvas(output_path, pagesize=self.page_size)
        width, height = self.page_size
        pdf.setFont(self.font, self.font_size)
        x = self.margin
        y = height - self.margin
        max_chars = 95

        paragraphs = text.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip() == "":
                y -= self.line_height
                if y < self.margin:
                    pdf.showPage()
                    pdf.setFont(self.font, self.font_size)
                    y = height - self.margin
                continue

            words = paragraph.split()
            line = ""
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
                y -= self.line_height
                if y < self.margin:
                    pdf.showPage()
                    pdf.setFont(self.font, self.font_size)
                    y = height - self.margin

        pdf.save()
        print("\n✅ PDF Generated Successfully")
        print("Saved at:", os.path.abspath(output_path))
        return output_path


def generate_pdf(text, output_path="output/scanned_document.pdf", font="Helvetica"):
    generator = PDFGenerator(font=font)
    return generator.generate(text, output_path)