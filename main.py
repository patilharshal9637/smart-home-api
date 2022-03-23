from email.policy import HTTP
import random

from sqlite3 import Timestamp
import string
from fastapi import FastAPI, Response,status
from pydantic import BaseModel
import uvicorn
from helper import data



app = FastAPI()
data = data.data




class Devices(BaseModel):
    room_name:str
    devices:dict
    timeStamp:str
    connection_gateway:str

class Register(BaseModel):
    email:str
    fname:str
    lname:str
    profile_img:str
    passwd:str



#defining some helping methods

#1:helping while authentication like is user exist ot not
def auth_check(email,passwd):
    
    for check_email in data["auth"]:
        if(check_email == email):
            user_data =data["auth"][email]
            if(user_data["passwd"] == passwd):
                return str(user_data["uid"])
            else:
                return "password didn't match"
    return "user not found"

#2:checkig user if already exist for registering new user in databse
def isExist(email:str):
    for check_email in data["auth"]:

        if(check_email == email):
            return True
            
    return False

#3:returning dictionary for storing data in auth key of data
def return_auth_dict(user:dict,uid:str):
    return {
        "email":user["email"],
        "passwd":user["passwd"],
        "uid":uid
    }

#4:returning dictionary for storing data in auth key of data
def return_user_dict(user:dict,uid:str):
    return {
        "uid":uid,
        "email":user["email"],
        "fname":user["fname"],
        "lname":user["lname"],
        "profile_img":user["profile_img"],
        
        
        
    }

#5:returning user data on request
def return_user_data(uid:str):
    usr_data = data["user"][str(uid)]
    if not usr_data:
        return "no data found"
    else:
        return usr_data


#6:generating uid for user
def get_random_string(length:int):
    # With combination of lower and upper case
    result_str =''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

#7:change applicances state
def change_applicances_state(serviceData: dict, room_name: str, device_name: str, state: bool):
    serviceData[room_name]["devices"][device_name] = state
    return "success"

#8:creating room prerequisites
def create_room_prequisites(serviceData, roomName):
    serviceData[roomName] = {
        "room_name": roomName,
        "devices": {

        }

    }
    return "success"

# 9:creating devices
def create_single_device(serviceData, roomName, deviceName):
    serviceData[roomName]["devices"][deviceName] = False
    return "success"



@app.get("/")
def initial():
    return data

@app.get("/auth/{email}&{passwd}")
def auth_validate(email:str,passwd:str):
    auth_data = auth_check(email=email,passwd=passwd)
 
    return auth_data

@app.get("/userdata/{uid}")
def userdata(uid:str):
    user_data = return_user_data(uid=uid)
    return user_data


@app.post("/register")
def register(new_user:Register):
    user = new_user.dict()
    print(user)
    check = isExist(email=user["email"])
    print(check)
    if(check):
        return "User already exist"
    else:
        
        uid = get_random_string(14)
        data["auth"][user["email"]] =return_auth_dict(user=user,uid=uid)
        data["user"][uid] = return_user_dict(user=user, uid=uid)
        data['services'][uid] = {

        }
        
    return "Account created successfully"


#updating appliances state
@app.patch("/services/{uid}/{room_name}/{device_name}&{state}")
def update_device_state(uid:str,room_name:str,device_name:str,state:bool):
    serviceData = data["services"][uid]
    
    status = change_applicances_state(serviceData,room_name=room_name,device_name=device_name,state=state)
    return status




#creating rooms
@app.put("/createroom/{uid}&{room_name}")
def create_rooms(uid: str, room_name:str):
    serviceData = data["services"][uid]
    status = create_room_prequisites(serviceData, room_name)
    return status

#get services data from uid
@app.get("/getservices/{uid}/{room_name}") 
def get_service_data(uid:str,room_name:str):
    serviceData = data["services"][uid]
    user_device_data = serviceData[room_name]["devices"]
    return user_device_data

#creating devices
@app.put("/services/{uid}/{room_name}/{device_name}")
def create_device(uid: str, room_name:str, device_name:str):
    serviceData = data["services"][uid]
    status = create_single_device(serviceData, room_name, device_name)
    return status


    
if __name__ == "__main__":
    uvicorn.run(app=app,port=8000,host="10.0.2.2")
