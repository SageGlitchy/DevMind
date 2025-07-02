from core.intent import infer_intent

while True:
    query = input("Query: ")
    print("Intent:", infer_intent(query))