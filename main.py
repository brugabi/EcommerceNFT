import modules.database as database
import zipfile

from flask import Flask,url_for,render_template,send_file

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

if __name__ == "__main__":
    app.run(debug=True)



