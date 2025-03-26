from typing import Optional, List, Union

from pydantic import Field, BaseModel


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

my_rules = ComplianceResponse(extracted_rules=[])
