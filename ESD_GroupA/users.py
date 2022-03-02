#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Investment_Counsellor(db.Model):
    __tablename__ = 'investmentCounsellor'

    IC_id = db.Column(db.Integer, primary_key=True)
    IC_name = db.Column(db.String(64), nullable=False)
    IC_chatid = db.Column(db.Integer, nullable=False)
    IC_accountname = db.Column(db.String(64), nullable=False)
    IC_password = db.Column(db.String(64), nullable=False)

    def __init__(self, IC_id, IC_name, IC_chatid, IC_accountname, IC_password):
        self.IC_id = IC_id
        self.IC_name: IC_name
        self.IC_chatid: IC_chatid
        self.IC_accountname: IC_accountname
        self.IC_password: IC_password

    def json(self):
        return {
            'IC_id': self.IC_id,
            'IC_name': self.IC_name,
            'IC_chatid': self.IC_chatid,
            'IC_accountname': self.IC_accountname,
            'IC_password': self.IC_password
        }


class Client(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(64), nullable=False)
    client_password = db.Column(db.String(64), nullable=False)
    client_age = db.Column(db.Integer, nullable=False)
    client_chatid = db.Column(db.Integer, nullable=False)
    created_date = db.Column((db.Date), nullable=False)
    client_type = db.Column(db.String(64), nullable=False)
    client_accountname = db.Column(db.String(64), nullable=False)
    investment_id = db.Column(db.String(1064), nullable=False)
    ticker_name = db.Column(db.String(64), nullable=False)
    stock_name = db.Column(db.String(1064), nullable=False)
    IC_id = db.Column(db.ForeignKey(
        'investmentCounsellor.IC_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    investmentCounsellor = db.relationship(
        'Investment_Counsellor', primaryjoin='Client.IC_id == Investment_Counsellor.IC_id', backref='Client')

    def __init__(self, client_id, client_name, client_password, client_age, client_chatid, created_date, client_type, client_accountname, investment_id, IC_id):
        self.client_id: client_id
        self.client_name: client_name
        self.client_password: client_password
        self.client_age: client_age
        self.client_chatid: client_chatid
        self.created_date: created_date
        self.client_type: client_type
        self.client_accountname: client_accountname
        self.investment_id: investment_id
        self.ticker_name = ticker_name
        self.stock_name = stock_name
        self.IC_id: IC_id

    def json(self):
        return {
            'client_id': self.client_id,
            'client_name': self.client_name,
            'client_password': self.client_password,
            'client_age': self.client_age,
            'client_chatid': self.client_chatid,
            'created_date': self.created_date,
            'client_type': self.client_type,
            'client_accountname': self.client_accountname,
            'investment_id': self.investment_id,
            'ticker_name': self.ticker_name,
            'stock_name': self.stock_name,
            'IC_id': self.IC_id
        }


@app.route("/users/client")
def get_all_clients():
    clients = Client.query.all()
    if len(clients):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "clients": [client.json() for client in clients]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Client not found."
        }
    ), 404


@app.route("/users/client/<string:client_id>")
def find_by_client_id(client_id):
    client = Client.query.filter_by(client_id=client_id).first()
    if client:
        return jsonify(
            {
                "code": 200,
                "data": client.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Client ID not found."
        }
    ), 404


@app.route("/users/ic")
def get_all_ics():
    ICs = Investment_Counsellor.query.all()
    if len(ICs):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "ICs": [IC.json() for IC in ICs]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "IC not found."
        }
    ), 404


@app.route("/users/ic_chatid/<string:client_id>")
def retrieve_IC_chatid(client_id):
    try:
        client = Client.query.filter_by(client_id=client_id).first()
        ICs = Investment_Counsellor.query.all()
        retrieve = ""
        for IC in ICs:
            if client.IC_id == IC.IC_id:
                retrieve = "Match"
                chatid = IC.IC_chatid

        if retrieve == "Match":
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "IC_chatid": chatid
                    }
                }
            )
    except:
        return jsonify(
            {
                "code": 404,
                "message": "Client ID not found."
            }
        ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": manage clients and ICs details ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
