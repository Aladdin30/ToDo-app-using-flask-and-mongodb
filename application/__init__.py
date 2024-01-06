from flask import Flask
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config["SECRET_KEY"]="7da5fcccf8a565554b88bd4164670f7af0aa9be0"
app.config["MONGO_URI"]="mongodb+srv://root:331332333@cluster0.3igwo8i.mongodb.net/flask?retryWrites=true&w=majority"

mongodb_client= PyMongo(app)
db=mongodb_client.db
from application import routes