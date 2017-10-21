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
BASE = "/dgapi"


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

@app.route(BASE +'/')
def index():
    startpage={'error':'wrong page'}
    return json.dumps(startpage,indent=None)

@app.route(BASE +'/put_fuelings',methods=['POST'])
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

@app.route(BASE +'/get_fuelings',methods=['POST'])
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





@app.route(BASE +'/del_fuelings',methods=['POST'])
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
        delete_fuelings(cars,fuelings)
        
        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')




@app.route(BASE +'/del_cars',methods=['POST'])
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
        old_cars=user['cars']
        if type(cars) is list:
            for c in cars:
                car=get_car_position(old_cars,c['id_car'])
                if car != None:
                    old_cars.pop(car)
        if type(cars) is dict:
            car=get_car_position(old_cars,cars['id_car'])
            if car != None:
                    old_cars.pop(car)
            
        result=users.update_one({"id": id_user},{'$set':{'cars': old_cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')



@app.route(BASE +'/add_cars',methods=['POST'])
def add_cars():
    app.logger.warning('add cars!!!')
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
                c['fuelings']=[]
                if not any(d['id_car'] == c['id_car'] for d in old_cars):
                    old_cars.append(c)
        if type(cars) is dict:
            cars['fuelings']=[]
            if not any(d['id_car'] == cars['id_car'] for d in old_cars):
                old_cars.append(cars)
        result=users.update_one({"id": id_user},{'$set':{'cars': old_cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')


@app.route(BASE +'/put_costs',methods=['POST'])
def put_costs():
    costs=json.loads(request.form.get('cost'))
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
            if type(costs) is list:
                for c in costs:
                    car=get_car(cars,f['CarID'])
                    if car != None:
                        old_costs=car.get('costs',None)
                        if old_costs==None:
                            car['costs']=[]
                            old_costs=car['costs']
                        
                        if any(d['ID'] == f['ID'] for d in old_costs):
                            position=[d['ID'] == f['ID'] for d in old_costs].index(True)
                            old_costs[position]=c
                        else:
                            old_costs.append(f)

            if type(costs) is dict:
                car=get_car(cars,costs['CarID'])
                if car != None:
                    old_costs=car.get('costs',None)
                    if old_costs==None:
                            car['costs']=[]
                            old_costs=car['costs']
                            
                            
                    if any(d['ID'] == costs['ID'] for d in old_costs):
                        position=[d['ID'] == costs['ID'] for d in old_costs].index(True)
                        old_costs[position]=costs
                    else:
                        old_costs.append(costs)
                    


        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')


@app.route(BASE +'/del_costs',methods=['POST'])
def del_costs():
    id_user=request.form.get('id')
    costs=json.loads(request.form.get('cost'))
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db=client[os.environ['OPENSHIFT_APP_NAME']]
    users=db.users
    user=users.find_one({"id": id_user})    
    if user == None:
        response={'request_id':id_user,'result':False}
    else:
        cars=user['cars']
        delete_costs(cars,costs)
        
        result=users.update_one({"id": id_user},{'$set':{'cars': cars }}).modified_count
        response={'request_id':id_user,'result':str(user['_id'])}
    
    return Response(json.dumps(response,indent=None),mimetype='application/json')

@app.route(BASE +'/register',methods=['POST'])
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

    u=users.find_one({"id": id_user})  

    if u==None:
        return_value = users.insert_one(user).inserted_id
    else:
        return_value = -1

    response={'request_id':id_user,'result':str(return_value)}
    return Response(json.dumps(response,indent=None),mimetype='application/json')



@app.route(BASE +'/login',methods=['POST'])
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
    
        

def get_car_position(cars,id_car):
    if any(d['id_car'] == id_car for d in cars):
        position=[d['id_car'] == id_car for d in cars].index(True)
        return position
    else:
        return None

def get_car(cars,id_car):
    if any(d['id_car'] == id_car for d in cars):
        position=[d['id_car'] == id_car for d in cars].index(True)
        return cars[position]
    else:
        return None
    

if __name__ == "__main__":
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.logger.warning('Start!!!')
    app.run()

def delete_fuelings(cars,fuelings):
    if type(fuelings) is list:
        for f in fuelings:
            car=get_car(cars,f['CarID'])
            if car != None:
                new_fuelings=car['fuelings']
                if any(d['ID'] == f['ID'] for d in new_fuelings):
                    position=[d['ID'] == f['ID'] for d in new_fuelings].index(True)
                    new_fuelings.pop(position)

                    
    if type(fuelings) is dict:
        car=get_car(cars,fuelings['CarID'])
        new_fuelings=car['fuelings']
        if car != None:
            if any(d['ID'] == fuelings['ID'] for d in new_fuelings):
                position=[d['ID'] == fuelings['ID'] for d in new_fuelings].index(True)
                new_fuelings.pop(position)


def delete_costs(cars,costs):
    if type(costs) is list:
        for c in costs:
            car=get_car(cars,f['CarID'])
            if car != None:
                old_costs=car.get('costs',None)
                if old_costs==None:
                    car['costs']=[]
                    old_costs=car['costs']
                if any(d['ID'] == c['ID'] for d in old_costs):
                    position=[d['ID'] == c['ID'] for d in old_costs].index(True)
                    old_costs.pop(position)

                    
    if type(costs) is dict:
        car=get_car(cars,costs['CarID'])
        if car != None:
            old_costs=car.get('costs',None)
            if old_costs==None:
                car['costs']=[]
                old_costs=car['costs']
            if any(d['ID'] == costs['ID'] for d in old_costs):
                position=[d['ID'] == costs['ID'] for d in old_costs].index(True)
                old_costs.pop(position)