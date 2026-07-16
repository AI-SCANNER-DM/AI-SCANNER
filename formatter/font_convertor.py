
FONT_MAP = {
    "Arial": "Helvetica",          
    "Times New Roman": "Times-Roman",  
    "Courier New": "Courier",      
}

def convert_font(text: str, chosen_font: str):
    """
    Takes cleaned text and a chosen font name.
    Returns a dict with the text and the resolved font name
    that pdf_generator.py can use directly.
    """
    resolved_font = FONT_MAP.get(chosen_font, "Helvetica")  

    return {
        "text": text,
        "font": resolved_font
    }