import os
import time
import uuid

from langchain_core.documents import Document
from langchain_core.messages import get_buffer_string
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Annotated

from Core.prompts import code_gen_chain_prompt, code_ge_prompt_with_tools_to_register_rules
from Core.settings import vecstore, tokenizer
from Core.utility import getApiKey


# Data model
class ValidationRule(BaseModel):
    description: str = Field(..., description="Detailed explanation of the requirement")
    field_name: str = Field(..., description="field name")
    validation_function_name: str = Field(...,
                                          description="Function from chat history which can be used for this or generated"
                                                      "function name from code")
    arguments: Optional[Union[List[int], List[str], List[List[str]]]] = Field(...,
                                                                              description="Extra aruments needed for function for.eg"
                                                                                          "for regex validator it will be regex pattern, for range validator it will be min and max value")
    code: Optional[str] = Field(None,
                                description="import statement and function without any main method. This function will be used later by main method")


class ComplianceResponse(BaseModel):
    """Respond to the user with this"""
    extracted_rules: List[ValidationRule] = Field(..., description="List of extracted data validation rules")


@tool
def save_recall_memory(memory: str) -> str:
    """Save memory to vectorstore for later semantic retrieval."""
    # user_id = get_user_id(config)
    document = Document(
        page_content=memory, metadata={"source": "history"}, id=str(uuid.uuid4())  # , metadata={"user_id": user_id}
    )
    vecstore.add_documents([document])
    return memory


@tool
def search_recall_memories(query: str) -> List[str]:
    """Search for relevant memories."""

    # user_id = get_user_id(config)

    def _filter_function(metadata) -> bool:
        return metadata.get("source") == "history"

    documents = vecstore.similarity_search(
        query, k=3, filter=_filter_function
    )
    return [document.page_content for document in documents]


@tool
def search_document_context(query: str) -> List[str]:
    """Search for relevant context from regulatory documents."""

    def _filter_function(metadata) -> bool:
        return metadata.get("source") == "table"

    documents = vecstore.similarity_search(
        query, k=1, filter=_filter_function
    )
    return [document.page_content for document in documents]


class State(MessagesState):
    # add memories that will be retrieved based on the conversation context
    recall_memories: List[str]


def agent(state: State) -> State:
    """Process the current state and generate a response using the LLM.

    Args:
        state (schemas.State): The current state of the conversation.

    Returns:
        schemas.State: The updated state with the agent's response.
    """
    bound = model_with_tools
    recall_str = (
            "<recall_memory>\n" + "\n".join(state["recall_memories"]) + "\n</recall_memory>"
    )
    prediction: ComplianceResponse = bound.invoke(
        {
            "messages": state["messages"],
            "recall_memories": recall_str,
        }
    )

    return {
        "messages": [prediction],
    }


def load_memories(state: State, config: RunnableConfig) -> State:
    """Load memories for the current conversation.

    Args:
        state (schemas.State): The current state of the conversation.
        config (RunnableConfig): The runtime configuration for the agent.

    Returns:
        State: The updated state with loaded memories.
    """

    convo_str = get_buffer_string(state["messages"])
    convo_str = tokenizer.decode(tokenizer.encode(convo_str)[:2048])
    recall_memories = search_recall_memories.invoke(convo_str, config)
    # print(f"RecallMemories:- {recall_memories}")
    return {
        "recall_memories": recall_memories,
    }


from pydantic_core import from_json


def extract_response(text: str) -> ComplianceResponse | None:
    """Extracts JSON content from a string wrapped with ```json...```"""
    try:
        json_str = "{\"extracted_rules\":" + text + "}"
        # json_str = re.sub(r"\\n", "\n", json_str)
        # json_str = "".join(ch for ch in json_str if unicodedata.category(ch)[0]!="C")
        return ComplianceResponse.model_validate(from_json(json_str))  # Convert string to dict
    except:
        print(f"Failed to parse :- {text}")
        return None


def parse_message(message) -> bool:
    response_obj = extract_response(message.content)
    if response_obj is None:
        return False
    # all_rule.extracted_rules.extend(response_obj.extracted_rules)
    return True


def route_tools(state: State):
    """Determine whether to use tools or end the conversation based on the last message.

    Args:
        state (schemas.State): The current state of the conversation.

    Returns:
        Literal["tools", "__end__"]: The next step in the graph.
    """
    msg = state["messages"][-1]
    if msg.tool_calls:
        return "tools"
    # elif parse_message(msg) == False:
    #     return "parseerror"
    return END


def get_graph():
    # Create the graph and add nodes
    builder = StateGraph(State)
    builder.add_node(load_memories)
    builder.add_node(agent)
    tools = [save_recall_memory, search_recall_memories, search_document_context]
    builder.add_node("tools", ToolNode(tools))
    # builder.add_node("parseerror", solve_parse_error)
    # Add edges to the graph
    builder.add_edge(START, "load_memories")
    builder.add_edge("load_memories", "agent")
    builder.add_conditional_edges("agent", route_tools, ["tools", "agent", END])
    builder.add_edge("tools", "agent")
    # builder.add_edge("parseerror", "agent")
    # Compile the graph
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


def generate_rules(fields: List[str]):
    global my_rules
    my_rules = ComplianceResponse(extracted_rules=[])
    config = {"configurable": {"user_id": "1", "thread_id": "1"}, "recursion_limit": 100}
    graph = get_graph()
    step = 7

    for i in range(0, len(fields), step):
        message = "Field for corporate loan schedule {}".format(', '.join(fields[i:i + step]))
        print(f"{message}")
        graph.invoke({"messages": [("user", message)], "recall_memories": []}, config=config)
        time.sleep(2)
    return my_rules


@tool
def is_integer(field_name: str, description: Annotated[str, "description of the rule"]) -> str:
    """Regester integer check for field_name"""
    my_rules.extracted_rules.append(ValidationRule(field_name=field_name,
                                                   description=description, validation_function_name=
                                                   "is_integer"))

    return f"Successfully registered rule for {field_name} with validation function is_integer."


@tool
def is_whole_number(field_name: str, description: str) -> str:
    """Register whole number check for field_name"""
    my_rules.extracted_rules.append(ValidationRule(field_name=field_name, description=description,
                                                   validation_function_name=
                                                   "is_whole_number"))
    return f"Successfully registered rule for {field_name} with validation function  is_whole_number."


@tool
def is_in_range(field_name: str, description: str, min_v: int, max_v: int) -> str:
    """Register whole number check for field_name"""
    my_rules.extracted_rules.append(ValidationRule(field_name=field_name, description=description,
                                                   validation_function_name=
                                                   "is_in_range", arguments=[min_v, max_v]))
    return f"Successfully registered rule for {field_name} with validation function  is_in_range."


@tool
def matches_pattern(field_name: str, description: str, pattern: List[str]) -> str:
    """Register regex pattern check """
    my_rules.extracted_rules.append(ValidationRule(field_name=field_name, description=description,
                                                   validation_function_name=
                                                   "matches_pattern", arguments=[pattern]))
    print(my_rules.extracted_rules)
    return f"Successfully registered rule for {field_name} with validation function matches_pattern."


@tool
def is_in_list(field_name: str, description: str, allowed_values: List[str]) -> str:
    """Register is in list check"""
    my_rules.extracted_rules.append(ValidationRule(field_name=field_name, description=description,
                                                   validation_function_name=
                                                   "is_in_list", arguments=[allowed_values]))
    return f"Successfully registered rule for {field_name} with validation function is_in_list."


@tool
def is_valid_date(field_name: str, description: str, format: str) -> str:
    """Register is valid date format check"""
    my_rules.extracted_rules.append(
        ValidationRule(field_name=field_name, description=description, validation_function_name=
        "is_valid_date"))
    return f"Successfully registered rule for {field_name} with validation function is_valid_date. "


registration_rules = [is_integer, is_in_list, is_whole_number, is_valid_date,
                      matches_pattern, is_in_range]


def solve_parse_error(state: State):
    return {"messages": [("user", "You should have invoked tools instead of giving json repsonse")]}


getApiKey()

rate_limiter = InMemoryRateLimiter(
    requests_per_second=.25,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.5,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)
# model = ChatMistralAI(
#     model="mistral-large-latest", api_key=os.environ["MISTRAL_API_KEY"])
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=os.environ["GOOGLE_API_KEY"],
                               rate_limiter=rate_limiter)

my_rules = ComplianceResponse(extracted_rules=[])
tools = [save_recall_memory, search_recall_memories, search_document_context]
tools.extend(registration_rules)
model_with_tools = code_ge_prompt_with_tools_to_register_rules | model.bind_tools(tools)
