from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, datetime
from sqlalchemy import Column, Date, DateTime, String, Integer, Text


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    age = db.Column(db.Integer)
    saved_financial_aid = db.relationship('SavedFinancialAid')
    userAlert = db.relationship('UserAlert')


class FinancialAid(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(255), nullable=False)
    type = db.Column(String(150), nullable=False)
    description = db.Column(Text, nullable=False)
    eligibility_criteria = db.Column(Text, nullable=False)
    opening_date = db.Column(Date, nullable=False)
    deadline = db.Column(Date, nullable=False)
    contact_details = db.Column(String(255), nullable=False)
    link_to_more_information = db.Column(String(255))  # Allow null values for optional link
    date_added = db.Column(Date, nullable=False, default=date.today)
    saved_financial_aid = db.relationship('SavedFinancialAid')
    userAlert = db.relationship('UserAlert')


class SavedFinancialAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    financial_aid_id = db.Column(db.Integer, db.ForeignKey('financial_aid.id'), nullable=False)
    date_saved = db.Column(db.DateTime)


class UserAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    financial_aid_id = db.Column(db.Integer, db.ForeignKey('financial_aid.id'), nullable=False)
    reminder_date = db.Column(db.DateTime)
    reminder_message = db.Column(db.Text)


