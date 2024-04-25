import ollama

messages = [{'role': 'system', 'content': 'You are an AI assistant who gives a quality response to whatever humans ask of you.'}]
text = ""
user_input = ""
while user_input != "bye":
    try:
        user_input = input("Prompt: ")      
        
        messages.append({'role': 'user', 'content': user_input})
        
        reply = ollama.chat(model='Mistral_7b', messages=messages,stream=True)
        
        for chunk in reply:
            print(chunk['message']['content'], end='', flush=True)
            text += chunk['message']['content']
        
        messages.append({'role': 'assistant', 'content': text})
            
        print('\n')
        
    except Exception as e:
        print(f"An error occurred: {e}")