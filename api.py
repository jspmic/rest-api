import json
import os
from imagekitio import ImageKit
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, \
        marshal_with, abort
from datetime import datetime
from hashlib import sha256
from pathlib import Path

# Logger function to register events


def logger(event: str) -> bool:
    """ Function to log a given event to a file called `log` """

    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_mssg = f"{now} - {event}\n"
    with open("log", "a") as log:
        log.write(log_mssg)
    print(log_mssg)

# Constants section
# This section consists of the setup variables of the environment


load_dotenv()

CODE: str = os.getenv("CODE")
USER: str = os.getenv("_USER")
PASSWD: str = os.getenv("PASSWD")
HOST: str = os.getenv("HOST")
DB_NAME: str = os.getenv("DB_NAME")
API_ID: str = os.getenv("API_ID")

# Initialization section

PATH = str(Path(__file__).parent)  # Working in the same folder as the file
os.chdir(PATH)
app = Flask(__name__)  # Flask app initialization

try:
    app.config["SQLALCHEMY_DATABASE_URI"] = \
            f"mysql://{USER}:{PASSWD}@{HOST}/{DB_NAME}"
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

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    stock_central_suivants = db.Column(db.JSON, nullable=False)

    stock_central_retour = db.Column(db.String(40), unique=False,
                                     nullable=False)

    photo_mvt = db.Column(db.String(60), unique=False, nullable=False)

    type_transport = db.Column(db.String(25), unique=False, nullable=False)

    motif = db.Column(db.String(45), unique=False, nullable=True)

    user = db.Column(db.String(35), unique=False, nullable=False)

    def to_dict(self):
        """ Function to be rendered when a representation of the object is needed """

        return {"id": self.id, "date": self.date.strftime("%d/%m/%Y"),
                "plaque": self.plaque,
                "logistic_official": self.logistic_official,
                "numero_mouvement": int(self.numero_mouvement),
                "stock_central_depart": self.stock_central_depart,
                "stock_central_suivants": self.stock_central_suivants,
                "stock_central_retour": self.stock_central_retour,
                "photo_mvt": self.photo_mvt,
                "type_transport": self.type_transport,
                "user": self.user, "motif": self.motif}


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

    user = db.Column(db.String(35), unique=False, nullable=False)

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
                "type_transport": self.type_transport,
                "user": self.user, "motif": self.motif}


class _TEMP_900(db.Model):
    """ The model that represents the _TEMP_900(Entity) operation or User management"""

    __tablename__ = "_TEMP_900"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _n_9032 = db.Column(db.String(35), nullable=False, unique=False)  # Username
    _n_9064 = db.Column(db.String(64), nullable=False, unique=True)  # Password

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
transfert_args.add_argument("user", type=str, required=True,
                            help="<user> cannot be blank")
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
    "user": fields.String,
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
livraison_args.add_argument("user", type=str, required=True,
                            help="<user> cannot be blank")
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
    "user": fields.String,
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

image_args = reqparse.RequestParser()
image_args.add_argument("image", type=str, required=True,
                        help="<image> cannot be blank")
image_args.add_argument("filename", type=str, required=True,
                        help="<filename> cannot be blank")
image_argsFields = {
    "url": fields.String,
}

# Ressource definition section


class Livraisons(Resource):
    """ Livraison Resource Class """

    def get(self) -> tuple:
        """ `date` and `user` parameters must be passed when GET /api/livraisons is called """

        date = request.args.get("date", "invalid")
        user = request.args.get("user", "invalid")
        if "invalid" in (date, user):
            logger("Not enough arguments in GET /api/livraisons")
            abort(404)

        try:
            f_date = datetime.strptime(
                    date, "%d/%m/%Y") if date != "*" else "*"

        except Exception as e:
            logger(f"Invalid date(GET /api/livraisons): {e}")
            abort(404)
        if f_date != "*":
            livraisons = Livraison.query.filter_by(date=f_date,
                                                   user=user).all()
        else:
            livraisons = Livraison.query.filter_by(user=user).all()

        return [i.to_dict() for i in livraisons], 200

    @marshal_with(livraisonFields)
    def post(self) -> tuple:
        """ The Livraison post requests requires a `body` to insert a new element """

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
                              user=args["user"],
                              motif=args["motif"])
        db.session.add(livraison)
        db.session.commit()
        return livraison.to_dict(), 200


class Transferts(Resource):
    """ Transfert Resource Class """

    def get(self) -> tuple:
        """ A `date` parameter must be passed when GET /api/transferts is called """

        date = request.args.get("date", "invalid")
        user = request.args.get("user", "invalid")
        if "invalid" in (date, user):
            logger("Not enough arguments provided for (GET) /api/transferts")
            abort(404)

        try:
            f_date = datetime.strptime(date, "%d/%m/%Y") if date != "*" else "*"
        except Exception as e:
            logger(f"Not a valid date(GET /api/transferts): {e}")
            return {"message": "Invalid date"}, 404

        if f_date != "*":
            transfert = Transfert.query.filter_by(date=f_date, user=user).all()
        else:
            transfert = Transfert.query.filter_by(user=user).all()

        return [i.to_dict() for i in transfert], 200

    @marshal_with(transfertFields)
    def post(self) -> tuple:
        """ The Transfert post requests requires a `body` to insert a new element """

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
                              stock_central_depart=args["stock_central_depart"],
                              stock_central_suivants=stock_central_suivants,
                              stock_central_retour=args["stock_central_retour"],
                              photo_mvt=args["photo_mvt"],
                              type_transport=args["type_transport"],
                              user=args["user"],
                              motif=args["motif"])
        db.session.add(transfert)
        db.session.commit()
        return transfert.to_dict(), 200


class _TEMP_(Resource):
    """ Entity Resource(Users) Class """

    def get(self) -> tuple:
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
    def post(self) -> tuple:
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


class Image(Resource):
    @marshal_with(image_argsFields)
    def post(self) -> tuple:
        try:
            args = image_args.parse_args()
            image = args["image"]
            filename = args["filename"]
        except Exception as e:
            logger(f"Error parsing arguments(GET /api/image): {e}")
            abort(404)

        private_key: str = os.getenv("PRIVATE_KEY")
        public_key: str = os.getenv("PUBLIC_KEY")
        url = os.getenv("URL")

        imagekit = ImageKit(
            public_key=public_key,
            private_key=private_key,
            url_endpoint=url
        )
        upload = imagekit.upload(
            file=image,
            file_name=filename
        )
        print(upload.url)
        return {"url": f"{upload.url}"}, 200


# Adding available resources

api.add_resource(Transferts, "/api/transferts")
api.add_resource(Livraisons, "/api/livraisons")
api.add_resource(_TEMP_, "/api/list")
api.add_resource(Image, "/api/image")

# Default routing section


@app.route("/")
def home():
    """ The default homepage of our API """

    return "<h1>RESTful API</h1>"


if __name__ == "__main__":
    app.run(debug=True)
