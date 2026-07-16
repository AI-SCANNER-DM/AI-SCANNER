# scanner/lines_segment.py

import cv2
import numpy as np


def crop_to_content(gray_image, margin_ratio=0.08):
    h, w = gray_image.shape
    my = int(h * margin_ratio)
    mx = int(w * margin_ratio)
    return gray_image[my:h-my, mx:w-mx]


def segment_lines_robust(gray_image, debug=False):
    cropped = crop_to_content(gray_image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3))
    dilated = cv2.dilate(255 - cropped, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes = sorted(bounding_boxes, key=lambda b: b[1])

    if debug:
        print(f"Total raw contours found: {len(bounding_boxes)}")
        for (x, y, w, h) in bounding_boxes:
            print(f"  box: x={x}, y={y}, w={w}, h={h}")

    line_images = []
    img_h, img_w = cropped.shape
    for (x, y, w, h) in bounding_boxes:
        if w > img_w * 0.1 and 8 < h < 150:
            line_images.append(cropped[y:y+h, x:x+w])

    return line_images


if __name__ == "__main__":
    import os
    from preprocess import preprocess_image

    test_path = r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting_0.jpg"
    processed = preprocess_image(test_path)

    lines = segment_lines_robust(processed, debug=True)
    print(f"Detected {len(lines)} lines")

    os.makedirs("assets/lines_test", exist_ok=True)
    for i, line_img in enumerate(lines):
        cv2.imwrite(f"assets/lines_test/line_{i}.jpg", line_img)

    print("Saved cropped lines to assets/lines_test/")