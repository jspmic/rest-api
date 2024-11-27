from init import logger, \
        authenticate_drive, CODE, SECRET, USER, \
        PASSWD, DB_NAME, HOST
import os
import json
import base64
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask import request
from flask_restful import marshal_with, abort, fields, \
        reqparse, Resource
from datetime import datetime
from googleapiclient.http import MediaFileUpload

# Changing to the current file path

PATH = str(Path(__file__).parent)  # Working in the same folder as the file
os.chdir(PATH)

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


class Stock(db.Model):
    """ The model that stores all the `Stock Central`"""
    __tablename__ = "Stock"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_central = db.Column(db.String(40), unique=True,
                              nullable=False)

    def to_dict(self):
        return {"id": self.id, "stock_central": self.stock_central}


class District(db.Model):
    """ The model that stores all the `District`"""
    __tablename__ = "District"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district = db.Column(db.String(25), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "district": self.district}


class Input(db.Model):
    """ The model that stores all the `Input`"""
    __tablename__ = "Input"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input = db.Column(db.String(100), unique=False, nullable=False)

    def to_dict(self):
        return {"id": self.id, "input": self.input}


class Type_Transport(db.Model):
    """ The model that stores all the `Type transport`"""
    __tablename__ = "Type_Transport"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_transport = db.Column(db.String(25), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "type_transport": self.type_transport}


class Colline(db.Model):
    """ The model that stores all the `Colline`"""
    __tablename__ = "Colline"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district = db.Column(db.String(25), unique=True, nullable=False)
    colline = db.Column(db.String(25), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "colline": self.colline}


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

    def to_dict(self) -> dict:
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

    def to_dict(self) -> dict:
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

    def to_dict(self) -> dict:
        return {
                "id": self.id,
                "_n_9032": self._n_9032,
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
image_args.add_argument("image1", type=str, required=True,
                        help="<image1> cannot be blank")
image_args.add_argument("image2", type=str, required=True,
                        help="<image2> cannot be blank")
image_args.add_argument("filename1", type=str, required=True,
                        help="<filename1> cannot be blank")
image_args.add_argument("filename2", type=str, required=True,
                        help="<filename2> cannot be blank")
image_argsFields = {
    "image1": fields.String,
    "image2": fields.String,
}

colline_args = reqparse.RequestParser()
colline_args.add_argument("district", type=str, required=True,
                          help="<district> cannot be blank")

populate_args = reqparse.RequestParser()
populate_args.add_argument("districts", type=str, required=True,
                           help="<districts> cannot be blank")
populate_args.add_argument("type_transports", type=str, required=True,
                           help="<type_transports> cannot be blank")
populate_args.add_argument("stocks", type=str, required=True,
                           help="<stocks> cannot be blank")
populate_args.add_argument("inputs", type=str, required=True,
                           help="<inputs> cannot be blank")

populate_put_args = reqparse.RequestParser()
populate_put_args.add_argument("districts", type=str, required=True,
                               help="<districts> cannot be blank")

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
            if _n_9064 == SECRET:
                result = _TEMP_900.query.filter_by(_n_9032=_n_9032).first()
            else:
                result = _TEMP_900.query.filter_by(_n_9032=_n_9032,
                                                   _n_9064=_n_9064).first()
        else:
            logger("Authorization header not properly formatted(GET /api/list)")
            return {"message": "Provide a valid Authorization header"}, 403

        if not result:
            logger(f"User {_n_9032} not found(GET /api/list)")
            abort(404, message="Not found on the server")
        districts = District.query.all()
        type_transport = Type_Transport.query.all()
        inp = Input.query.all()
        stock = Stock.query.all()
        result_copy = result.to_dict()
        result_copy.update({
            "districts": districts,
            "type_transport": type_transport,
            "inputs": inp,
            "stocks": stock
            })

        return result_copy, 200

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


class Collines(Resource):
    """ Entity Resource(Users) Class """

    def get(self) -> dict:
        """ This resource needs 1 header `x-api-key`"""

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403

        try:
            args = colline_args.parse_args()
            district = args["district"]
        except Exception as e:
            logger(f"Invalid district {district} in GET /api/colline: {e}")
            abort(404, message="No district in request found")

        result = Colline.query.filter_by(district=district).all()
        if not result:
            logger(f"Colline for district {district} not found(GET /api/colline)")
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


class Populate(Resource):
    """ Entity Resource(Populate) Class """

    def post(self) -> tuple:
        """ This resource needs 1 header `x-api-key`"""

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403

        try:
            args = populate_args.parse_args()
            print(args)

            # These fields are to be lists when parsed
            districts = json.loads(args["districts"])
            inputs = json.loads(args["inputs"])
            stocks = json.loads(args["stocks"])
            type_transports = json.loads(args["type_transports"])

        except Exception as e:
            logger(f"Invalid arguments in GET /api/populate: {e}")
            abort(404, message="Provide valid arguments")
        for _district in districts:
            db.session.add(District(district=_district))
        for _input in inputs:
            db.session.add(Input(input=_input))
        for _stock in stocks:
            db.session.add(Stock(stock_central=_stock))
        for _type_transport in type_transports:
            db.session.add(Type_Transport(type_transport=_type_transport))
        db.session.commit()
        return {"message": "Inserted"}, 201

    def put(self) -> tuple:
        """ This resource needs 1 header `x-api-key`"""

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403
        try:
            args = populate_put_args.parse_args()
            districts = json.loads(args["districts"])
        except Exception as e:
            logger(f"Invalid argument in PUT /api/populate: {e}")
            abort(404, message="Provide a valid argument")
        districts_obj = [District(district=_district)
                         for _district in districts]
        db.session.add_all(districts_obj)
        db.session.commit()
        return {"message": "Inserted successfully"}, 201

    def delete(self) -> tuple:
        """ This resource needs 1 header `x-api-key`"""

        code = request.headers.get("x-api-key", "invalid")
        if "invalid" == code:
            logger("x-api-key header not provided(GET /api/list)")
            return {"message": "Provide an api key"}, 403

        if code != CODE:
            logger("x-api-key header not matching(GET /api/list)")
            return {"message": "Invalid api key"}, 403

        field = request.args.get("field", "invalid")
        if field == "invalid":
            logger("Field parameter not provided(DELETE /api/populate)")
            abort(404, message="Invalid request")
        if field == "Districts":
            concerned = District.query.all()
        elif field == "Type_transports":
            concerned = Type_Transport.query.all()
        elif field == "Stocks":
            concerned = Stock.query.all()
        elif field == "Inputs":
            concerned = Input.query.all()
        else:
            logger(f"Field {field} not found(DELETE /api/populate)")
            abort(404, message="Invalid field")

        [db.session.delete(_concerned) for _concerned in concerned]
        db.session.commit()
        return {"message": "Deleted successfully"}, 200


drive_service = authenticate_drive()


# Google drive api corresponding procedures

def upload_image(image: str, filename: str) -> tuple:
    # Upload the given image to google drive

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
        media = MediaFileUpload(file_path,
                                mimetype="image/jpeg",
                                chunksize=-1, resumable=True)
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
        # logging.critical(f"Critical error occurred: {e}")
        logger(f"Error handling image upload: {e}")
        abort(500, message="Internal Server Error")

    # logging.info(f"Uploaded image: {image_id}")
    return {'url': f"https://drive.google.com/uc?id={image_id}"}, 201


class Image(Resource):
    @marshal_with(image_argsFields)
    def post(self) -> tuple:
        try:
            args = image_args.parse_args()
            image1: str = args["image1"]
            image2: str = args["image2"]
            filename1: str = args["filename1"]
            filename2: str = args["filename2"]
        except Exception as e:
            logger(f"Error parsing arguments(GET /api/image): {e}")
            abort(404, message="Provide a valid request to the server")

        try:
            image1 = upload_image(image1, filename1)
            image2 = upload_image(image2, filename2)
            image1_url = image1[0].get("url", "invalid")
            image2_url = image2[0].get("url", "invalid")
        except Exception as e:
            logger(f"Error uploading image: {e}")
            abort(500, message="Internal server error")

        if "invalid" in (image1_url, image2_url):
            logger(f"Error uploading image(url check:551): {image1}, {image2}")
            abort(500, message="Internal server error")

        return {"image1": image1_url, "image2": image2_url}, 201


# Adding available resources

api.add_resource(Transferts, "/api/transferts")
api.add_resource(Livraisons, "/api/livraisons")
api.add_resource(_TEMP_, "/api/list")
api.add_resource(Image, "/api/image")
api.add_resource(Collines, "/api/colline")
api.add_resource(Populate, "/api/populate")

# Default routing section


@app.route("/")
def home():
    """ The default homepage of our API """

    return "<h1>RESTful API</h1>"
