from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register custom fonts (you can add more later)
try:
    pdfmetrics.registerFont(TTFont("Arial", "fonts/arial.ttf"))
except:
    pass


class FontConverter:

    def __init__(self):
        self.available_fonts = {
            "Times": "Times-Roman",
            "Helvetica": "Helvetica",
            "Courier": "Courier",
            "Arial": "Arial"
        }

    def get_font(self, font_name):

        if font_name in self.available_fonts:
            return self.available_fonts[font_name]

        return "Helvetica"

    def list_fonts(self):
        return list(self.available_fonts.keys())