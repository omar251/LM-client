import ollama
from ollama import Client

client = Client(host='http://localhost:11434')

model = ollama.list()['models'][0]['name']
print(model)
history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    try:
        reply = client.chat(model=model, messages=history,stream=True)
        new_message = {"role": "assistant", "content": ""}
        
        for chunk in reply:
            print(chunk['message']['content'], end='', flush=True)
            new_message["content"] += chunk['message']['content']
             
        history.append(new_message)    
        print()
        user_input = input("> ")
        if user_input == "exit":
            break
        history.append({"role": "user", "content": user_input})
        
    except Exception as e:
        print(f"An error occurred: {e}")