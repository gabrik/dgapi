#!flask/bin/python
import os
from flask import Flask
from flask import request
from flask import Response
#import sys
#sys.path.append('../')
#from utils import *
import logging
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
        cars=user['cars']
        if cars == None:
            response={'request_id':id_user,'result':False}
        else:
            if type(fuelings) is list:
                for f in fuelings:
                    car=get_car(cars,f['CarID'])
                    if car != None:
                        new_fuelings=car['fuelings']
                        if any(d['ID'] == f['ID'] for d in new_fuelings):
                            position=[d['ID'] == f['ID'] for d in new_fuelings].index(True)
                            new_fuelings[position]=f
                        else:
                            new_fuelings.append(f)

            if type(fuelings) is dict:
                car=get_car(cars,fuelings['CarID'])
                new_fuelings=car['fuelings']
                if car != None:
                    if any(d['ID'] == fuelings['ID'] for d in new_fuelings):
                        position=[d['ID'] == fuelings['ID'] for d in new_fuelings].index(True)
                        new_fuelings[position]=fuelings
                    else:
                        new_fuelings.append(fuelings)


        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
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
        cars=user['cars']
        response={'request_id':id_user,'result':json.dumps(cars)}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')





@app.route('/del_fuelings',methods=['POST'])
def del_fuelings():
    id_user=request.form.get('id')
    fuelings=json.loads(request.form.get('fuel'))
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})    
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        cars=user['cars']
        #delete_fuelings(cars,fuelings)
        
        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')




@app.route('/del_cars',methods=['POST'])
def del_cars():
    id_user=request.form.get('id')
    cars=json.loads(request.form.get('car'))
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})    
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        new_cars=user['cars']
        if type(cars) is list:
            for c in cars:
                new_cars.remove(c)
        if type(cars) is dict:
            new_cars.remove(cars)
        
        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')



@app.route('/add_cars',methods=['POST'])
def add_cars():
    id_user=request.form.get('id')
    cars=json.loads(request.form.get('car'))
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})    
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        old_cars=user['cars']
        if type(cars) is list:
            for c in cars:
                if not any(d['id_car'] == c['id_car'] for d in old_cars):
                    old_cars.append(c)
        if type(cars) is dict:
            if not any(d['id_car'] == cars['id_car'] for d in old_cars):
                old_cars.append(cars)
        
        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')





@app.route('/register',methods=['POST'])
def register():

    username=request.form.get('name')
    id_user=request.form.get('id')
    '''
    car_model=request.form.get('car_model')
    car_manufacture=request.form.get('car_manufacture')
    car_fuel=request.form.get('car_fuel')
    '''
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    user={"Name": username,
    "id":id_user, 
    "cars":[]}

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
    
        



def get_car(cars,id_car):
    if any(d['id_car'] == id_car for d in cars):
        position=[d['id_car'] == id_car for d in cars].index(True)
        return cars[position]
    else:
        return None
    

if __name__ == "__main__":
    logging.warning('Start!!!')
    app.run()

