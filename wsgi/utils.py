def get_car(cars,id_car):
    if any(d['id_car'] == id_car for d in cars):
        position=[d['id_car'] == id_car for d in cars].index(True)
        return cars[position]
    else:
        return None
    
def update_fuelings(cars,fuelings):
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



def delete_fuelings(cars,fuelings):
    if type(fuelings) is list:
        for f in fuelings:
            car=get_car(cars,f['CarID'])
            if car != None:
                new_fuelings=car['fuelings']
                if any(d['ID'] == f['ID'] for d in new_fuelings):
                    position=[d['ID'] == f['ID'] for d in new_fuelings].index(True)
                    new_fuelings.remove(position)

                    
    if type(fuelings) is dict:
        car=get_car(cars,fuelings['CarID'])
        new_fuelings=car['fuelings']
        if car != None:
            if any(d['ID'] == fuelings['ID'] for d in new_fuelings):
                position=[d['ID'] == fuelings['ID'] for d in new_fuelings].index(True)
                new_fuelings.remove(position)

        
    


def delete_cars(old_cars,cars):
    if type(cars) is list:
        for c in cars:
            old_cars.remove(c)
    if type(cars) is dict:
        old_cars.remove(cars)
    
    return old_cars


def adding_cars(old_cars,cars):
    print type(old_cars)
    if type(cars) is list:
        for c in cars:
            if c not in old_cars:
                old_cars.append(c)
    if type(cars) is dict:
        if cars not in old_cars:
            old_cars.append(cars)

    return old_cars

        