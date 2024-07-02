import io
import json
import folium
import zipfile
import os
from modules import database
from modules.graph import calcular_distancia
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
cliente = {
    'carrinho':{},
    'total_compra':0,
    'distancia_frete':0,
    'tempo':0
}

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # Ler os dados do banco de dados
        nfts = database.ler_banco_de_dados()['dados']
        
        # Criar a lista de NFTs
        nft_list = [{'id': key, **value} for key, value in nfts.items()]
        
        # Retornar a lista como JSON
        return jsonify(nft_list)
    except Exception as e:
        # Em caso de erro, retornar uma mensagem de erro
        return jsonify({"success": False, "message": str(e)})


@app.route('/insert', methods=['POST'])
def insert():
    try:
        nome = request.form['nome']
        valor = float(request.form['valor'])
        blockchain = request.form['blockchain']
        status = request.form['status']
        file = request.files['imagem']
        
        # Salvar a imagem
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        database.inserir_registro(nome=nome, valor=valor, blockchain=blockchain, status=status, image_path=image_url)
        
        
        return jsonify({"success": True, "message": "O NFT foi inserido com sucesso!", "image_url": image_url})
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
        if not data:
            return jsonify({"success": False, "message": "Nenhum dado fornecido."}), 400

        id = data.get('id')
        if not id:
            return jsonify({"success": False, "message": "ID não fornecido."}), 400

        nome = data.get('nome')
        valor = data.get('valor')
        blockchain = data.get('blockchain')
        status = data.get('status')

        # Atualizar cada campo se estiver presente
        if nome is not None:
            database.alterar_registro(id=id, key='nome', valor=nome)
        if valor is not None:
            database.alterar_registro(id=id, key='valor', valor=float(valor))
        if blockchain is not None:
            database.alterar_registro(id=id, key='blockchain', valor=blockchain)
        if status is not None:
            database.alterar_registro(id=id, key='status', valor=status)

        return jsonify({"success": True, "message": f"O NFT {id} foi alterado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route("/carrinhoDeCompras",methods=['GET'])
def carrinho_de_compras():
    return render_template("carrinhoDeCompras.html",shopCart=cliente['carrinho'])

@app.route("/inserir_no_carrinho",methods=['POST'])
def inserir_no_carrinho():
    try:
        data = request.get_json()
        print(data)
        id = str(data['id'])
        if cliente['carrinho'].get(id,None) is not None:
            raise Exception("Você ja tem este produto no seu carrinho! Produto não inserido!")
        nft = database.ler_banco_de_dados().get('dados').get(id)
        cliente['carrinho'][id] = nft
        cliente['total_compra'] = cliente['total_compra'] +  database.ler_banco_de_dados().get('dados').get(id).get('valor')

        print(cliente['total_compra'])
        
        return jsonify({"success": True, "message": f"Produto inserido no carrinho!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route("/remover_do_carrinho",methods=['POST', 'GET'])
def remover_do_carrinho():
    
    try:
        data = request.get_json()
        id = str(data['id'])
        produto_removido = cliente['carrinho'].pop(id)
        cliente['total_compra'] = cliente['total_compra'] - produto_removido.get('valor')
        return jsonify({"success": True, "message": f"Produto removido do carrinho!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@app.route("/get-ids",methods=['GET'])
def get_ids():
    return jsonify([id for id in database.ler_banco_de_dados().get('dados').keys()])

@app.route("/get-data/<int:id>",methods=['GET'])
def get_data(id):
    data = database.ler_banco_de_dados().get('dados').get(str(id))
    return jsonify(data)

@app.route("/get-bairros",methods=['GET'])
def get_bairros():
    with open('bairros.json','r', encoding='utf-8', errors='ignore') as json_bairros:
        locacoes = json.load(json_bairros)

    return jsonify(list(locacoes.keys()))

@app.route("/iframe-frete", methods=['POST'])
def get_iframe():
    try:
        with open('bairros.json', 'r', encoding='utf-8', errors='ignore') as json_bairros:
            localizacoes = json.load(json_bairros)

        data = request.get_json()
        destino = data.get('target')
        origem = 'Rio Vermelho'

        if destino not in localizacoes:
            return jsonify({"error": "Destino não encontrado"}), 400

        m = folium.Map(location=[-12.9714, -38.5014], zoom_start=12)
        cliente['distancia_frete'],caminho = calcular_distancia(origem, destino)
        for bairro in caminho:
            folium.Marker(
                location=localizacoes[bairro],
                tooltip=bairro,
                popup=bairro,
                icon=folium.Icon(color="blue"),
            ).add_to(m)

        bairro_anterior = origem
        for bairro in caminho:
            folium.PolyLine(
                locations=[localizacoes[bairro_anterior],localizacoes[bairro]],
                weight=4,
                color='blue'
            ).add_to(m)
            bairro_anterior=bairro

        iframe = m.get_root()._repr_html_()
        
        response = jsonify({"iframe": iframe})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/get-valor-compra",methods=['GET'])
def get_valor_compra():

    return jsonify({
        'valor_carrinho':cliente['total_compra'],
        'valor_frete':cliente['distancia_frete']*2,
        'tempo':cliente['distancia_frete']/2})

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    # IDs dos produtos no carrinho
    carrinho_ids = list(cliente['carrinho'].keys())

    # Atualizar status dos produtos no carrinho
    for produto_id in carrinho_ids:
        database.alterar_registro(id=produto_id, key='status', valor="Indispon\u00edvel")
        cliente['carrinho'].pop(produto_id)

    return jsonify({"message": "Compra finalizada e Seus produtos estao a caminho", "carrinho": []})

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    print("caminho imagem")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Salva a imagem no diretório especificado
    file.save('static/img' + file.filename)
    return jsonify({'success': 'Img enviada'})

if __name__ == '__main__':
    app.run(debug=True)
