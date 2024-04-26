import ollama
from ollama import Client

client = Client(host='http://localhost:11434')

text = ""
user_input = "hello"
model = ollama.list()['models'][0]['name']
print(model)
messages = [{'role': 'system', 'content': 'You are an AI assistant who gives a quality response to whatever humans ask of you.'}]

reply = client.chat(model=model, messages=messages,stream=True)
for chunk in reply:
    print(chunk['message']['content'], end='', flush=True)
    text += chunk['message']['content']
messages.append({'role': 'assistant', 'content': text})
print('\n')

while user_input != "bye":
    try:
        user_input = input("Prompt: ")      
        
        messages.append({'role': 'user', 'content': user_input})
        
        reply = client.chat(model=model, messages=messages,stream=True)
        for chunk in reply:
            print(chunk['message']['content'], end='', flush=True)
            text += chunk['message']['content']       
        messages.append({'role': 'assistant', 'content': text})
        print('\n')
        
    except Exception as e:
        print(f"An error occurred: {e}")