#!flask/bin/python
import os
from flask import Flask
from flask import request
import pymongo
import json
from bson import json_util
from bson import objectid
import re

app = Flask(__name__)
#add this so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True



#return a specific park given it's mongo _id
@app.route("/ws/parks/park/<parkId>")
def onePark(parkId):
    #setup the connection
    #conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    #db = conn[os.environ['OPENSHIFT_APP_NAME']]

    #query based on the objectid
    #result = db.parkpoints.find({'_id': objectid.ObjectId(parkId)})

    #turn the results into valid JSON
    #return str(json.dumps({'results' : list(result)},default=json_util.default))
    return parkId

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"
    
#need this in a scalable app so that HAProxy thinks the app is up
@app.route("/")
def blah():
    return "hello world"

if __name__ == "__main__":
    app.run()

