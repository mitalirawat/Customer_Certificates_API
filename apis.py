from bson.objectid import ObjectId
from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_bcrypt import Bcrypt
import json
import pymongo

from certificates import simple_page

import settings

app = Flask(__name__)
app.register_blueprint(simple_page)
bcrypt = Bcrypt(app)
api = Api(app)


def validate_customer(data):
    if "name" not in data or "email" not in data or "passwd" not in data:
        return False
    return True

def add_customers():
    cust_data = request.json

    #print cust_data
    custlist = cust_data["customers"]
    for cust in custlist:
        if not validate_customer(cust):
            return settings.create_error_response(errmsg="invalid or missing keys in data\n")
        cust["passwd"] = bcrypt.generate_password_hash(cust["passwd"])

    x = settings.custcoll.insert_many(custlist)
    print x.inserted_ids
    return None


def delete_customers():
    cust_data = request.json
    #print cust_data
    if "ids" not in cust_data["customers"]:
        return settings.create_error_response("Delete requires 'ids' field in the form data")
    ids = cust_data["customers"]["ids"]
    print ids
    plist = [ObjectId(i) for i in ids]
    settings.custcoll.delete_many({'_id': {'$in': plist}})
    return None

def create_customer_response(data):
    for cust in data["customers"]:
        cust["id"] = str(cust["_id"])
        cust.pop("_id", None)
        cust.pop("passwd", None)

@app.route('/customers', methods=['POST', 'DELETE'])
def create_customers():

    if request.headers['Content-Type'] == 'application/json':
        if request.method == "POST":
            err = add_customers()
            if err:
                return err

            data = request.json
            print data
            create_customer_response(data)

        if request.method == "DELETE":
            err = delete_customers()
            if err: return err
            data = request.json
            #print data

        resp = Response("Response:" + json.dumps(data) + "\n", status=200, mimetype='application/json')
        return resp

    else:
        return settings.create_error_response(errmsg="415 Unsupported Media Type")

#import certificates

if __name__ == '__main__':
    settings.init()
    app.run(host= '0.0.0.0', port='5002')