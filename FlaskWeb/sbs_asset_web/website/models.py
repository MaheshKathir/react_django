from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Bay_No = db.Column(db.String(10000))
    Employee_Id = db.Column(db.String(10000))
    Employee_Name = db.Column(db.String(10000))
    Department = db.Column(db.String(10000))
    Program = db.Column(db.String(10000))
    Client_name = db.Column(db.String(10000))
    Cost_Center_Code = db.Column(db.String(10000))
    Vertical = db.Column(db.String(10000))
    WFH_WFO = db.Column(db.String(10000))
    Sharing = db.Column(db.String(10000))
    Device = db.Column(db.String(10000))
    Device_Status = db.Column(db.String(10000))
    Device_Model = db.Column(db.String(10000))
    Asset = db.Column(db.String(10000))
    Serial_No = db.Column(db.String(10000))
    Asset_Owner = db.Column(db.String(10000))
    Warranty_Status = db.Column(db.String(10000)) 
    Purchase_Date = db.Column(db.String(10000))
    Warranty_Exp_Date = db.Column(db.String(10000))
    Configuration = db.Column(db.String(10000))
    Monitor_1_Size = db.Column(db.String(10000)) 
    Monitor_1_Asset = db.Column(db.String(10000))
    Monitor_1_Owner = db.Column(db.String(10000))
    Monitor_2_Size = db.Column(db.String(10000)) 
    Monitor_2_Asset = db.Column(db.String(10000))
    Monitor_2_Owner = db.Column(db.String(10000))
    Headphone = db.Column(db.String(10000))
    Software = db.Column(db.String(10000))
    previous_Asset = db.Column(db.String(10000))
    Remarks = db.Column(db.String(10000))
    Faulty_Status = db.Column(db.String(10000))
    Faulty_Sent_date = db.Column(db.String(10000))
    Gatepass_No = db.Column(db.String(10000))
    Gatepass_IN = db.Column(db.String(10000))
    Gatepass_OUT = db.Column(db.String(10000))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Assets')
