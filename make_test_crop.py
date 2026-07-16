import cv2

img = cv2.imread(r"C:\Users\Admin\OneDrive\Desktop\Ai_digitalised_document_scanner\assets\handwriting_0.jpg")
small_crop = img[150:500, :]   # skip the header box, capture real handwriting lines
cv2.imwrite("assets/handwriting_small_test.jpg", small_crop)
print("Small test crop saved to assets/handwriting_small_test.jpg")