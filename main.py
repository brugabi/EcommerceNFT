import modules.database as database
from flask import Flask,url_for,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/etapa1")
def etapa1():
    return render_template('etapa1.html')

if __name__ == "__main__":
    app.run(debug=True)



