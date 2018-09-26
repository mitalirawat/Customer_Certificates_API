# Customer Certificates

This repository implements a basic RESTful HTTP API for creating customers and their certificates, listing active certificates
and deleting customers

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
  
Add a certificate: Returns ids of the certs added

`curl -H "Content-type: application/json" -X POST http://23.96.111.47:5002/certificates -d '{"certificates": [{"cust_id":"cust1","status":"A", "priv_key":"pvkey1", "cert_body":"certificatebody1"}, {"cust_id":"abby","status":"A", "priv_key":"pkabby", "cert_body":"certificatebody1"}]}'`

List active certificates for a customer: This is empty if there are no active certs for a customer.

`curl -X GET http://23.96.111.47:5002/customers/cust1/certificates`

Delete/Remove a customer: 

Replace the value in the ids field here by the ids returned from create calls of customer.
This returns the entire list of ids sent for deletion even if the id does not exist. Future work to return only the ids
that were present and got actually deleted.

`curl -H "Content-type: application/json" -X DELETE http://23.96.111.47:5002/customers -d '{"customers": {"ids":["5ba7204c8eb1d10f81579bee", "5ba7204c8eb1d10f81579bed"]}}'`

Activate/Deactivate a certificate:

id here is the id of the certificate returned from create certificate call and status can be either "A" for active and "I" for inactive/deactivate.
This returns only the list of ids whose status changed from the old state and does not include the other ids.

`curl -H "Content-type: application/json" -X PUT http://23.96.111.47:5002/certificates/status -d '{"certificates": [{"id""5ba9c0bc8eb1d10b68e43c6f", "status":"I"}, {"id":"5ba9c0bc8eb1d10b68e43c70","status":"A"}]}'`

**Future Work**:

1. Validations to check if the object requested to be stored in the database confirms with our object parameters
2. Add Docker support to project
3. Add Unit Tests
4. Returning specific error responses
5. setup logging

