import zipfile
import modules.database as database
from flask import Flask,url_for,render_template,send_file,request

app = Flask(__name__)


@app.route("/")
def home():
    titulo = "Catalogo"
    catalogo = database.lista_de_produtos()
    return render_template("index.html",titulo=titulo,catalogo=catalogo)

@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/adm')
def adm ():
    return render_template('adm.html')

@app.route('/return-file')
def return_file():
    pathzip = './arquivos/data_exported.zip'
    with zipfile.ZipFile(pathzip, 'w') as zipf:
        zipf.write('database.json')

    return send_file(pathzip, as_attachment=True)

@app.route('/insert',methods=['POST'])
def insert():
    try:
        nome = request.form['nome']
        valor = request.form['valor']
        blockchain = request.form['blockchain']
        status = request.form['status']
        image_path = None
        database.inserir_registro(nome=nome,valor=valor,blockchain=blockchain,status=status,image_path=image_path)

        return {"success":True,
                "message":"Usuario inserido com sucesso"}
    
    except Exception as e:
        return {"success":False,
                "message":f"{e}"}
    
@app.route('/delete',methods=['POST'])
def delete():
    try:
        id = request.form['id']
        database.remover_registro(id=id)

        return {"success":True,
                "message":f"O usuario {id} foi deletado com sucesso!"}
    
    except Exception as e:
        return {"success":False,
                "message":f"{e}"}

@app.route('/alterar',methods=['POST'])
def alterar():
    try:
        id = request.form['id']
        key = request.form['key']
        valor = request.form['valor']
        database.alterar_registro(id=id,key=key,valor=valor)
        return {"success":True,
                "message":f"O usuario {id} foi alterado com sucesso!"}
    
    except Exception as e:
        return {"success":False,
                "message":f"{e}"}


if __name__ == "__main__":
    app.run(debug=True)



