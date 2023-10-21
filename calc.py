#VERIFIED
def Tserving(d,v,Bfull,Bv,s,q,l,e):
    return Twait(q,l) + Tcharge(Bfull,Bv,s,d,e)

#VERIFIED
def Cost(d,v,Ppeak,Poff,peak,Bfull,Bv,Ptravel,e):
    if peak:
        return Ppeak*Evc(Bfull,Bv,d,e) + Ttravel(d,v) * Ptravel
    else:
        return Poff*Evc(Bfull,Bv,d,e) + Ttravel(d,v) * Ptravel
    
#VERIFIED
def Evc(Bfull,Bv,d,e):
    return Bfull - (Bv-Etravel(d,e))

#VERIFIED
def Etravel(d,e):
    return d*e

#VERIFIED
def Ttravel(d,v):
    return d/v

#VERIFIED
def Dmax(soc,Bfull,e):
    return (soc * Bfull)/e

#VERIFIED
def Twait(q,l):
    return q/l

#VERIFIED
def Tcharge(Bfull,Bv,s,d,e):
    return Evc(Bfull,Bv,d,e)/s


#VERIFIED
def calculate_grid_distance(car_location, station_location):
    car_x, car_y = car_location
    station_x, station_y = station_location
    
    steps_x = abs(station_x - car_x)
    steps_y = abs(station_y - car_y)
    
    total_steps = steps_x + steps_y
    
    return total_steps

def queue_length(solution, cs):
    length = 0
    for c in solution:
        if c==cs:
            length += 1
    return length