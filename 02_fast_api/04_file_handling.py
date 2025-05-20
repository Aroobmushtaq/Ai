# 📦 Import necessary modules
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import shutil
import os

#  Define the folder where uploaded files will be saved
UPLOAD_FOLDER = "03_fastapi/uploads"

#  Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#  Initialize the FastAPI app
app = FastAPI()

#  Mount the uploads folder as a static directory
# This allows files in the uploads folder to be accessed via URL
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")

#  File upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    #  Create the full path to save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    #  Save the uploaded file to the defined path using binary write mode
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #  Create the URL that can be used to access the uploaded file
    file_url = f"/static/{file.filename}"

    #  Return the filename and the public URL to access it
    return {"filename": file.filename, "file_url": file_url}
