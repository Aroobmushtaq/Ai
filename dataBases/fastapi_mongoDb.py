from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from bson.objectid import ObjectId  
import os
load_dotenv()
print(os.getenv("DB_URI"))
app = FastAPI()
def get_db():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("connected to the Database")
        return client
    except Exception as e:
        print(f"error to connected to DB :{e}")
        return None

client = get_db()
if client:
    db = client["firstDB"]
    # collection = db["studentData"]
else:
    print("database not connected")

class Student(BaseModel):
    name: str
    age: str
    email: str

@app.get("/")
def cheking():
    return{"All":"Good"}
@app.get("/allData")
def all_Data():
    try:
        studentData=db.studentData.find()
        newData=[]
        for data in studentData:
            newData.append({
                "id":str(data["_id"]),
                "name":data["name"],
                "age":data["age"],
                "email":data["email"]
            })
        return{
            "data":newData,
            "message":"fetch all data successfully",
            "status":"success",
            "error":None
        }
    except Exception as e:
        print(f"Error to reading data :{e}")
        return{
            "data":[],
            "status":"Failed",
            "message": "not fetched data vform database due to error",
            "error":str(e)
        }
