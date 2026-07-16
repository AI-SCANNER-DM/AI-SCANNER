from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

MODEL_NAME = "Cdywalst/donut-base-handwriting_recognition"

processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

image = Image.open("assets/handwriting.jpg").convert("RGB")

pixel_values = processor(
    image,
    return_tensors="pt"
).pixel_values.to(device)

outputs = model.generate(pixel_values)

result = processor.batch_decode(
    outputs,
    skip_special_tokens=True
)[0]

print("\nDONUT RESULT:\n")
print(result)