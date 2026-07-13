from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatAnthropic(model="claude-sonnet-4-5", api_key="YOUR_KEY")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You correct OCR/handwriting extraction errors. Fix spelling, spacing, "
               "and obvious misreads without changing meaning or adding content. "
               "Return only the corrected text."),
    ("human", "{raw_text}")
])

cleanup_chain = prompt | llm | StrOutputParser()

def clean_ocr_output(raw_text: str) -> str:
    return cleanup_chain.invoke({"raw_text": raw_text})