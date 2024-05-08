import requests

data = {'id':2,
        'key':'nome',
        'valor':'Teste Alterar'}
response = requests.post("http://127.0.0.1:5000/alterar",data=data)
print(response.content)