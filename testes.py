import json
from modules import database

# Testando a função
resultados = database.ler_banco_de_dados_arvore_b(min_key=4, max_key=8, min_value=10000, substring="Test")
print("Registros filtrados:", json.dumps(resultados,indent=2))