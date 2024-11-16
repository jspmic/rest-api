import os
import json
import pickle
import base64
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, \
        marshal_with, abort
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Google drive scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Changing to the current file path
PATH = str(Path(__file__).parent)  # Working in the same folder as the file
os.chdir(PATH)


# Authenticate to drive
def authenticate_drive():
    creds = None
    # Load saved token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Authenticate if credentials are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)


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

    photo_mvt = db.Column(db.String(70), unique=False, nullable=False)
    photo_journal = db.Column(db.String(70), unique=False, nullable=False)

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
                "photo_journal": self.photo_journal,
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

    photo_mvt = db.Column(db.String(70), unique=False, nullable=False)
    photo_journal = db.Column(db.String(70), unique=False, nullable=False)

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
                "photo_journal": self.photo_journal,
                "type_transport": self.type_transport,
                "user": self.user, "motif": self.motif}


class _TEMP_900(db.Model):
    """ The model that represents the _TEMP_900(Entity) operation or User management"""

    __tablename__ = "_TEMP_900"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _n_9032 = db.Column(db.String(30), nullable=False, unique=False)  # Username
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
transfert_args.add_argument("photo_journal", type=str, required=True,
                            help="<photo_journal> cannot be blank")
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
    "photo_journal": fields.String,
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
livraison_args.add_argument("photo_journal", type=str, required=True,
                            help="<photo_journal> cannot be blank")
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
    "photo_journal": fields.String,
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
                              photo_journal=args["photo_journal"],
                              type_transport=args["type_transport"],
                              user=args["user"],
                              motif=args["motif"])
        db.session.add(livraison)
        db.session.commit()
        return livraison.to_dict(), 201


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
                              photo_journal=args["photo_journal"],
                              type_transport=args["type_transport"],
                              user=args["user"],
                              motif=args["motif"])
        db.session.add(transfert)
        db.session.commit()
        return transfert.to_dict(), 201


class TransfertCollection(Resource):
    """ Transfert Resource Class """

    def get(self) -> tuple:
        """ A `date` parameter must be passed when GET /api/transferts/collection is called """

        date = request.args.get("date", "invalid")
        stock = request.args.get("stock", "invalid")
        if "invalid" in (date, stock):
            logger("Not enough arguments provided for (GET) /api/transferts/collection")
            abort(404, message="Not enough parameters")

        try:
            f_date = datetime.strptime(date, "%d/%m/%Y") if date != "*" else "*"
        except Exception as e:
            logger(f"Not a valid date(GET /api/transferts/collection): {e}")
            return {"message": "Invalid date"}, 404

        if f_date != "*":
            transfert = Transfert.query.filter_by(date=f_date,
                                                  stock_central_depart=stock).all()
        else:
            transfert = Transfert.query.filter_by(stock_central_depart=stock).all()

        return [i.to_dict() for i in transfert], 200


class LivraisonCollection(Resource):
    """ Livraison Resource Class """

    def get(self) -> tuple:
        """ `date` and `district` parameters must be passed when GET /api/livraisons/collection is called """

        date = request.args.get("date", "invalid")
        district = request.args.get("district", "invalid")
        if "invalid" in (date, district):
            logger("Not enough arguments in GET /api/livraisons/collection")
            abort(404, message="Not enough parameters")

        try:
            f_date = datetime.strptime(
                    date, "%d/%m/%Y") if date != "*" else "*"

        except Exception as e:
            logger(f"Invalid date(GET /api/livraisons): {e}")
            abort(404, message="Invalid date")
        if f_date != "*":
            livraisons = Livraison.query.filter_by(date=f_date,
                                                   district=district).all()
        else:
            livraisons = Livraison.query.filter_by(district=district).all()

        return [i.to_dict() for i in livraisons], 200


class _TEMP_(Resource):
    """ Entity Resource(Users) Class """

    def get(self) -> dict:
        """ This resource needs 2 headers `x-api-key` and `Authorization` """

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403

        authorization = request.headers.get("Authorization", "invalid")

        if "invalid" in authorization:
            logger("Authorization header not provided(GET /api/list)")
            return {"message": "Provide the Authorization header"}, 403

        authorization = authorization.split(":")
        if len(authorization) == 2:
            _n_9032 = authorization[0]
            _n_9064 = authorization[1]  # This one must be sha256 hashed
        else:
            logger("Authorization header not properly formatted(GET /api/list)")
            return {"message": "Provide a valid Authorization header"}, 403

        result = _TEMP_900.query.filter_by(_n_9032=_n_9032,
                                           _n_9064=_n_9064).first()
        if not result:
            logger(f"User {_n_9032} not found(GET /api/list)")
            abort(404, message="Not found on the server")

        return result.to_dict(), 200

    @marshal_with(tmp_argsFields)
    def post(self) -> tuple:

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403

        try:
            args = tmp_args.parse_args()
            _n_9032 = args["_n_9032"]
            _n_9064 = args["_n_9064"]  # This one must be sha256 hashed
        except Exception as e:
            logger(f"_n_9032 and _n_9064 not provided properly(POST /api/list): {e}")
            abort(403, message="Provide valid headers")

        if len(_n_9064) != 64:
            logger("_n_9064 field exceeded(or not) the length limit(POST /api/list)")
            abort(403, message="Field length limit not respected")

        tmp = _TEMP_900(_n_9032=_n_9032,
                        _n_9064=_n_9064)
        db.session.add(tmp)
        db.session.commit()
        return tmp.to_dict(), 201


drive_service = authenticate_drive()


class Image(Resource):
    @marshal_with(image_argsFields)
    def post(self) -> tuple:
        try:
            args = image_args.parse_args()
            image: str = args["image"]
            filename: str = args["filename"]
        except Exception as e:
            logger(f"Error parsing arguments(GET /api/image): {e}")
            abort(404)

        try:

            uploads_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)

            # Save image to a temporary file
            file_path = os.path.join('uploads', filename)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image.encode()))

            # Upload the file to Google Drive
            file_metadata = {
                'name': filename,
            }
            media = MediaFileUpload(file_path, mimetype="image/jpeg")
            drive_file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            # Set permissions to your email only
            permission = {
                'type': 'user',
                'role': 'reader',
                'emailAddress': os.getenv("EMAIL")
            }
            drive_service.permissions().create(
                fileId=drive_file.get('id'),
                body=permission
            ).execute()

            # Cleanup temporary file
            os.remove(file_path)

            # Return file ID as response
            image_id = drive_file.get('id')

        except Exception as e:
            logger(f"Error handling image upload: {e}")
            abort(500, message="Internal Server Error")

        return {'url': f"https://drive.google.com/uc?id={image_id}"}, 201


# Adding available resources

api.add_resource(Transferts, "/api/transferts")
api.add_resource(TransfertCollection, "/api/transferts/collection")
api.add_resource(Livraisons, "/api/livraisons")
api.add_resource(LivraisonCollection, "/api/livraisons/collection")
api.add_resource(_TEMP_, "/api/list")
api.add_resource(Image, "/api/image")

# Default routing section


@app.route("/")
def home():
    """ The default homepage of our API """

    return "<h1>RESTful API</h1>"
