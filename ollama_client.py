import ollama

model = ollama.list()['models'][0]['name']
print(model)
modelfile = ollama.show(model)['modelfile']
print(modelfile)
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
    modelfile = f'    FROM{path}{modelfile}'
    print(modelfile)
    ollama.create(model=model, modelfile=modelfile)

    
