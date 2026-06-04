from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Database 
db = SQLAlchemy()


## Models

# User Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')
    approved = db.Column(db.Boolean, default=False)

    location = db.Column(db.String)
    pincode = db.Column(db.String)
    service_type = db.Column(db.String)
    experience = db.Column(db.Float)

    # Relationship
    requests = db.relationship('ServiceRequest',foreign_keys= 'ServiceRequest.customer_id', 
                back_populates='customer', lazy= True)

    assigned_requests = db.relationship('ServiceRequest',foreign_keys= 'ServiceRequest.professional_id', 
                back_populates='professional', lazy= True)



    def __repr__(self):
        return f' <User {self.username}>'


# Service Model 

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Float)

    #Relationship
    requests = db.relationship('ServiceRequest', backref='service', cascade="delete, delete-orphan")

    def __repr__(self):
        return f'<Service {self.name}>'


# Service Request Model

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested_date = db.Column(db.Date, nullable= False)
    completion_date = db.Column(db.Date)
    service_status = db.Column(db.String, default='requested', nullable=False)
    rating = db.Column(db.Integer)

    # Relationships
    customer = db.relationship('User', foreign_keys=[customer_id], back_populates= 'requests')
    professional = db.relationship('User', foreign_keys=[professional_id], back_populates= 'assigned_requests')


