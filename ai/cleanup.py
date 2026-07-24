from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGroq(
    model="llama-3.1-8b-instant",
   api_key=os.environ["GROQ_API_KEY"]
)


prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You correct OCR/handwriting extraction errors. Fix only obvious spelling "
     "and character-recognition mistakes. Do NOT add, invent, or guess any words, "
     "labels, or content that is not already present in the input. Do NOT add "
     "placeholders like blanks or labels. If a word is unclear, leave it as-is "
     "rather than guessing.\n\n"
     "STRICT OUTPUT RULES:\n"
     "- Output exactly one corrected line for every input line — never two versions of the same line.\n"
     "- Never repeat, restate, or duplicate a phrase, sentence, or line.\n"
     "- Do not include any explanation, preamble, or commentary — only the corrected text.\n"
     "- Preserve the original line breaks and line count exactly."),
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