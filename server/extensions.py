from pymongo import MongoClient
import os

mongo = os.getenv("mongo")
if not mongo:
    mongo = "localhost:27017"

print(f"Running quokka-prime with Mongo: {mongo}")

client = MongoClient(host=[mongo])
if "TESTDB" not in os.environ:
    db = client.quokkadb
else:
    client.drop_database("testdb")
    db = client.testdb
