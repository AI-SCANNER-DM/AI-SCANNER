from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key="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"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You correct OCR/handwriting extraction errors. Fix spelling, spacing, "
               "and obvious misreads without changing meaning or adding content. "
               "Return only the corrected text."),
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