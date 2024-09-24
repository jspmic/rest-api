from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql:///database.db"
db = SQLAlchemy(app)


class Transfert(db.Model):
    __tablename__ = "Transfert"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.String(10), unique=True, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    stock_central_suivants = db.Column(JSON)

    photo_mvt = db.Column(db.URL, unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    def __repr__(self):
        return "<Transfert> model"


@app.route("/")
def home():
    return "<h1>RESTful API</h1>"


if __name__ == "__main__":
    app.run(debug=True)
