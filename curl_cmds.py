import os

"""TEST CREATE CUSTOMER"""
#curl -H "Content-type: application/json" -X POST http://23.96.111.47:5002/customers -d '{"customers": [{"name":"abby", "email":"abby1@gmail", "passwd":"password123"},{"name":"cust1", "email":"e1", "passwd":"password456"}]}'
os.system("curl -H \"Content-type: application/json\" -X POST http://23.96.111.47:5002/customers -d \'{\"customers\":[{\"name\":\"abby\", \"email\":\"e1\",\"passwd\":\"pass345\"}, {\"name\":\"cust1\", \"email\":\"e2\",\"passwd\":\"pass123\"}]}\'")

print "\n"
print "\n"

"""TEST CREATE CERT"""
#curl -H "Content-type: application/json" -X POST http://23.96.111.47:5002/certificates -d '{"certificates": [{"cust_id":"5baaf22c8eb1d1342b75589a","status":"A", "priv_key":"pvkey1", "cert_body":"certificatebody1"}, {"cust_id":"5baaf22c8eb1d1342b75589a","status":"A", "priv_key":"pkabby", "cert_body":"certificatebody1"}]}'
"""replace the cust_id to run"""
os.system("curl -H \"Content-type: application/json\" -X POST http://23.96.111.47:5002/certificates -d '{\"certificates\": [{\"cust_id\":\"5baaf22c8eb1d1342b75589a\",\"status\":\"A\", \"priv_key\":\"e1\", \"cert_body\":\"5678\"}, {\"cust_id\":\"5baaf22c8eb1d1342b75589a\",\"status\":\"A\", \"priv_key\":\"e2\", \"cert_body\":\"1234\"}]}'")

print "\n"
print "\n"

"""TEST DELETE"""
#curl -H "Content-type: application/json" -X DELETE http://23.96.111.47:5002/customers -d '{"customers": {"ids":["5ba7204c8eb1d10f81579bee", "5ba7204c8eb1d10f81579bed"]}}'`
os.system("curl -H \"Content-type: application/json\" -X DELETE http://23.96.111.47:5002/customers -d \'{\"customers\": {\"ids\":[\"5ba7204c8eb1d10f81579bee\", \"5ba721728eb1d110a20efed2\"]}}\'")

print "\n"
print "\n"

"""TEST GET ACTIVE CERTS"""
#curl -X GET http://23.96.111.47:5002/customers/5baaf2278eb1d1342b755898/certificates
os.system("curl -X GET http://23.96.111.47:5002/customers/cust1/certificates")

print "\n"
print "\n"

"""TEST ACTIVATE/DEACTIVATE CERTIFICATE"""
#curl -H "Content-type: application/json" -X PUT http://23.96.111.47:5002/certificates/status -d '{"certificates": [{"id""5ba9c0bc8eb1d10b68e43c6f", "status":"I"}, {"id":"5ba9c0bc8eb1d10b68e43c70","status":"A"}]}'`

os.system("curl -H \"Content-type: application/json\" -X PUT http://23.96.111.47:5002/certificates/status -d '{\"certificates\": [{\"id\":\"5baab9f58eb1d17c512fedc3\", \"status\":\"I\"}, {\"id\":\"5baab9f58eb1d17c512fedc2\",\"status\":\"I\"}]}'")


