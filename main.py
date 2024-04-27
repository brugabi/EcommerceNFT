import modules.database as database

dado = {'nome':'Bruninha',
        'profissao':'teste'}

database.inserir(item=dado)

#print(database.ler_registro(16))
#database.remover_registro(16)
print(database.ler_registro(17))
database.alterar_registro(17,'profissao','cafetao')
print(database.ler_registro(17))
