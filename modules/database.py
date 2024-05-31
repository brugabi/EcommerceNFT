import os
import json
from zipfile import ZipFile
from modules.utils import agora,log

def create_database():
    '''
    '''

    if os.path.exists('database.json'):
        log("Base de dados existe!!")
    else:
        log("Base da dados não existe, então iremos criar uma!!")
        dictionary = {
            'atualizacao': agora(),
            'dados':{}
        }
        with open('database.json','w') as data_file:
            data_file.write(json.dumps(dictionary,indent=1))

def ler_banco_de_dados() -> dict:
    with open('database.json','r') as database_file:
        data_dict = json.load(database_file)
    return data_dict

def inserir_registro(nome:str,valor:float,blockchain:str,status:bool,image_path:str):
    '''
    '''
    
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
        item = {
            'nome':nome,
            'valor':valor,
            "blockchain":blockchain,
            "status":status,
            "image":image_path
        }
        data_dict['dados'][id] = item
        data_dict['atualizacao'] = agora()

        # Salvando a base de dados
        salvar_dados(data_dict)

        log("Item inserido com sucesso!")
    except Exception as e:
        raise Exception(f"Erro ao inserir o item na base de dados: {e}")

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
    try:
        data_dict = ler_banco_de_dados()
        if data_dict['dados'].pop(str(id),None) is None:
            raise Exception("O id informado nao existe na nossa base de dados!")  
        salvar_dados(data_dict)
    except Exception as e:
            raise e

def alterar_registro(id: int, key: str, valor:any):
    '''
    alterar'''
    try:
        data_dict = ler_banco_de_dados()
        
        if id not in list(data_dict['dados'].keys()): # Verificando se é uma id Válida
            raise Exception("O id não encontrado.")
        
        if key not in list(data_dict['dados'][str(id)].keys()):
            raise Exception(f"A key {key} nao e uma key valida.")
        
        data_dict['dados'][str(id)][key] = valor
        salvar_dados(data_dict)
    except Exception as e:
        raise e

def exportar_base_de_dados():
    """
    Descrição
    ---------
    Função para exportar a base da dados para o diretório Download.
    Em caso de já existir uma arquivo com o nome data_exported.zip, o caso será tratado.

    Args
    ----
    None.

    Return
    ------
    None.

    Raise
    -----
    Exception.
    """

    log("Extraindo o caminho da pasta download.")
    user_download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

    base_filename = 'data_exported.zip'  # Base filename for the ZIP file
    full_zip_path = os.path.join(user_download_dir, base_filename)

    # Check if the file already exists
    counter = 1
    while os.path.exists(full_zip_path):
        full_zip_path = os.path.join(user_download_dir, f"{base_filename[:-4]}({counter}).zip")
        counter += 1

    log(f"Salvando o arquivo em {full_zip_path}")

    try:
        with ZipFile(full_zip_path, 'w') as zip_file:
            zip_file.write('database.json')

        log("Arquivo salvo com sucesso!")
    except Exception as e:
        log(f"Erro ao criar o arquivo zip: {e}")
        raise e
    
    return zip_file

