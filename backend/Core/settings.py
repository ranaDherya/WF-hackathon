import tiktoken
from langchain_mistralai import ChatMistralAI

from Core.vectorstore import initializeVectorStore

tokenizer = tiktoken.encoding_for_model("gpt-4o")
vecstore = initializeVectorStore("data/FR_Y-14Q20240331_i.pdf", "data/regulatory_db")
