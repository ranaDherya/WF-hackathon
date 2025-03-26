from Core.codegen import get_graph
from Core.utility import getApiKey

getApiKey()
graph = get_graph()
config = {"configurable": {"user_id": "1", "thread_id": "1"}, "recursion_limit":50}
message = "Field for corporate loan schedule Country, City, OriginationDate, MaturityDate, FacilityType"
_ = graph.invoke({"messages": [("user", message)], "recall_memories" :[]}, config=config)