from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("request",request)
    print("call_next",call_next)
    response = await call_next(request)
    response.headers["X-Process-Time"] = "10 sec"
    return response
@app.get("/")
def read_root():
    return{"message": "server is running"}