from outlet_chain import outlet_chain

def test_outlet_chain():
    questions = [
        "How many outlets are there in Kuala Lumpur?",
        "List all outlets in Petaling Jaya.",
        "What is the address for the Ekocheras outlet?",
        "Find the outlet names that contain Coffee."
    ]
    for q in questions:
        print(f"Question: {q}")
        answer = outlet_chain(q)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    test_outlet_chain()