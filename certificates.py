from bson.objectid import ObjectId
import flask
import json
import requests

import settings

cert_app = flask.Blueprint('cert_app', __name__, template_folder='templates')

def validate_certificate(data):
    if "cust_id" not in data:
        return False
    if "status" not in data:
        data["status"]="I"
    if "priv_key" not in data:
        return False
    if "cert_body" not in data:
        return False
    return True

def validate_certificate_modification(data):
    if "id" not in data:
        return False
    if "status" not in data or data["status"] not in ["A", "I"]:
        return  False
    return True

def notify_changes(to_send):
    req = requests.post('http://httpbin.org/post', data=to_send)
    print req.status_code

def create_certificate_response(data):
    for cert in data["certificates"]:
        cert["id"] = str(cert["_id"])
        cert.pop("_id")

# add_certificates adds new certificates for customers
@cert_app.route('/certificates', methods = ['POST'])
def add_certificates():
    data = flask.request.json
    certs = data["certificates"]
    for cert in certs:
        if not validate_certificate(cert):
            return settings.create_error_response(errmsg="cannot add certificate, parameters "+
             "missing in one of the certs\n")

    x = settings.mycerts.insert_many(certs)
    print x.inserted_ids
    create_certificate_response(data)

    resp = flask.Response("Response:"+json.dumps(data)+"\n", status=200, mimetype='application/json')
    return resp

# update_cerificates activates or deactivates certificates
@cert_app.route('/certificates/status', methods = ['PUT'])
def update_certificates():
    data = flask.request.json
    certs = data["certificates"]
    for cert in certs:
        if not validate_certificate_modification(cert):
            return settings.create_error_response(errmsg="cannot activate/deactivate certificate; id or status "+
            "missing/invalid in one of the certs\n")
    to_send = []
    rsplist = []
    for cert in certs:
        certid = cert["id"]
        status = cert["status"]
        # find the existing cert and check if the status is
        # already the same as that of the asking query- if it is, no need to update'''
        db_cert = settings.mycerts.find_one({"id": certid})
        if db_cert and db_cert["status"] == status:
            continue

        x= settings.mycerts.update({'_id': ObjectId(certid)},
                   {'$set': {'status': status,
                             }})
        print x
        if x["updatedExisting"]==True:
            to_send.append({"cert_id": certid, "status": status})
            rsplist.append(cert)

    notify_changes(to_send)

    for cert in rsplist:
        cert["id"] = str(cert["id"])
    data["certificates"] = rsplist

    resp = flask.Response(json.dumps(data)+"\n", status=200, mimetype='application/json')
    return resp

# get_active_certificates lists the activate certificates of a customer
@cert_app.route('/customers/<customer_id>/certificates', methods = ['GET'])
def get_active_certificates(customer_id):

    clist = settings.mycerts.find({"cust_id":customer_id, "status":"A"})
    newlist=[]
    for cert in clist:
        cert["id"] = str(cert["_id"])
        cert.pop("_id")
        newlist.append(cert)
        print cert


    respdata="No active certificates found for this customer" if len(newlist) ==0 else newlist

    resp = flask.Response("Active Certificates: "+ json.dumps(respdata)+"\n", status=200, mimetype='application/json')
    return resp