import json
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, \
        marshal_with, abort
from datetime import datetime

# Initialization section

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
        "mysql://micael:micael@localhost/my_database"
db = SQLAlchemy(app)
api = Api(app)

# Model definition section


class Transfert(db.Model):
    __tablename__ = "Transfert"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.String(10), unique=False, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    stock_central_suivants = db.Column(db.JSON, nullable=False)

    stock_central_retour = db.Column(db.String(40), unique=False,
                                     nullable=False)

    photo_mvt = db.Column(db.String(60), unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    def to_dict(self):
        return {"id": self.id, "date": self.date, "plaque": self.plaque,
                "logistic_official": self.logistic_official,
                "numero_mouvement": int(self.numero_mouvement),
                "stock_central_depart": self.stock_central_depart,
                "stock_central_suivants": self.stock_central_suivants,
                "stock_central_retour": self.stock_central_retour,
                "photo_mvt": self.photo_mvt,
                "type_transport": self.type_transport, "motif": self.motif}


class Livraison(db.Model):
    __tablename__ = "Livraison"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.String(10), unique=False, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    boucle = db.Column(db.JSON, nullable=False)

    stock_central_retour = db.Column(db.String(40), unique=False,
                                     nullable=False)

    photo_mvt = db.Column(db.String(60), unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    def to_dict(self):
        return {"id": self.id, "date": self.date, "plaque": self.plaque,
                "logistic_official": self.logistic_official,
                "numero_mouvement": int(self.numero_mouvement),
                "stock_central_depart": self.stock_central_depart,
                "boucle": self.boucle,
                "stock_central_retour": self.stock_central_retour,
                "photo_mvt": self.photo_mvt,
                "type_transport": self.type_transport, "motif": self.motif}


# Argument definition section

transfert_args = reqparse.RequestParser()
transfert_args.add_argument("date", type=str, required=True,
                            help="<date> cannot be blank")
transfert_args.add_argument("plaque", type=str, required=True,
                            help="<plaque> cannot be blank")
transfert_args.add_argument("logistic_official", type=str, required=True,
                            help="<logistic_official> cannot be blank")
transfert_args.add_argument("numero_mouvement", type=int, required=True,
                            help="<numero_mouvement> cannot be blank")
transfert_args.add_argument("stock_central_depart", type=str, required=True,
                            help="<stock_central_depart> cannot be blank")
transfert_args.add_argument("stock_central_suivants", type=str, required=True,
                            help="<stock_central_suivants> cannot be blank")
transfert_args.add_argument("stock_central_retour", type=str, required=True,
                            help="<stock_central_retour> cannot be blank")
transfert_args.add_argument("photo_mvt", type=str, required=True,
                            help="<photo_mvt> cannot be blank")
transfert_args.add_argument("type_transport", type=str, required=True,
                            help="<type_transport> cannot be blank")
transfert_args.add_argument("motif", type=str, required=False)

transfertFields = {
    "date": fields.String,
    "plaque": fields.String,
    "logistic_official": fields.String,
    "numero_mouvement": fields.Integer,
    "stock_central_depart": fields.String,
    "stock_central_suivants": fields.String,
    "stock_central_retour": fields.String,
    "photo_mvt": fields.String,
    "type_transport": fields.String,
    "motif": fields.String
}

livraison_args = reqparse.RequestParser()
livraison_args.add_argument("date", type=str, required=True,
                            help="<date> cannot be blank")
livraison_args.add_argument("plaque", type=str, required=True,
                            help="<plaque> cannot be blank")
livraison_args.add_argument("logistic_official", type=str, required=True,
                            help="<logistic_official> cannot be blank")
livraison_args.add_argument("numero_mouvement", type=int, required=True,
                            help="<numero_mouvement> cannot be blank")
livraison_args.add_argument("stock_central_depart", type=str, required=True,
                            help="<stock_central_depart> cannot be blank")
livraison_args.add_argument("boucle", type=str, required=True,
                            help="<boucle> cannot be blank")
livraison_args.add_argument("stock_central_retour", type=str, required=True,
                            help="<stock_central_retour> cannot be blank")
livraison_args.add_argument("photo_mvt", type=str, required=True,
                            help="<photo_mvt> cannot be blank")
livraison_args.add_argument("type_transport", type=str, required=True,
                            help="<type_transport> cannot be blank")
livraison_args.add_argument("motif", type=str, required=False)

livraisonFields = {
    "date": fields.String,
    "plaque": fields.String,
    "logistic_official": fields.String,
    "numero_mouvement": fields.Integer,
    "stock_central_depart": fields.String,
    "boucle": fields.String,
    "stock_central_retour": fields.String,
    "photo_mvt": fields.String,
    "type_transport": fields.String,
    "motif": fields.String
}

# Ressource definition section


class Livraisons(Resource):
    def get(self) -> list:
        livraisons = Livraison.query.all()
        result = [i.to_dict() for i in livraisons]
        return jsonify(result)

    @marshal_with(livraisonFields)
    def post(self):
        args = livraison_args.parse_args()

        try:
            date = datetime.strptime(args["date"], "%d/%m/%Y")
        except Exception as e:
            mssg = {"error": f"Invalid date format: {e}"}
            return jsonify(mssg), 400
        boucle = json.loads(args["boucle"])

        livraison = Livraison(date=date,
                              plaque=args["plaque"],
                              logistic_official=args["logistic_official"],
                              numero_mouvement=args["numero_mouvement"],
                              stock_central_depart=args["stock_central_depart"],
                              boucle=boucle,
                              stock_central_retour=args["stock_central_retour"],
                              photo_mvt=args["photo_mvt"],
                              type_transport=args["type_transport"],
                              motif=args["motif"])
        db.session.add(livraison)
        db.session.commit()
        return livraison.to_dict()


class Transferts(Resource):
    def get(self) -> list:
        transferts = Transfert.query.all()
        result = [i.to_dict() for i in transferts]
        return jsonify(result)

    @marshal_with(transfertFields)
    def post(self):
        args = transfert_args.parse_args()

        try:
            date = datetime.strptime(args["date"], "%d/%m/%Y")
        except Exception as e:
            mssg = {"error": f"Invalid date format: {e}"}
            return jsonify(mssg), 400

        stock_central_suivants = json.loads(args["stock_central_suivants"])
        transfert = Transfert(date=date,
                              plaque=args["plaque"],
                              logistic_official=args["logistic_official"],
                              numero_mouvement=args["numero_mouvement"],
                              stock_central_depart=args["stock_central_depart"],
                              stock_central_suivants=stock_central_suivants,
                              stock_central_retour=args["stock_central_retour"],
                              photo_mvt=args["photo_mvt"],
                              type_transport=args["type_transport"],
                              motif=args["motif"])
        db.session.add(transfert)
        db.session.commit()
        return transfert.to_dict()


api.add_resource(Transferts, "/api/transferts")
api.add_resource(Livraisons, "/api/livraisons")

# Default routing section


@app.route("/")
def home():
    return "<h1>RESTful API</h1>"


if __name__ == "__main__":
    app.run(debug=True)
