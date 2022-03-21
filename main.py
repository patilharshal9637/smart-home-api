from email.policy import HTTP
import random

from sqlite3 import Timestamp
import string
from fastapi import FastAPI, Response,status
from pydantic import BaseModel
import uvicorn



app = FastAPI()
data ={
    "auth":{
        "patil.sanket18@outlook.com":{
            "email":"patil.sanket18@outlook.com",
            "passwd":"Sanket@123",
            "uid":"7219442303"
        },
        "psanket18052001@gmail.com":{
            "email":"psanket18052001@gmail.com",
            "passwd":"Sanket@123",
            "uid":"7709982500"
        }
    },
    "user":{
        "7219442303":{
            "email":"patil.sanket18@outlook.com",
            "fname":"Sanket",
            "lname":"Patil",
            "profile_img":"http://this.is.pic",
            "service":{
                "living_room":{
                    "room_name":"Living Room",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"12032022 11:30AM",
                    "connection_gateway":"192.168.43.1"
                },
                "bedroom":{
                    "room_name":"Bed Room",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"13032022 16:30PM",
                    "connection_gateway":"192.168.43.2"
                },
                "kitchen":{
                    "room_name":"Kitchen",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"14032022 7:30AM",
                    "connection_gateway":"192.168.43.3"
                }
            }

        },
        "7709982500":{
                "email":"psanket18052001@gmail.com",
            "fname":"Sanket",
            "lname":"Patil",
            "profile_img":"http://this.is.pic",
            "service":{
                "living_room":{
                    "room_name":"Living Room",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"12032022 11:30AM",
                    "connection_gateway":"192.168.43.1"
                },
                "bedroom":{
                    "room_name":"Bed Room",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"13032022 16:30PM",
                    "connection_gateway":"192.168.43.2"
                },
                "kitchen":{
                    "room_name":"Kitchen",
                    "device":{
                        "tv":True,
                        "light":False,
                        "washing_machine":True,
                        "fan":True
                    },
                    "time_stamp":"14032022 7:30AM",
                    "connection_gateway":"192.168.43.3"
                }
            }
        }
    }
}



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
    service:dict
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
        "service":user["service"]
        
        
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
def change_applicances_state(user_data:dict,room_name:str,device_name:str,state:bool):
    service = user_data["service"]
    try:
        service[room_name]["device"][device_name] = state
        return "success"
    except:
        return "failure"



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
        data["user"][uid] = return_user_dict(user=user,uid=uid)
        
    return "Account created successfully"


#updating appliances state
@app.put("/service/{uid}&{room_name}&{device_name}&{state}")
def update_device_state(uid:str,room_name:str,device_name:str,state:bool):
    user_data = return_user_data(uid=uid)
    status = change_applicances_state(user_data=user_data,room_name=room_name,device_name=device_name,state=state)
    return status


    
if __name__ == "__main__":
    uvicorn.run(app=app,port=8000,host="10.0.2.2")