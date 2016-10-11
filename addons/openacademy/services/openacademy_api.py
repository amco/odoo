import xmlrpclib

url = "http://127.0.0.1:8069"
dbname = "ao"
user = "admin"
password = "admin"

# version 2 of common webservices
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(dbname, user, password, {})

print uid

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/objects'.format(url))

session_ids = models.execute_kw(dbname, uid, password, "openacademy.session", "search", [()])

print session_ids

sessions = models.execute_kw(dbname, uid, password, "openacademy.session", "read", session_ids, {"fields": ["name", "code"]})

print len(sessions)
