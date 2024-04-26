import requests
from openai import OpenAI
import ollama

urls = ["http://localhost:1234","http://localhost:11434"]

def check_url_status(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

server_count = 0
for url in urls:
    if check_url_status(url):
        server_count += 1
        print(f"Connected to {url}")
        break
if server_count == 0:
    print("Could not connect to any server. Exiting...")
    exit(1)
    
url += "/v1"
model = "gpt-3.5-turbo"
try:
    model = ollama.list()['models'][0]['name']
except Exception as e:
        print(f"An error occurred: {e}")
        
# Point to the local server
client = OpenAI(base_url=url, api_key="local_key")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    completion = client.chat.completions.create(
        model=model,
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    user_input = input("> ")
    if user_input == "exit":
        break
    history.append({"role": "user", "content": user_input})