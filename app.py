from flask import Flask, render_template, request, jsonify
from modules import database  # Supondo que você tem um módulo de banco de dados

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',catalogo=database.ler_banco_de_dados()['dados'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html')

@app.route('/return-file')
def return_file():
    # Lógica para retorno de arquivo
    return "Arquivo"

@app.route('/adm')
def adm():
    return render_template('crud.html')

@app.route('/crud')
def crud():
    return render_template('crud.html')

@app.route('/get-nfts', methods=['GET'])
def get_nfts():
    try:
        nfts = database.ler_banco_de_dados()['dados']
        nft_list = [{'id': key, **value} for key, value in nfts.items()]
        return jsonify(nft_list)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/insert', methods=['POST'])
def insert():
    try:
        nome = request.form['nome']
        valor = request.form['valor']
        blockchain = request.form['blockchain']
        status = bool(request.form['status'])
        image_path = None
        database.inserir_registro(nome=nome, valor=valor, blockchain=blockchain, status=status, image_path=image_path)

        return {"success": True, "message": "NFT inserido com sucesso"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.route('/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        id = data['id']
        database.remover_registro(id=id)
        return {"success": True, "message": f"O NFT {id} foi deletado com sucesso!"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.route('/alterar', methods=['POST'])
def alterar():
    try:
        data = request.get_json()
        id = data['id']
        key = data['key']
        valor = data['valor']
        database.alterar_registro(id=id, key=key, valor=valor)
        return {"success": True, "message": f"O NFT {id} foi alterado com sucesso!"}
    except Exception as e:
        return {"success": False, "message": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
