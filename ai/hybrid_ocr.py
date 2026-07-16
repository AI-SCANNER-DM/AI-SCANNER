# ai/hybrid_ocr.py

import easyocr
from ai.trocr import recognize_text
from ai.cleanup import clean_ocr_output
import cv2
import os

reader = easyocr.Reader(['en'])


def group_into_lines(results, y_threshold=15):
    boxes = []
    for (bbox, text, conf) in results:
        (tl, tr, br, bl) = bbox
        y_center = (tl[1] + bl[1]) / 2
        x_left = tl[0]
        boxes.append((y_center, x_left, bbox))

    boxes.sort(key=lambda b: b[0])

    lines = []
    current_line = []
    current_y = None

    for (y, x, bbox) in boxes:
        if current_y is None or abs(y - current_y) <= y_threshold:
            current_line.append((x, bbox))
            current_y = y if current_y is None else current_y
        else:
            current_line.sort(key=lambda b: b[0])
            lines.append([bb for (_, bb) in current_line])
            current_line = [(x, bbox)]
            current_y = y

    if current_line:
        current_line.sort(key=lambda b: b[0])
        lines.append([bb for (_, bb) in current_line])

    return lines


def hybrid_extract(image_path):
    print("Starting hybrid_extract...", flush=True)

    img = cv2.imread(image_path)
    if img is None:
        print("ERROR: Could not read image at", image_path, flush=True)
        return "", ""

    print("Running EasyOCR detection...", flush=True)
    results = reader.readtext(image_path)
    print(f"EasyOCR found {len(results)} raw text boxes.", flush=True)

    lines = group_into_lines(results)
    print(f"Grouped into {len(lines)} lines. Starting TrOCR recognition...", flush=True)

    os.makedirs("assets/hybrid_lines", exist_ok=True)
    full_text = ""

    for i, line_boxes in enumerate(lines):
        xs_min, ys_min, xs_max, ys_max = [], [], [], []
        for bbox in line_boxes:
            (tl, tr, br, bl) = bbox
            xs_min.append(min(tl[0], bl[0]))
            xs_max.append(max(tr[0], br[0]))
            ys_min.append(min(tl[1], tr[1]))
            ys_max.append(max(bl[1], br[1]))

        x_min, x_max = int(min(xs_min)), int(max(xs_max))
        y_min, y_max = int(min(ys_min)), int(max(ys_max))

        crop = img[y_min:y_max, x_min:x_max]
        crop_path = f"assets/hybrid_lines/line_{i}.jpg"
        cv2.imwrite(crop_path, crop)

        print(f"Processing line {i+1}/{len(lines)}...", flush=True)
        line_text = recognize_text(crop_path)
        full_text += line_text + "\n"

    print("\nRunning LangChain cleanup on raw OCR output...", flush=True)
    cleaned_text = clean_ocr_output(full_text)

    return full_text, cleaned_text


if __name__ == "__main__":
    try:
        test_path = r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting_small_test.jpg"
        raw_text, cleaned_text = hybrid_extract(test_path)

        print("\n--- RAW HYBRID EXTRACTED TEXT ---")
        print(raw_text)

        print("\n--- CLEANED TEXT (after LangChain) ---")
        print(cleaned_text)
    except Exception as e:
        import traceback
        print("SCRIPT CRASHED:")
        traceback.print_exc()