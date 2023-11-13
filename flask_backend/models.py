from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Satellite(db.Model):
    __tablename__ = 'satellites'

    satellite_name = db.Column(db.String(255), primary_key=True)
    un_registry_country = db.Column(db.String(255))
    operator_country = db.Column(db.String(255))
    operator = db.Column(db.String(255))
    user_type = db.Column(db.String(255))
    purpose = db.Column(db.String(255))
    detailed_purpose = db.Column(db.Text)
    orbit_class = db.Column(db.String(255))
    orbit_type = db.Column(db.String(255))
    longitude_geo = db.Column(db.Float)
    perigee = db.Column(db.Integer)
    apogee = db.Column(db.Integer)
    eccentricity = db.Column(db.Float)
    inclination = db.Column(db.Float)
    orbital_period = db.Column(db.Float)
    launch_mass = db.Column(db.Integer)
    dry_mass = db.Column(db.Integer)
    power = db.Column(db.Float)
    launch_date = db.Column(db.Date)
    lifetime = db.Column(db.Float)
    contractor = db.Column(db.String(255))
    contractor_country = db.Column(db.String(255))
    launch_site = db.Column(db.String(255))
    launch_vehicle = db.Column(db.String(255))
    cospar = db.Column(db.String(255))
    norad = db.Column(db.Integer)
    comments = db.Column(db.Text)
    orbital_data_source = db.Column(db.String(255))
    source1 = db.Column(db.Text)
    data_status =  db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'satellite_name': self.satellite_name,
            'un_registry_country': self.un_registry_country,
            'operator_country': self.operator_country,
            'operator': self.operator,
            'user_type': self.user_type,
            'purpose': self.purpose,
            'detailed_purpose': self.detailed_purpose,
            'orbit_class': self.orbit_class,
            'orbit_type': self.orbit_type,
            'longitude_geo': self.longitude_geo,
            'perigee': self.perigee,
            'apogee': self.apogee,
            'eccentricity': self.eccentricity,
            'inclination': self.inclination,
            'orbital_period': self.orbital_period,
            'launch_mass': self.launch_mass,
            'dry_mass': self.dry_mass,
            'power': self.power,
            'launch_date': self.launch_date.isoformat() if self.launch_date else None,
            'lifetime': self.lifetime,
            'contractor': self.contractor,
            'contractor_country': self.contractor_country,
            'launch_site': self.launch_site,
            'launch_vehicle': self.launch_vehicle,
            'cospar': self.cospar,
            'norad': self.norad,
            'comments': self.comments,
            'orbital_data_source': self.orbital_data_source,
            'source1': self.source1,
            'data_status': self.data_status
        }

class SatelliteEditRecord(db.Model):
    __tablename__ = 'satellite_edit_records'
    
    id = db.Column(db.Integer, primary_key=True)
    satellite_name = db.Column(db.String(255), db.ForeignKey('satellites.satellite_name'), nullable=False)
    column_name = db.Column(db.String(255), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    edited_by = db.Column(db.String(255))
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'satellite_name': self.satellite_name,
            'column_name': self.column_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'edited_by': self.edited_by,
            'edit_time': self.edit_time.strftime('%Y-%m-%d %H:%M:%S') if self.edit_time else None
        }


class RecordTable(db.Model):
    __tablename__ = 'record_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime)  # Changed to DateTime to store timestamp
    satellite_name = db.Column(db.String(255), db.ForeignKey('satellites.satellite_name'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'satellite_name': self.satellite_name
        }