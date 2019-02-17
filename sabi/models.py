
# setup db inside the __init__.py
from sabi import db

# SQL DATABASE AND MODELS

class Device(db.Model):

    __tablename__ = 'devices'

    id = db.Column(db.Integer,primary_key = True)
    hostname = db.Column(db.Text, unique=True, index=True)
    nasid = db.Column(db.Text)
    ip = db.Column(db.Text)
    gateway = db.Column(db.Text)
    wan = db.Column(db.Text)
    location = db.Column(db.Text)

    def __init__(self,hostname,nasid,ip,gateway,wan,location):
        self.hostname = hostname
        self.nasid = nasid
        self.ip = ip
        self.gateway = gateway
        self.wan = wan
        self.location = location


    def __repr__(self):
        #return f"Device {self.hostname} has {self.ip} and is located in {self.location}."
        return f"{self.hostname} {self.nasid} {self.location}"
