import json
from difflib import get_close_matches

def load_knowledge_base(file_path:str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data : dict = json.load(f)
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {"question": [], "answer": []}

def save_knowledge_base(file_path:str, data:dict) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f , indent=2)

def add_to_knowledge_base(file_path:str, question:str, answer:str) -> None:
    data = load_knowledge_base(file_path)
    data['question'].append(question)
    data['answer'].append(answer)
    save_knowledge_base(file_path, data)

def find_best_match(user_question:str,questions:list) -> str or None:
    best_match = get_close_matches(user_question, questions , n=1, cutoff=0.6)
    if best_match:
        return best_match[0] if best_match[0] else None

def get_answer(user_question:str, data:dict) -> str or None:
    if user_question in data['question']:
        index = data['question'].index(user_question)
        return data['answer'][index]
    else:
        return None

def chatbot():
    file_path = 'knowlage_base.json'
    data = load_knowledge_base(file_path)
    while True:
        user_question = input("Ask me a question: ")
        if user_question.lower() == 'quit':
            break
        answer = get_answer(user_question, data)
        if answer is not None:
            print(f"Answer: {answer}")
        else:
            print("I don't know the answer to that question.")
            user_answer = input("What is the answer to your question? ")
            add_to_knowledge_base(file_path, user_question, user_answer)
            data = load_knowledge_base(file_path) 

if __name__ == "__main__":
    chatbot()