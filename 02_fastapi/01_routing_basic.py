from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_hello_world():
    return{"hello":"world"}