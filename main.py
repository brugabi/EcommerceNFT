import modules.database as database
import zipfile
import os
import json
from flask import Flask,url_for,render_template,send_file

app = Flask(__name__)


@app.route("/")
def home():
    titulo = "Catalogo"
    catalogo = database.lista_de_produtos()
    return render_template("index.html",titulo=titulo,catalogo=catalogo)

@app.route('/return-file')
def return_file():
    return send_file('./arquivos/data_exported.zip', as_attachment=True)

@app.route('/file-downloads/')
def file_downloads():
    return render_template('download.html')
if __name__ == "__main__":
    app.run(debug=True)



