# Customer Certificates

This repository implements a basic RESTful HTTP API for creating customers and their certificates, listing active certificates
and deleting customers.
App defined in apis.py.

**Database**

1. **Two** mongodb collections to store data.
2. Created a compound index on certificates collection for fast retrieval of active
certificates for a cust_id.

 Customers:
 
    name
    email
    passwd
    
 Certificates
    
    cust_id
    status : could be active "A" or inactive "I"
    priv_key
    cert_body
    
Current schema can be enforced by validation checks. Some checks are in place but not exhaustively.
In future, if more fields need to be added, we need to only change the validations.
    
**Usage via Curl**

This implementation has been hosted on a VM and below are
some examples of curl requests that can be sent to the server.

Add a customer: Returns ids of the customers added

`curl -H "Content-type: application/json" -X POST http://23.96.111.47:5002/customers -d
 '{"customers": [{"name":"abby", "email":"abby1@gmail", "passwd":"password123"},
  {"name":"cust1", "email":"e1", "passwd":"password456"}]}'`
  
Get all customers:

`curl -X GET http://23.96.111.47:5002/customers`

Add a certificate: Replace cust_id value with the customer id string returned in previous call. Returns ids of the certs added

`curl -H "Content-type: application/json" -X POST http://23.96.111.47:5002/certificates -d '{"certificates": [{"cust_id":"5baaf22c8eb1d1342b75589a","status":"A", "priv_key":"pvkey1", "cert_body":"certificatebody1"}, {"cust_id":"5baaeb5d8eb1d11eb4e355cb","status":"A", "priv_key":"pkabby", "cert_body":"certificatebody1"}]}'`

List active certificates for a customer: This is empty if there are no active certs for a customer.

`curl -X GET http://23.96.111.47:5002/customers/5baaf22c8eb1d1342b75589a/certificates`

Activate/Deactivate a certificate:

id here is the id of the certificate returned from create certificate call and status can be either "A" for active and "I" for inactive/deactivate.
This returns only the list of ids whose status changed from the old state and does not include the other ids.

`curl -H "Content-type: application/json" -X PUT http://23.96.111.47:5002/certificates/status -d '{"certificates": [{"id":"5baaf3308eb1d1342b75589c", "status":"I"}, {"id":"5baaf3308eb1d1342b75589d","status":"A"}]}'`

Delete/Remove a customer: 

Replace the value in the ids field here by the ids returned from create calls of customer.
This returns the count of deleted ids.

`curl -H "Content-type: application/json" -X DELETE http://23.96.111.47:5002/customers -d '{"customers": {"ids":["5baaf22c8eb1d1342b75589a", "5baaf2278eb1d1342b755898"]}}'`


Test Script

Including a curl_cmds script that runs all create positive cases and delete/PUT works if replaced with correct ids.

`python curl_cmds.py`

**Future Work**:

1. Validations to check if the object requested to be stored in the database confirms with our object parameters
2. Check before adding a certificate if the user exists in customer collection.
3. Add Docker support to project
4. Add Unit Tests
5. Returning specific error responses
6. setup logging

