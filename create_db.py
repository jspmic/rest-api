from init import app, db
from api import Transfert, Livraison, _TEMP_900
from custom_models import Colline, District, Type_Transport, Input


with app.app_context():
    db.create_all()
