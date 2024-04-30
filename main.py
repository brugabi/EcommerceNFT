import modules.database as database
import zipfile

from flask import Flask,url_for,render_template,send_file

app = Flask(__name__)


@app.route("/")
def home():
    titulo = "Catalogo"
    catalogo = database.lista_de_produtos()
    return render_template("index.html",titulo=titulo,catalogo=catalogo)

@app.route('/return-file')
def return_file():
    pathzip = './arquivos/data_exported.zip'
    with zipfile.ZipFile(pathzip, 'w') as zipf:
        zipf.write('database.json')

    return send_file(pathzip, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)



