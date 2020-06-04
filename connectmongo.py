from pymongo import MongoClient
import credentials
import ssl

username = ""     # change username
password = ""     # change password

if not username or not password:
    username = credentials.username
    password = credentials.password

connect_str = "mongodb+srv://{}:{}@cluster0-hvt3i.gcp.mongodb.net/test?retryWrites=true&w=majority".format(username,password)

client = MongoClient(connect_str,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
"""
# This is used to check connection working
# check client connection
dbs_names = client.list_database_names()
print(dbs_names)

# check freeway's collection
collection_names = client.freeway.list_collection_names()
print(collection_names)
"""

# Input collection
freeway = client['freeway']
loop = freeway['loop']
stations = freeway['stations']