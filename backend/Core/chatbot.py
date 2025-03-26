
from typing import List, TypedDict
from langchain.docstore.document import Document
from langchain_google_genai import ChatGoogleGenerativeAI

from Core.prompts import get_chatbot_maintemplate, get_chatbot_contextualizequery_template
from Core.vectorstore import getVectorStore



# Extend the state to include chat_history
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    chat_history: List[str]

class MyChatBot:
    def __init__(self):
        self.chat_history = []
        self.vectorstore = getVectorStore("data/regulatory_db")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
        self.main_prompt = get_chatbot_maintemplate()
        self.history_contextualize_prompt = get_chatbot_contextualizequery_template()

    # Application Step 1: Retrieve relevant documents
    def retrieve(self, question) -> dict:
        # Retrieve documents based on similarity search using the question
        self.chat_history += [f"user: {question}"]
        contextualized_query = self.contextualize_query(question)
        retrieved_docs = self.vectorstore.similarity_search(contextualized_query)

        return {"context": retrieved_docs, "question": contextualized_query}

    def contextualize_query(self, query: str):
        """
        Contextualizes the user query based on the conversation history.
        :param query:   The user query
        :param history:    The conversation history
        :return:   The contextualized query
        """
        try:
            message = self.history_contextualize_prompt.invoke({"history": self.chat_history, "query":query})
            response = self.llm.invoke(message)

            return str(response.content)
        except Exception as e:
            print(f"Error contextualizing query: {e}")
            return ""

    # Application Step 2: Generate an answer using the retrieved context and chat history
    def generate(self, query:str):
        # Concatenate the page_content of each document into a single context string
        state = self.retrieve(query)
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])

        # Build messages using a prompt template including question, docs_content, and chat_history_text
        messages = self.main_prompt.invoke({
            "question": state["question"],
            "context": docs_content,
        })
        print(f"Contextualized Query: {state['question']}")

        # Generate a response using the LLM
        response = self.llm.invoke(messages)

        # Append the new conversation turn to the chat history
        new_turn = f"assistant: {response.content}"
        self.chat_history += [new_turn]

        return response.content

# # Compile application graph: sequence of steps with state propagation
# graph_builder = StateGraph(State).add_sequence([retrieve, generate])
# graph_builder.add_edge(START, "retrieve")
# graph = graph_builder.compile()

#