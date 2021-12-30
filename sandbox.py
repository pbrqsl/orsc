import json

path = '_secret.json'




with open(path, 'r') as file:
    content = json.loads(file.read())

print(content['password'])