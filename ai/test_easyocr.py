# ai/test_easyocr.py

import easyocr

reader = easyocr.Reader(['en'])  # 'en' = English, downloads model first time (one-time)

image_path = r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting_0.jpg"

results = reader.readtext(image_path)

full_text = ""
for (bbox, text, confidence) in results:
    print(f"[{confidence:.2f}] {text}")
    full_text += text + "\n"

print("\n--- FULL EXTRACTED TEXT ---")
print(full_text)