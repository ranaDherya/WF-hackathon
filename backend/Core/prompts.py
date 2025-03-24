from langchain.prompts import PromptTemplate

chatbot_main_template_str = """
You are a compliance assistant helping auditor in creating
    profiling rule for bank transaction data based on regulatory reporting instructions.
Retrieved Context:
{context}

Question: {question}
Answer:
"""

chatbot_contextualize_query_template_str = """
            You are a helpful assistant that contextualizes the user query depending on the previous conversation 
                    queries only if required
            Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if and only if needed and otherwise return it as is. \
            History: {history}
            Latest query: {query}

            ANSWER: """
def get_chatbot_maintemplate():
    return PromptTemplate(template=chatbot_main_template_str, input_variables=["context", "chat_history", "question"])

def get_chatbot_contextualizequery_template():
    return PromptTemplate(template=chatbot_contextualize_query_template_str, input_variables=["history", "query"])

