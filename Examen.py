from flask import Flask, render_template, abort
from DbClass import Dbclass

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/collection")  # aanmaken nieuwe route
def collection():
    db = Dbclass()
    games = db.getcollection()
    return render_template("collection.html", games=games)

if __name__ == '__main__':
#debugger aanzetten MAAR vanaf de website online staat (productie) zet je deze terug uit
    app.run(debug=True)
