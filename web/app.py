import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId 

application = Flask(__name__, template_folder='template')

# default_mongo_uri = "mongodb://127.0.0.1:27017/detection"
# application.config["MONGO_URI"] = os.getenv("MONGO_URI", default_mongo_uri)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin'


mongo = PyMongo(application)
db = mongo.db

@application.route("/")
def lists ():
	curs = db.object.find()
	a1="active"
	return render_template('index.html',a1=a1,curs=curs)

@application.route("/action", methods=['POST'])
def action ():
	Name=request.values.get("Name")
	Confidence=request.values.get("Confidence")
	DateTime=request.values.get("DateTime")
	db.object.insert_one({ "Name":Name, "Confidence":Confidence, "DateTime":DateTime})
	return redirect("/")

@application.route("/remove")
def remove ():
	key=request.values.get("_id")
	db.object.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@application.route("/update")
def update ():
	key=request.values.get("_id")
	curs=db.object.find({"_id":ObjectId(key)})
	return render_template('update.html',curs=curs)

@application.route("/action3", methods=['POST'])
def action3 ():
	Name=request.values.get("Name")
	Confidence=request.values.get("Confidence")
	DateTime=request.values.get("DateTime")
	key=request.values.get("_id")
	db.object.update_one({"_id":ObjectId(key)}, {'$set':{"Name":Name, "Confidence":Confidence, "DateTime":DateTime}})
	return redirect("/")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5500, debug=True)