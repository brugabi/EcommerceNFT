import io
import json
import zipfile
from modules import database 
from modules.utils import compress_lzw, decompress_lzw
from flask import Flask, render_template, request, jsonify, send_file, redirect

app = Flask(__name__)
carrinho_de_compras_cliente = {}

@app.route('/')
def home():
    # Obter parâmetros de filtro
    min_key = request.args.get('min_key', type=int)
    max_key = request.args.get('max_key', type=int)
    min_value = request.args.get('min_value', type=float)
    max_value = request.args.get('max_value', type=float)
    substring = request.args.get('substring', type=str)

    # Ler e filtrar banco de dados
    b_tree = database.ler_banco_de_dados_arvore_b(min_key=min_key,max_key=max_key,min_value=min_value, max_value=max_value, substring=substring)
    return render_template('index.html', catalogo=b_tree)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html')

@app.route('/download-database')
def download():
    data = database.ler_banco_de_dados()['dados']
    json_data = json.dumps(data)
    byte_data = json_data.encode()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('database.json', byte_data)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='database.zip',
        mimetype='application/zip'
    )

@app.route('/adm')
def adm():
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
        nome = request.form.get('nome')
        valor = float(request.form.get("valor"))
        # blockchain = request.form['blockchain']
        # status = bool(request.form['status'])
        # image_path = None
        # database.inserir_registro(nome=nome, valor=valor, blockchain=blockchain, status=status, image_path=image_path)

        print(nome)
        print(request.form.get('blockchain'),f' {type(request.form.get("blockchain"))}')

        return jsonify({"success": True, "message": "NFT inserido com sucesso"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

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
    
@app.route("/carrinhoDeCompras",methods=['GET'])
def carrinho_de_compras():
    return render_template("carrinhoDeCompras.html",shopCart=carrinho_de_compras_cliente)

@app.route("/inserir_no_carrinho",methods=['POST'])
def inserir_no_carrinho():
    try:
        data = request.get_json()
        id = str(data['id'])
        if carrinho_de_compras_cliente.get(id,None) is not None:
            raise Exception("Você ja tem este produto no seu carrinho! Produto não inserido!")
        
        nft = database.ler_banco_de_dados().get('dados').get(id)
        carrinho_de_compras_cliente[id] = nft

        return jsonify({"success": True, "message": f"Produto inserido no carrinho!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route("/remover_do_carrinho",methods=['POST'])
def remover_do_carrinho():
    try:
        data = request.get_json()
        id = str(data['id'])
        del carrinho_de_compras_cliente[id]

        return jsonify({"success": True, "message": f"Produto removido do carrinho!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)
