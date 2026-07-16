# formatter/font_convertor.py

# Map user-friendly font names to actual font file paths
# You'll need .ttf font files for anything beyond default PDF fonts
FONT_MAP = {
    "Arial": "Helvetica",           # built-in PDF font, no file needed
    "Times New Roman": "Times-Roman",  # built-in PDF font
    "Courier New": "Courier",       # built-in PDF font
}

def convert_font(text: str, chosen_font: str):
    """
    Takes cleaned text and a chosen font name.
    Returns a dict with the text and the resolved font name
    that pdf_generator.py can use directly.
    """
    resolved_font = FONT_MAP.get(chosen_font, "Helvetica")  # default fallback

    return {
        "text": text,
        "font": resolved_font
    }