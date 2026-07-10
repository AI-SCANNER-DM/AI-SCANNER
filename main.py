from ai.trocr import recognize_text

text = recognize_text(
    "assets/handwriting.jpg"
)

print("\nRecognized Text:\n")
print(text)