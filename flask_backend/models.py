from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    
#new launches
class Satellite_New(db.Model):
    __tablename__ = 'ucs_new_launches'

    full_name = db.Column(db.String(255))
    official_name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    owner_country = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    users = db.Column(db.String(255))
    purpose = db.Column(db.String(255))
    detail_purpose = db.Column(db.String(255))
    orbit_class = db.Column(db.String(255))
    orbit_type = db.Column(db.String(255))
    in_geo = db.Column(db.Integer)
    perigee = db.Column(db.Integer)
    apogee = db.Column(db.Integer)
    eccentricity = db.Column(db.String(255))
    inclination = db.Column(db.Float)
    period = db.Column(db.String(255))
    mass = db.Column(db.Float)
    dry_mass = db.Column(db.Float)
    power = db.Column(db.String(255))
    launch_date = db.Column(db.DateTime)
    expected_lifetime = db.Column(db.String(255))
    contractor = db.Column(db.String(255))
    contractor_country = db.Column(db.String(255))
    launch_site = db.Column(db.String(255))
    launch_vehicle = db.Column(db.String(255))
    cospar = db.Column(db.String(255), primary_key=True)
    norad = db.Column(db.Integer)
    source = db.Column(db.String(255))
    additional_source = db.Column(db.String(255))
    data_status = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'full_name': self.full_name,
            'official_name': self.official_name,
            'owner_country': self.owner_country,
            'orbit_class': self.orbit_class,
            'country': self.country,
            'owner': self.owner,
            'users': self.users,
            'purpose': self.purpose,
            'detail_purpose': self.detail_purpose,
            'orbit_class': self.orbit_class,
            'orbit_type': self.orbit_type,
            'in_geo': self.in_geo,
            'perigee': self.perigee,
            'apogee': self.apogee,
            'eccentricity': self.eccentricity,
            'inclination': self.inclination,
            'period': self.period,
            'mass': self.mass,
            'dry_mass': self.dry_mass,
            'power': self.power,
            'launch_date': self.launch_date,
            'expected_lifetime': self.expected_lifetime,
            'contractor': self.contractor,
            'contractor_country': self.contractor_country,
            'launch_site': self.launch_site,
            'launch_vehicle': self.launch_vehicle,
            'cospar': self.cospar,
            'norad': self.norad,
            'source': self.source,
            'additional_source': self.additional_source,
            'data_status': self.data_status
        }
    
#ucs_master_dataset
class Satellite_Master(db.Model):
    __tablename__ = 'ucs_master'

    full_name = db.Column(db.String(255))
    official_name = db.Column(db.String(255))
    country = db.Column(db.String(255))
    owner_country = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    users = db.Column(db.String(255))
    purpose = db.Column(db.String(255))
    detail_purpose = db.Column(db.String(255))
    orbit_class = db.Column(db.String(255))
    orbit_type = db.Column(db.String(255))
    in_geo = db.Column(db.String(255))
    perigee = db.Column(db.String(255))
    apogee = db.Column(db.String(255))
    eccentricity = db.Column(db.String(255))
    inclination = db.Column(db.String(255))
    period = db.Column(db.String(255))
    mass = db.Column(db.String(255))
    dry_mass = db.Column(db.String(255))
    power = db.Column(db.String(255))
    launch_date = db.Column(db.String(255))
    expected_lifetime = db.Column(db.String(255))
    contractor = db.Column(db.String(255))
    contractor_country = db.Column(db.String(255))
    launch_site = db.Column(db.String(255))
    launch_vehicle = db.Column(db.String(255))
    cospar = db.Column(db.String(255), primary_key=True)
    norad = db.Column(db.String(255))
    data_status =  db.Column(db.Integer)
    source = db.Column(db.String(255))
    additional_source = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'full_name': self.full_name,
            'official_name': self.official_name,
            'owner_country': self.owner_country,
            'orbit_class': self.orbit_class,
            'country': self.country,
            'owner': self.owner,
            'users': self.users,
            'purpose': self.purpose,
            'detail_purpose': self.detail_purpose,
            'orbit_class': self.orbit_class,
            'orbit_type': self.orbit_type,
            'in_geo': self.in_geo,
            'perigee': self.perigee,
            'apogee': self.apogee,
            'eccentricity': self.eccentricity,
            'inclination': self.inclination,
            'period': self.period,
            'mass': self.mass,
            'dry_mass': self.dry_mass,
            'power': self.power,
            'launch_date': self.launch_date,
            'expected_lifetime': self.expected_lifetime,
            'contractor': self.contractor,
            'contractor_country': self.contractor_country,
            'launch_site': self.launch_site,
            'launch_vehicle': self.launch_vehicle,
            'cospar': self.cospar,
            'norad': self.norad,
            'data_status': self.data_status,
            'source': self.source,
            'additional_source': self.additional_source
        }

class SatelliteEditRecord(db.Model):
    __tablename__ = 'satellite_edit_records'
    
    id = db.Column(db.Integer, primary_key=True)
    cospar = db.Column(db.String(255), db.ForeignKey('ucs_master.cospar'), nullable=False)
    column_name = db.Column(db.String(255), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    edited_by = db.Column(db.String(255))
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'cospar': self.cospar,
            'column_name': self.column_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'edited_by': self.edited_by,
            'edit_time': self.edit_time.strftime('%Y-%m-%d %H:%M:%S') if self.edit_time else None
        }
    
class SatelliteRemovalRecord(db.Model):

    __tablename__ = 'satellite_removal_records'

    id = db.Column(db.Integer, primary_key=True)
    cospar = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "cospar": self.cospar,
            "reason": self.reason,
        }



class RecordTable(db.Model):
    __tablename__ = 'record_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime)  # Changed to DateTime to store timestamp
    cospar = db.Column(db.String(255), db.ForeignKey('ucs_master.cospar'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'cospar': self.cospar
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class ScrapeRecord(db.Model):
    __tablename__ = 'scrape_record'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    scrape_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "scrape_date": self.scrape_date,
        }