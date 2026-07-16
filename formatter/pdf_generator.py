from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def generate_pdf(formatted_data: dict, output_path: str = "assets/output.pdf"):
    """
    Takes a dict with 'text' and 'font' (from convert_font),
    and writes it into a PDF file.
    """
    text = formatted_data["text"]
    font_name = formatted_data["font"]

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont(font_name, 12)

    x_margin = 1 * inch
    y_position = height - 1 * inch
    line_height = 14

    max_chars_per_line = 90  
    words = text.split()
    line = ""

    for word in words:
        if len(line) + len(word) + 1 <= max_chars_per_line:
            line += word + " "
        else:
            c.drawString(x_margin, y_position, line.strip())
            y_position -= line_height
            line = word + " "

          
            if y_position < 1 * inch:
                c.showPage()
                c.setFont(font_name, 12)
                y_position = height - 1 * inch

    if line:
        c.drawString(x_margin, y_position, line.strip())

    c.save()
    print(f"PDF saved to {os.path.abspath(output_path)}")