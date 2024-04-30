import modules.database as database
import zipfile
import os
import json
from flask import Flask,url_for,render_template,send_file

app = Flask(__name__)

diretorio = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def home():
    titulo = "Catalogo"
    catalogo = database.lista_de_produtos()
    return render_template("index.html",titulo=titulo,catalogo=catalogo)

@app.route('/download')
def download():
    path = 'database.json'

    #Abre o arquivo JSON
    with open(path, 'r') as file:
        Arqui_JSON = json.load(file)


    #Gera arquivo ZIP

    zip_path = 'database.zip'

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(path, 'database.json')
 

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)



