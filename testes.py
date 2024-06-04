from modules import database
from modules.BTree import BTree

dados = database.ler_banco_de_dados()['dados']

# Inicializar a árvore B com grau mínimo 3
b_tree = BTree(3)

# Inserir dados na árvore B
for key, value in dados.items():
    # Convertendo 'valor' e 'status' para o tipo apropriado
    value['valor'] = float(value['valor'])
    value['status'] = bool(value['status'])
    b_tree.insert((int(key), value))

# Listar todos os dados na árvore B
print("LISTAR")
print(b_tree.traverse())

print("\nPROCURAR")
search_key = 4
result = b_tree.search(search_key)
if result:
    print(f"Elemento encontrado: {result}")
else:
    print("Elemento não encontrado")

print("\nFILTROS")
max_value = 10000
print(b_tree.filter_records(max_value=max_value, substring="Test        "))


