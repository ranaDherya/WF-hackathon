import pandas as pd

from Core.codegen import generate_rules

from Core.codeexecution import code_execution
import pandas
fname = "data.csv"

df = pd.read_csv(fname, skipinitialspace=True)
columns =  list(df.columns)

temp = generate_rules(columns)
print(temp)

# code_execution(, df)
