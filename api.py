from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, \
        marshal_with, abort
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
        "mysql://micael:micael@localhost/my_database"
db = SQLAlchemy(app)
api = Api(app)


class Transfert(db.Model):
    __tablename__ = "Transfert"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    plaque = db.Column(db.String(15), unique=False, nullable=False)
    logistic_official = db.Column(db.String(50), unique=False, nullable=False)
    numero_mouvement = db.Column(db.String(10), unique=False, nullable=False)

    stock_central_depart = db.Column(db.String(40), unique=False,
                                     nullable=False)

    stock_central_suivants = db.Column(db.Text, nullable=False)

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


# Argument definition to the api
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
            return {"error": f"Invalid date format: {e}"}, 400

        transfert = Transfert(date=date,
                              plaque=args["plaque"],
                              logistic_official=args["logistic_official"],
                              numero_mouvement=args["numero_mouvement"],
                              stock_central_depart=args["stock_central_depart"],
                              stock_central_suivants=args["stock_central_suivants"],
                              stock_central_retour=args["stock_central_retour"],
                              photo_mvt=args["photo_mvt"],
                              type_transport=args["type_transport"],
                              motif=args["motif"])
        db.session.add(transfert)
        db.session.commit()
        return transfert.to_dict()


api.add_resource(Transferts, "/api/transferts")


@app.route("/")
def home():
    return "<h1>RESTful API</h1>"


if __name__ == "__main__":
    app.run(debug=True)
