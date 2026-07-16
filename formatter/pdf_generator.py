from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()

    def generate_pdf(self, text, output_file):

        document = SimpleDocTemplate(output_file)

        story = []

        paragraph = Paragraph(text, self.styles["Normal"])

        story.append(paragraph)

        document.build(story)

        print(f"PDF saved as {output_file}")