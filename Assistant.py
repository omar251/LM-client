import pyttsx3
import openai

openai.api_type = "open_ai"
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "Whatever"

messages = [{'role': 'system', 'content': 'You are an AI assistant who gives a quality response to whatever humans ask of you.'}]

# Initialize pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

while True:
    try:
        user_input = input("Prompt: ")
        
        messages.append({'role': 'user', 'content': user_input})
        
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages,
            temperature=0.7,
            max_tokens=-1
        )
        print(response.choices[0].message.content)
        text = response.choices[0].message.content
        
        engine.say(text)
        engine.runAndWait()
        
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})
    except Exception as e:
        print(f"An error occurred: {e}")




