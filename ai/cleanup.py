from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="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"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You correct OCR/handwriting extraction errors. Fix only obvious spelling "
               "and character-recognition mistakes. Do NOT add, invent, or guess any words, "
               "labels, or content that is not already present in the input. Do NOT add "
               "placeholders like blanks or labels. If a word is unclear, leave it as-is "
               "rather than guessing. Return only the corrected text, preserving line breaks."),
    ("human", "{raw_text}")
])

cleanup_chain = prompt | llm | StrOutputParser()

def clean_ocr_output(raw_text: str) -> str:
    return cleanup_chain.invoke({"raw_text": raw_text})


if __name__ == "__main__":
    sample_text = "Th1s is a smaple 0f messsy OCR output."
    cleaned = clean_ocr_output(sample_text)
    print("Original: ", sample_text)
    print("Cleaned:  ", cleaned)