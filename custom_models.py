from init import db

# This file contains custom models written to handle performance issues
# in the soft_ui such as:
#     - `Isolates` not effective as expected
#     - O(n) time when populating the caches


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
    __tablename__ = "Type Transport"
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
