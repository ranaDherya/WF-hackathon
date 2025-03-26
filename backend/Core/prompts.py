from langchain.prompts import PromptTemplate, ChatPromptTemplate

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

code_gen_chain_prompt = ChatPromptTemplate.from_messages([("""
  "system",
You are an expert python developer you have vast experience in profiling data
which are used for regulatory reporting. In this task you will be provided with column names.
Your task is to generate code for all the validation rules pertainin to these columns
1. You are given tool called search_document_context which can be used to extract validation requirement
from regulatory document.
2. You have to give special attention on allowed_values column. In most cases
this column will be enough.
3.Some example of allowed_values column 
a.{{Rounded whole dollar amount,
e.g.: 20000000
Supply numeric values without
any non- numeric formatting
(no dollar sign, commas or
decimal).}} this can be interpreted as regex pattern for whole number ,
b. Must be in yyyy- mm-dd format,e.g.: 2005-02-01:- can be interpreted
as date validation.
c. Similarly 2 character country code :- can be interpreted as regex pattern for city code.
d. Enter number code of the description:- check description to find out allowable code value
 usually 1-n function will be integer range checker which takes two additional parameter of min and max
e. one of the given 1.value 2.value1 3.value2 4.value3 so our function will take list of allowed value
as argument and can check if it exists 
4. For many of the fields this allowed_values is same or similar hence
it makes sense to have common function for similar validations i.e for all regex validation
we can call regex_validator function with data and pattern as parameter.
5.You are writing in new file. At first you don't have any function so
you have to generate a function with relevan imports to validate that requirements.
Keep the funciton simple enough so that other similar reuirements can be validated by same function
6.Next time you can just reference the same function by name.
7. Remember reporting is most important so your validation rules must include nice description
which can be used to create a informed error message for the cause of failing of rule.
8. For now you can ignore validation rules recquiring more than one field
 "Recall memories are contextually retrieved based on the current"
9. Please don't write any rule which is not required
10. Write all the rules which are required.
11. You can retrieve context for each column separately for better context
12. Each function will be called on one row of pandas dataframe
13. You can call search_recall_memories to check if such validation function is already 
generated hence just name can be provided in this case code will be null.
14. Your code should contain only one function. Code to apply this function will 
be written later
" conversation:\n{recall_memories}\n\n"

"Memory Usage Guidelines:\n"
            "1. Actively use memory tools (search_recall_memories, save_recall_memory)"
            " to build a comprehensive understanding of the code.\n"
            "2. Make informed suppositions and extrapolations based on stored"
            " memories.\n"
            "3. Regularly reflect on past interactions to identify patterns and"
            " preferences.\n"
            4. Don't assume anything

Input data is in csv file which will be loaded in memory as pandas data frame
Follow the output structure rigorously

Output Instuction:
***Important when you are calling tools skip these output instructions call tools***
Output will be list 
For each rule you will output in json format :
  rule_id: str = Field(..., description="Unique identifier for the validation rule")
    description: str = Field(..., description="Detailed explanation of the requirement")
    impacted_data_fields: List[str] = Field(..., description="List of affected data fields")
    validation_function_name: str = Field(..., description="Function from chat history you are using to validate this rool or function name from code if code is not empty")
    validation_function_argument: Optional[Union[List[int], List[str]] ]  =  Field(..., description="Extra aruments needed for function for.eg"
    "for regex validator it will be regex pattern, for range validator it will be min and max value")
    code: Optional[str] = Field(..., description="import statement and function without any main method. This function will be used later by main method")
eg output:
[{{"rule_id": "rule1", "description":"impacted_data_fields":["field1", "field2"], "validation_function_name": "func", "validation_function_argument":[1,2],"code":"#some_code" }}]
"""),("placeholder", "{messages}")])

code_ge_prompt_with_tools_to_register_rules = ChatPromptTemplate.from_messages([(
    "system",
    """
  You are an expert python developer you have vast experience in profiling data
  which are used for regulatory reporting. In this task you will be provided with column names.
  Your task is to generate code for all the validation rules pertainin to these columns
  1. You are given tool called search_document_context which can be used to extract validation requirement
  from regulatory document.
  2. You have to give special attention on allowed_values column. In most cases
  this column will be enough.
  3.Some example of allowed_values column 
  a.{{Rounded whole dollar amount,
  e.g.: 20000000
  Supply numeric values without
  any non- numeric formatting
  (no dollar sign, commas or
  decimal).}} this can be interpreted as regex pattern for whole number ,
  b. Must be in yyyy- mm-dd format,e.g.: 2005-02-01:- can be interpreted
  as date validation.
  c. Similarly 2 character country code :- can be interpreted as regex pattern for city code.
  d. Enter number code of the description:- check description to find out allowable code value
   usually 1-n function will be integer range checker which takes two additional parameter of min and max
  e. one of the given 1.value 2.value1 3.value2 4.value3 so our function will take list of allowed value
  as argument and can check if it exists 
  f. value must be valid code as given in description use in_range min value 1 max value x 
  highest code in description
  4. You have to register each rule by calling corresponding tool description is what will be printed if the
  valdation fails example 'field x Should be integer' 
  5. Remember reporting is most important so your validation rules must include nice description
  which can be used to create a informed error message for the cause of failing of rule.
  6. For now you can ignore validation rules requiring more than one field
  7. Please don't register any rule which is not required
  8. Don't make any assumption about the rule
  9. You can retrieve context for each column separately for better context
  10. You should call registration tool once each for each rule:
    field_name:  field_name ,description : brief rule description
  11. You must batch your rule registration tool call so as not to exceed api limit
  12. For most of the field you have to call atleast one registration tool
  13. Please don't call tool twice for same rule and column
   Recall memories are contextually retrieved based on the current
  conversation:\n{recall_memories}\n\n
  
  "Memory Usage Guidelines:\n"
              "1. Actively use memory tools (search_recall_memories, save_recall_memory)"
              " to build a comprehensive understanding of the code.\n"
              "2. Make informed suppositions and extrapolations based on stored"
              " memories.\n"
              "3. Regularly reflect on past interactions to identify patterns and"
              " preferences.\n"
              4. Don't assume anything
  
  """),("placeholder", "{messages}")])
