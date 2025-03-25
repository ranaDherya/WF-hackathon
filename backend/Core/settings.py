import tiktoken
from langchain_mistralai import ChatMistralAI
import uuid

from Core.codegen import save_recall_memory, search_recall_memories, search_document_context
from Core.prompts import code_gen_chain_prompt
from Core.vectorstore import initializeVectorStore

tokenizer = tiktoken.encoding_for_model("gpt-4o")
vecstore = initializeVectorStore("data/FR_Y-14Q20240331_i.pdf", "data/regulatory_db")
model_with_tools = None
def init_codegenllm():
    global model_with_tools
    mistralmodel = ChatMistralAI(
        model="mistral-large-latest")

    tools = [save_recall_memory, search_recall_memories, search_document_context]
    model_with_tools = code_gen_chain_prompt | mistralmodel.bind_tools(tools)
def init():
    init_codegenllm()
