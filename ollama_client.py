import ollama
import os
import math


class GetModels:
    def __init__(self, folder_path):
        if not os.path.exists(folder_path):
            raise ValueError("Folder path does not exist")
        if not os.path.isdir(folder_path):
            raise ValueError("Folder path is not a directory")
        self.folder_path = folder_path

    def bytes_to_human_readable(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    
    def get_folder_contents(self, path=None):
        if path is None:
            path = self.folder_path
        contents = os.listdir(path)
        return contents

    def calculate_size(self, path):
        if os.path.isfile(path):
            return os.path.getsize(path)
        total_size = 0
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                total_size += os.path.getsize(item_path)
            elif os.path.isdir(item_path):
                total_size += self.calculate_size(item_path)
        return total_size

    def select_model(self):
        contents = self.get_folder_contents()
        print("Available models in the folder:")
        for n, item in enumerate(contents, start=1):
            item_path = os.path.join(self.folder_path, item)
            item_size = self.calculate_size(item_path)
            print(f"{n}. {item} - {self.bytes_to_human_readable(item_size)}")

        while True:
            selection = input("Select model number: ")
            try:
                model_number = int(selection) - 1
                if 0 <= model_number < len(contents):
                    model_name = contents[model_number]
                    model_path = os.path.join(self.folder_path, model_name)
                    model = self.get_folder_contents(model_path)[0]
                    model_path = os.path.join(model_path, model)
                    model_size = self.calculate_size(model_path)
                    return model_name, model_path, self.bytes_to_human_readable(model_size)
                else:
                    print("Invalid selection. Please enter a valid model number.")
            except ValueError:
                print("Invalid selection. Please enter a valid model number.")

folder_path = r"C:\Users\pc\Documents\MyData\LLM_models\models\TheBloke"
get_models = GetModels(folder_path)
model_name, model_path, model_size = get_models.select_model()
print(f"Model Name: {model_name}")
print(f"Model Path: {model_path}")
print(f"Model Size: {model_size}")

model_name = input("Enter model name: ")
print(model_name, model_path)

def create(model='new_model', path=''):
    modelfile ='''
TEMPLATE """
<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|> user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
'''
    modelfile = f'FROM {path}{modelfile}'
    print(modelfile)
    ollama.create(model=model, modelfile=modelfile)


# modelfile = ollama.show(model)['modelfile']
# print(modelfile)
yn = input("Do you want to create a new model? (y/n)")
if yn == 'y':
    create(model_name,model_path)

models = ollama.list()
for model in models['models']:
    print('- ',model['name'])
    model = model['name']
