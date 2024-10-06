import json
import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, \
        marshal_with, abort
from datetime import datetime
from hashlib import sha256
from pathlib import Path

# Logger function(register errors)


def logger(mssg: str) -> bool:
    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_mssg = f"{now} - {mssg}\n"
    with open("log", "a") as log:
        log.write(log_mssg)
    print(log_mssg)

# Constants section


load_dotenv()

CODE: str = os.getenv("CODE")

# Initialization section

PATH = str(Path(__file__).parent)
os.chdir(PATH)
app = Flask(__name__)

try:
    app.config["SQLALCHEMY_DATABASE_URI"] = \
            "mysql://micael:micael@localhost/my_database"
    db = SQLAlchemy(app)
    api = Api(app)
except Exception as e:
    logger(f"Couldn't load database: {e}")

# Model definition section


class Transfert(db.Model):
    """ The model that represents the Transfert operation """

    __tablename__ = "Transfert"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.Integer, unique=False, nullable=False)
    district = db.Column(db.String(15), unique=False, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    stock_central_suivants = db.Column(db.JSON, nullable=False)

    stock_central_retour = db.Column(db.String(40), unique=False,
                                     nullable=False)

    photo_mvt = db.Column(db.String(60), unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    def to_dict(self):
        """ Function to be rendered when a repr of the object is needed """

        return {"id": self.id, "date": self.date.strftime("%d/%m/%Y"),
                "plaque": self.plaque,
                "logistic_official": self.logistic_official,
                "numero_mouvement": int(self.numero_mouvement),
                "district": self.district,
                "stock_central_depart": self.stock_central_depart,
                "stock_central_suivants": self.stock_central_suivants,
                "stock_central_retour": self.stock_central_retour,
                "photo_mvt": self.photo_mvt,
                "type_transport": self.type_transport, "motif": self.motif}


class Livraison(db.Model):
    """ The model that represents the Livraison operation """

    __tablename__ = "Livraison"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.Integer, unique=False, nullable=False)

    district = db.Column(db.String(15), unique=False, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    boucle = db.Column(db.JSON, nullable=False)

    stock_central_retour = db.Column(db.String(40), unique=False,
                                     nullable=False)

    photo_mvt = db.Column(db.String(60), unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    def to_dict(self):
        return {"id": self.id, "date": self.date.strftime("%d/%m/%Y"),
                "plaque": self.plaque,
                "logistic_official": self.logistic_official,
                "numero_mouvement": int(self.numero_mouvement),
                "stock_central_depart": self.stock_central_depart,
                "district": self.district,
                "boucle": self.boucle,
                "stock_central_retour": self.stock_central_retour,
                "photo_mvt": self.photo_mvt,
                "type_transport": self.type_transport, "motif": self.motif}


class _TEMP_900(db.Model):
    """ The model that represents the _TEMP_900(Entity) operation """

    __tablename__ = "_TEMP_900"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _n_9032 = db.Column(db.String(35), nullable=False, unique=False)
    _n_9064 = db.Column(db.String(64), nullable=False, unique=True)

    def to_dict(self):
        return {
                "id": self.id,
                "_n_9032": self._n_9032,
                "_n_9064": self._n_9064,
                }


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
transfert_args.add_argument("district", type=str, required=True,
                            help="<district> cannot be blank")
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
    "district": fields.String,
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
livraison_args.add_argument("district", type=str, required=True,
                            help="<district> cannot be blank")
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
    "district": fields.String,
    "stock_central_depart": fields.String,
    "boucle": fields.String,
    "stock_central_retour": fields.String,
    "photo_mvt": fields.String,
    "type_transport": fields.String,
    "motif": fields.String
}

tmp_args = reqparse.RequestParser()
tmp_args.add_argument("_n_9032", type=str, required=True,
                      help="<_n_9032> cannot be blank")
tmp_args.add_argument("_n_9064", type=str, required=True,
                      help="<_n_9064> cannot be blank")

tmp_argsFields = {
    "_n_9032": fields.String,
    "_n_9064": fields.String
    }

# Ressource definition section


class Livraisons(Resource):
    """ Livraison Resource Class """

    def get(self):
        date = request.args.get("date", "invalid")
        if date == "invalid":
            logger("No date provided in GET /api/livraisons")
            abort(404)

        try:
            f_date = datetime.strptime(date, "%d/%m/%Y") if date != "*" else "*"
        except Exception as e:
            logger(f"Invalid date(GET /api/livraisons): {e}")
            abort(404)
        if f_date != "*":
            livraisons = Livraison.query.filter_by(date=f_date).all()
        else:
            livraisons = Livraison.query.all()

        return [i.to_dict() for i in livraisons], 200

    @marshal_with(livraisonFields)
    def post(self):
        try:
            args = livraison_args.parse_args()
            date = datetime.strptime(args["date"], "%d/%m/%Y")
        except Exception as e:
            logger(f"Error parsing arguments(POST /api/livraisons): {e}")
            abort(404)
        boucle = json.loads(args["boucle"])

        livraison = Livraison(date=date,
                              plaque=args["plaque"],
                              logistic_official=args["logistic_official"],
                              numero_mouvement=args["numero_mouvement"],
                              district=args["district"],
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
    """ Transfert Resource Class """

    def get(self):
        date = request.args.get("date", "invalid")
        if date == "invalid":
            logger("No date provided for (GET) /api/transferts")
            abort(404)

        try:
            f_date = datetime.strptime(date, "%d/%m/%Y") if date != "*" else "*"
        except Exception as e:
            logger(f"Not a valid date(GET /api/transferts): {e}")
            return {"message": "Invalid date"}, 404

        if f_date != "*":
            transfert = Transfert.query.filter_by(date=f_date).all()
        else:
            transfert = Transfert.query.all()

        return [i.to_dict() for i in transfert], 200

    @marshal_with(transfertFields)
    def post(self) -> dict:

        try:
            args = transfert_args.parse_args()
            date = datetime.strptime(args["date"], "%d/%m/%Y")
        except Exception as e:
            logger(f"Error parsing arguments(POST /api/transferts): {e}")
            abort(404)

        stock_central_suivants = json.loads(args["stock_central_suivants"])
        transfert = Transfert(date=date,
                              plaque=args["plaque"],
                              logistic_official=args["logistic_official"],
                              numero_mouvement=args["numero_mouvement"],
                              district=args["district"],
                              stock_central_depart=args["stock_central_depart"],
                              stock_central_suivants=stock_central_suivants,
                              stock_central_retour=args["stock_central_retour"],
                              photo_mvt=args["photo_mvt"],
                              type_transport=args["type_transport"],
                              motif=args["motif"])
        db.session.add(transfert)
        db.session.commit()
        return transfert.to_dict()


class _TEMP_(Resource):
    """ Entity Resource Class """

    def get(self) -> bool:
        """ This resource needs 2 parameters `code` and `_n_9032` """

        code = request.args.get("code", "invalid")
        if code != CODE:
            logger("Code was incorrect in GET /api/list")
            return {"message": "Invalid code"}, 404

        _n_9032 = request.args.get("_n_9032", "invalid")
        _n_9064 = request.args.get("_n_9064", "invalid")
        if "invalid" in [_n_9032, _n_9064]:
            logger("_n_90xx not provided(GET /api/list)")
            return {"message": "Provide a valid _n_90xx parameter"}

        _n_9064 = sha256(_n_9064.encode()).hexdigest()
        result = _TEMP_900.query.filter_by(_n_9032=_n_9032,
                                           _n_9064=_n_9064).first()
        if not result:
            logger(f"User {_n_9032} not found(GET /api/list)")
            abort(404)
        return result.to_dict(), 200

    @marshal_with(tmp_argsFields)
    def post(self) -> None:
        code = request.args.get("code", "invalid")
        if code != CODE:
            logger("Code was incorrect in POST /api/list")
            return {"message": "Invalid code"}, 404

        try:
            args = tmp_args.parse_args()
            _n_9064 = sha256(args["_n_9064"].encode()).hexdigest()
        except Exception as e:
            logger(f"Error parsing arguments(POST /api/list): {e}")
            abort(404)
        tmp = _TEMP_900(_n_9032=args["_n_9032"],
                        _n_9064=_n_9064)
        db.session.add(tmp)
        db.session.commit()
        return tmp.to_dict(), 201


api.add_resource(Transferts, "/api/transferts")
api.add_resource(Livraisons, "/api/livraisons")
api.add_resource(_TEMP_, "/api/list")

# Default routing section


@app.route("/")
def home():
    """ The default home of our API """

    return "<h1>RESTful API</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
