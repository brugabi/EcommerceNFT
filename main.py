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

if __name__ == "__main__":
    app.run(debug=True)



