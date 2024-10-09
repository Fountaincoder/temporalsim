from temporallib import *

def updater(func):    
    def inner(unit):
        func(unit)
        for to, port in unit["to"]:
            units[to][port] = unit["out"]
    return inner


@updater
def bufferUpdate(unit):
    unit["out"] = unit["in"][unit["clock"]]
    unit["clock"] += 1

def tbufferUpdate(unit):
    if unit["t"]==1:
        unit["out"] = unit["in"][unit["clock"]] if unit["clock"] <= len(unit["in"])-1 else 0 
        unit["clock"] += 1
        for to, port in unit["to"]:
                units[to][port] += unit["out"]
    
def bufferReset(unit):
    unit["clock"] = 0
     
    
@updater
def collectUpdate(unit):
    unit["buf"]+= [unit["in"]]


@updater
def rbufferUpdate(unit):
    clockp = unit["clock"] % (len(unit["in"]))
    unit["clock"] = clockp + 1 
    unit["out"] = unit["in"][clockp]

@updater
def tempUpdate(unit):
    unit["out"] = unit["in"][unit["clock"]]
    unit["clock"] += 1

def finishUpdate(unit):
    return unit["in"]

def divmodUpdate(unit):
    # print(unit["rem"],unit["div"])
    
    unit["op1count"] += unit["op1"]  
    if unit["op1count"] < 2:
        if unit["op2"] == 0:
            unit["rem"] += 1
        else:
            unit["op2count"] +=1
            if unit["op2count"]==2: 
                unit["clock"] = unit["rem"]+1
                unit["op2count"]=0     
            unit["rem"] = 0
            unit["div"] += 1
        return False
    else:
        unit["div"] -= 1
        for  out, to, port ,utype in unit["to"]:
            units[to][port] = list(reversed(to_temporal(unit[out],utype)))
        unit["clock"] = 0
        unit["op1count"] = 0
        unit["op2count"] = 0
        unit["rem"] = 0
        unit["div"] = 0
        return True


def whileUpdate(unit):
    for to, port in unit["to"]:
        units[to][port] = unit["in"]

    return  unit["in"] == unit["zero"] or unit["in"] == 0 

     
def Rbuffer(n, to,  utype =  Unary.P1):
    return {"type": "rbuffer", "clock": 0, "in":list(reversed(to_temporal(n, utype))),
            "to" : to}


def Buffer(n, to,  utype =  Unary.P20):
    return {"type": "buffer", "clock": 0, "in":to_temporal(n, utype),
                        "to" : to}
                        
def TBuffer(n, to, t,  utype =  Unary.P20):
    return {"type": "tbuffer", "clock": 0, "in":to_temporal(n, utype),
                        "to" : to, "t":t}

def Finish():
    return {"type": "finish", "clock": 0, "in":0}                        

def DivMod(to,):
    return {"type": "divmod", "clock": 0, "to" : to,
        "op1":0,"op2":0, "op1count":0, "op2count":0, "div":0, "rem":0}


def Temp(to):
    return {"type": "temp", "to" : to, "in":0}

            
def While(to,utype = Unary.P1):
    return {"type": "while", "clock": 0, "in" : 0,  "to" : to, "zero" : to_temporal(0, utype) }


def tick(in_units):
    global units 
    units =  in_units
    divState = False
    finish = []
    for u in units:
        match u:
            case {"type":"buffer", **remainder} : bufferUpdate(u)
            case {"type":"rbuffer", **remainder} : rbufferUpdate(u)
            case {"type":"tbuffer", **remainder} : tbufferUpdate(u)
            case {"type":"divmod", **remainder} : divState =  divmodUpdate(u)
            case {"type":"while", **remainder} : pass 
            case {"type":"collector", **remainder} : collectUpdate(u)
            case {"type":"finish", **remainder} : finish = finishUpdate(u)
            case {"type":"temp", **remainder} : tempUpdate(u)
    return divState,finish


def reset(in_units):
    global units 
    units =  in_units
    whileState = False
    for u in units:
        match u:
            case {"type":"buffer", **remainder} : bufferReset(u)
            case {"type":"rbuffer", **remainder} : bufferReset(u)
            case {"type":"divmod", **remainder} : pass
            case {"type":"while", **remainder} : whileState = whileUpdate(u)
            case {"type":"collector", **remainder} : pass
            case {"type":"temp", **remainder} : pass
    return whileState
