import os
import json
from modules.utils import agora

def create_database():
    '''
    '''

    if os.path.exists('database.json'):
        print("Base de dados existe!!")
    else:
        print("Base da dados não existe, então iremos criar uma!!")
        dictionary = {
            'atualizacao': agora(),
            'dados':{}
        }
        with open('database.json','w') as data_file:
            data_file.write(json.dumps(dictionary,indent=1))

def ler_banco_de_dados():
    with open('database.json','r') as database_file:
        data_dict = json.load(database_file)
    return data_dict

def inserir(item:dict):
    '''
    '''

    if isinstance(item,dict) is not True:
        raise ValueError("O valor inserido deve ser um dicionário!!")
    
    if os.path.exists('database.json') is not True:
        create_database()

    # Abrindo o banco de dados para inserção
    with open('database.json','r') as database_file:
        data_dict = json.load(database_file)

    # Inserindo o dado na base de dados
    try:
        # Gerando o id
        if len(data_dict['dados']) == 0:
            id = 1
        else:
            id = int(list(data_dict['dados'].keys())[-1]) + 1
        
        # Inserindo o dicionario
        data_dict['dados'][id] = item
        data_dict['atualizacao'] = agora()
        print("Item inserido com sucesso!")
    except Exception as e:
        raise Exception(f"Erro ao inserir o item na base de dados: {e}")
    
    # Salvando a base de dados
    salvar_dados(data_dict)

def salvar_dados(data_dict):
    try:
        with open('database.json','w') as database_file:
            database_file.write(json.dumps(data_dict,indent=1))
    except Exception as e:
        raise Exception(f"Erro ao salvar a base de dados: {e}")
    
def ler_registro(id:int):
    '''
    '''
    #Abrindo o banco de dados para inserção
    data_dict = ler_banco_de_dados()

    return data_dict['dados'].get(str(id))

def remover_registro(id: int):
    '''
    teste
    '''
    data_dict = ler_banco_de_dados()
    del data_dict['dados'][str(id)]
    salvar_dados(data_dict)

def alterar_registro(id: int, key: str, valor:any):
    '''
    alterar'''

    data_dict = ler_banco_de_dados()
    data_dict['dados'][str(id)][key] = valor
    salvar_dados(data_dict)