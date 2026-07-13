import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    
    coords = np.column_stack(np.where(binary > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = binary.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC)
    
    return deskewed
if __name__ == "__main__":
    test_path = r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting.jpg"
    result = preprocess_image(test_path)
    cv2.imwrite(r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting.jpg", result)
    print("Preprocessing done — check assets/test_output.jpg")