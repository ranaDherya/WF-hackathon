import pandas as pd
import importlib.util
import os
import ast, json
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import sys
from pydantic_core import from_json
# Define Validation Rule Schema
class ValidationRule(BaseModel):
    rule_id: str
    description: str
    impacted_data_fields: List[str]
    validation_function_name: Optional[str]
    validation_function_argument: Optional[Union[List[int], List[str], List[List[str]]]]
    code: Optional[str]
class ComplianceResponse(BaseModel):
    extracted_rules: List[ValidationRule] = Field(..., description="List of extracted data validation rules")

# Step 1: Write new functions to a Python file
GENERATED_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + ("generated_validations.py")

def write_functions_to_file(rules: ComplianceResponse):
    with open(GENERATED_FILE, "w") as f:
        f.write("# Auto-generated validation functions\n\n")
        # f.write("import re\n\n")  # Add any necessary imports
        for rule in rules.extracted_rules:
            if rule.code:
                f.write(rule.code + "\n\n")

# Step 2: Load the generated module dynamically
def load_generated_module():
    module_name = "generated_validations"
    spec = importlib.util.spec_from_file_location(module_name, GENERATED_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Step 3: Validate a row using reflection
def validate_row(idx, row, rules: ComplianceResponse):
    errors = []
    module = load_generated_module()  # Load dynamically created functions

    for rule in rules.extracted_rules:
        field = rule.impacted_data_fields[0]
        if field in row:
            value = row[field]
            func_name = rule.validation_function_name

            if func_name and hasattr(module, func_name):
                func = getattr(module, func_name)  # Reflection to get function
                args = rule.validation_function_argument or []
                ret_value = func(value, *args)

                if not ret_value and ret_value != "VALID":
                    errors.append(f"Row {idx}:- Validation failed for {field}: {rule.description}")

    return errors

# Step 4: Load Validation Rules from CSV
def load_validation_rules(json_path):
    rules : str
    with open(json_path, "r") as f:
        rules = f.read()
    return ComplianceResponse.model_validate(from_json(rules))

def main(validation_rules, fname):
    write_functions_to_file(validation_rules)

    # Example Data Row
    df = pd.read_csv(fname)

    # Validate Row
    errors = []
    for idx, row in df.iterrows():
        errors.extend(validate_row(idx, row, validation_rules))

    if errors:
        print("Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("All validations passed.")

# Step 5: Main Execution
if __name__ == "__main__":
    validation_rules = load_validation_rules("validation.json")
    fname = sys.argv[1]
    # Generate function file
    main(validation_rules, fname)

