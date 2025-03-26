import pandas as pd
import importlib.util
import os
import ast, json
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import sys
from pydantic_core import from_json

from Core.codegen import ComplianceResponse
from generated_validations import *
# Define Validation Rule Schema

# Step 1: Write new functions to a Python file
# GENERATED_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + ("generated_validations.py")

# Step 2: Load the generated module dynamically
# def load_generated_module():
#     module_name = "generated_validations"
#     spec = importlib.util.spec_from_file_location(module_name, GENERATED_FILE)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     return module
def get_function(name):
    if name == "is_integer":
        return is_integer
    if name == "is_whole_number":
        return is_whole_number
    if name == "is_in_range":
        return is_in_range
    if name == "matches_pattern":
        return matches_pattern
    if name == "is_in_list":
        return is_in_list
    if name == "is_valid_date":
        return is_valid_date
    return None

# Step 3: Validate a row using reflection
def validate_row(idx, row, rules: ComplianceResponse):
    errors = []
    # module = load_generated_module()  # Load dynamically created functions

    for rule in rules.extracted_rules:
        field = rule.field_name
        if field in row:
            value = row[field]
            func_name = rule.validation_function_name


            func = get_function(func_name)  # Reflection to get function
            if func is None:
                print(f"Function {func_name} not found")
                continue
            args = rule.arguments or []
            ret_value = func(value, *args)
            if not ret_value:
                errors.append(f"{idx}, {field}, {value}, {rule.description}")

    return errors

# Step 4: Load Validation Rules from CSV
def load_validation_rules(json_path):
    rules : str
    with open(json_path, "r") as f:
        rules = f.read()
    return ComplianceResponse.model_validate(from_json(rules))

def code_execution(validation_rules, df):
    # Example Data Row
    # Validate Row
    errors = ["index, field, value, error"]
    for idx, row in df.iterrows():
        errors.extend(validate_row(idx, row, validation_rules))

    if errors:
        print("Validation Errors:")
        with open("data/temp/validation_errors.csv", "w") as f:
            for error in errors:
                f.writelines(error)
    else:
        print("All validations passed.")

# # Step 5: Main Execution
# if __name__ == "__main__":
#     validation_rules = load_validation_rules("validation.json")
#     fname = sys.argv[1]
#     # Generate function file
#     df = pd.read_csv(fname, skipinitialspace=True)
#     code_execution(validation_rules, df)

