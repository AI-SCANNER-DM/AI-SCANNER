# AI Digitalised Document Scanner

## Overview

AI Digitalised Document Scanner is a Python-based project that converts handwritten and printed documents into editable digital text using Artificial Intelligence.

The system performs:

- Document detection
- Image preprocessing
- Handwriting recognition
- Text cleanup
- PDF generation
- DOCX generation

---

## Features

- Scan notebook pages
- Recognize handwritten text
- Recognize printed text
- Export as TXT
- Export as PDF
- Export as DOCX
- AI-powered OCR using TrOCR
- Image enhancement using OpenCV

---

## Technologies Used

- Python
- OpenCV
- TrOCR
- Hugging Face Transformers
- PyTorch
- Pillow
- Tesseract OCR
- LangChain (Future Enhancement)

---

## Project Structure

AI-SCANNER/
│
├── ai/
├── scanner/
├── formatter/
├── gui/
├── storage/
├── assets/
├── output/
├── config.py
├── requirements.txt
├── README.md
└── main.py

---

## Installation

Clone the repository.

Create a virtual environment.

Install the required libraries.

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python main.py
```

---

## Future Improvements

- Automatic page detection
- Multi-page scanning
- Cloud storage
- Searchable documents
- AI grammar correction
- RAG-based document understanding
- LangChain integration

---

## Authors

Developed as a BCA AI Project.
