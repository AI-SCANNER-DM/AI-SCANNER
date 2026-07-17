"""
AI Document Classifier
----------------------
Classifies OCR extracted text into different document categories.
"""

from transformers import pipeline

# Load the Hugging Face zero-shot classification model
classifier = pipeline(
    task="zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Supported document categories
DOCUMENT_LABELS = [
    "Invoice",
    "Receipt",
    "Resume",
    "Letter",
    "Notes",
    "Assignment",
    "Certificate",
    "Report",
    "Bill",
    "Identity Document",
    "Application Form"
]


def classify_document(text):
    """
    Classify OCR extracted text.

    Parameters
    ----------
    text : str
        OCR extracted text.

    Returns
    -------
    dict
        Example:
        {
            "label": "Assignment",
            "confidence": 0.97
        }
    """

    if not text.strip():
        return {
            "label": "Unknown",
            "confidence": 0.0
        }

    result = classifier(
        sequences=text,
        candidate_labels=DOCUMENT_LABELS
    )

    return {
        "label": result["labels"][0],
        "confidence": round(float(result["scores"][0]), 4)
    }