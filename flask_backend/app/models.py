from flask_backend.app import db


class Orbit(db.Model):
    JCAT = db.Column(db.String(50), primary_key=True)
    OpOrbitOQU = db.Column(db.String(100))
    inclination = db.Column(db.Float)
    perigee = db.Column(db.Integer)
    apogee = db.Column(db.Integer)
    primary_planet = db.Column(db.String(50))


class Satellites(db.Model):
    JCAT = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    piece = db.Column(db.String(50))
    PL_name = db.Column(db.String(50))
    parent = db.Column(db.String(50))
    state = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    bus = db.Column(db.String(50))
    status = db.Column(db.String(50))
    altname = db.Column(db.String(100))
    dest = db.Column(db.String(100))


class Dates(db.Model):
    JCAT = db.Column(db.String(50), primary_key=True)
    Ldate = db.Column(db.DateTime)
    Sdate = db.Column(db.DateTime)
    Ddate = db.Column(db.DateTime)
    Odate = db.Column(db.DateTime)


class Specs(db.Model):
    JCAT = db.Column(db.String(50), primary_key=True)
    motor = db.Column(db.String(100))
    length = db.Column(db.Float)
    diameter = db.Column(db.Float)
    mass = db.Column(db.Integer)
    drymass = db.Column(db.Integer)
    tot_mass = db.Column(db.Integer)
    span = db.Column(db.Float)
    shape = db.Column(db.String(50))


class Deletes(db.Model):
    JCAT = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    Deletion_date = db.Column(db.DateTime)
