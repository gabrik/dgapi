#!flask/bin/python
import os
from flask import Flask
from flask import request
from flask import Response
import json
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
    fuelings=json.loads(request.form.get('fuel'))
    id_user=request.form.get('id')
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        new_fuelings=user['fuelings']
        new_fuelings.append(fuelings)
        result=users.update_one({"id": id_user},{'$set':{'fuelings': new_fuelings }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')

@app.route('/get_fuelings',methods=['POST'])
def get_fuelings():
    id_user=request.form.get('id')
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        fuelings=user['fuelings']
        response={'request_id':id_user,'result':json.dumps(fuelings)}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')


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
    response={'request_id':id_user,'result':str(return_value)}
    return Response(json.dumps(response,indent=None),mimetype='application/json')



@app.route('/login',methods=['POST'])
def login():
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    id_user=request.form.get('id')
    user=users.find_one({"id": id_user})
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        user.pop("_id",None)
        response={'request_id':id_user,'result':json.dumps(user,indent=None)}

    return Response(json.dumps(response,indent=None),mimetype='application/json')
    
        

    

if __name__ == "__main__":
    app.run()

