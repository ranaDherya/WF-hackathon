
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader

class ValidationRule(BaseModel):
    rule_id: str = Field(..., description="Unique identifier for the validation rule")
    description: str = Field(..., description="Detailed explanation of the requirement")
    impacted_data_fields: List[str] = Field(..., description="List of affected data fields")
    validation_type: str = Field(..., description="Type of validation (e.g., format check, threshold, range, mandatory field)")
    source_regulation: str = Field(..., description="Reference to the specific regulation or section")
    severity: str = Field(..., description="Compliance impact level (e.g., Critical, High, Medium, Low)")
    refinement_notes: Optional[str] = Field(None, description="Additional notes or refinements based on user feedback")

class ComplianceResponse(BaseModel):
    document_name: str = Field(..., description="Name of the compliance document")
    extracted_rules: List[ValidationRule] = Field(..., description="List of extracted data validation rules")

def parse_output(solution):
    """When we add 'include_raw=True' to structured output,
    it will return a dict w 'raw', 'parsed', 'parsing_error'."""

    return solution["parsed"]
extract_profiling_instruction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """<instructions> You are a Risk Compliance Officer. 
            You are given following document as federal government requiremets for banks regarding transactions.
             \n ------- \n  {context} \n ------- \n
            Your task is to exact, interpret and then refine the regulatory instuctions to identify
            the key data validation requirements for provided data fields. 
            Structure your answer as following: 
            ```json\n{schema}\n
            ```
            
            """
        ),
        ("placeholder", "{messages}"),
    ])
class ChatBot:
    def __init__(self, doc, model="gemini-1.5-pro"):
        self.llm = ChatGoogleGenerativeAI(model=model)
        self.structured_llm_profiling = self.llm.with_structured_output(ComplianceResponse, include_raw=True)
        self.code_gen_chain = extract_profiling_instruction_prompt | self.structured_llm_profiling | parse_output
        self.url = doc

        loader = PyPDFLoader(doc)

        data = loader.load()

        # Sort the list based on the URLs and get the text
        self.concatenated_content = "\n\n\n --- \n\n\n".join(
            data[i].page_content for i in range(len(data))
        )

