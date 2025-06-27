from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    userid = db.Column(db.String,primary_key=True,unique=True)
    fullname = db.Column(db.String,unique=True,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    Address = db.Column(db.String,nullable=False)
    pincode = db.Column(db.String(6),nullable=False)

class Admin(db.Model):
    __tablename__='admin'
    admin = db.Column(db.String,primary_key=True,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)

class ParkingLot(db.Model):
    __tablename__='parking_lots'
    lot_id = db.Column(db.String,primary_key=True)
    prime_location_name = db.Column(db.String,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String,nullable=False)
    pin_code = db.Column(db.String(6),nullable=False)
    max_spots = db.Column(db.Integer,nullable=False)

class ParkingSpot(db.Model):
    __tablename__='parking_spots'
    spot_id = db.Column(db.String,primary_key=True)
    lot_id = db.Column(db.String,db.ForeignKey('parking_lots.lot_id'),nullable=False)
    status = db.Column(db.String,nullable=False)

class ReserveParking(db.Model):
    __tablename__ = 'reservations'
    res_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    spot_id = db.Column(db.String,db.ForeignKey('parking_spots.spot_id'),nullable=False)
    user_id = db.Column(db.String,db.ForeignKey('user.userid'),nullable=False)
    vehicle_no = db.Column(db.String, nullable=False)
    in_date = db.Column(db.Date,nullable=False)
    out_date = db.Column(db.Date)
    in_time = db.Column(db.Time, nullable=False)
    out_time = db.Column(db.Time)
    cost_unit_time = db.Column(db.Integer,nullable=False)