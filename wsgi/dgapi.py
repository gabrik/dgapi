#!flask/bin/python
import os
from flask import Flask
from flask import request
import pymongo
import json
from bson import json_util
from bson import objectid
import re
from pymongo import MongoClient


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

@app.route('/')
def index():
    startpage={'error':'wrong page'}
    return json.dumps(startpage,indent=None)

@app.route('/put_fuelings',methods=['POST'])
def put_fuelings():
    fuelings=request.form.get('fuel')
    user_id=request.form.get('user')
    print fuelings
    print user_id

    return "ok"

@app.route('/get_fuelings',methods=['POST'])
def test():
    return "ok"


@app.route('/register',methods=['POST'])
def register():


    username=request.form.get('name')
    id_user=request.form.get('id')
    car_model=request.form.get('car_model')
    car_manufacture=request.form.get('car_manufacture')
    car_fuel=request.form.get('car_fuel')

    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    user={"Name": username,
    "id":id_user, 
    "car_model":car_model ,
    "car_manufacture": car_manufacture,
    "car_fuel":car_fuel,
    "fuelings":[]}


    users=db.users
    return_value = users.insert_one(user).inserted_id

    return {'request_id':id_user,'result':return_value}



@app.route('/login',methods=['POST'])
def login():
    return 'ok'

    

if __name__ == "__main__":
    app.run()

''' 
params.put("name", DGConfigu
 params.put("id",DGConfigurat
 params.put("car_model",DGCon
 params.put("car_manufacture"
 params.put("car_fuel",DGConf
 '''