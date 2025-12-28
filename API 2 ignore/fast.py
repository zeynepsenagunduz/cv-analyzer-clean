from fastapi import FastAPI, File, UploadFile
from  pydantic import BaseModel
import hashlib
import time
from werkzeug.utils import secure_filename
import os 
from helper import allowed_file, handleCV, processJobText, create_point, pdf_to_text
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import json
import psycopg2
from pydantic import BaseModel
import jwt


class Login(BaseModel):
    username: str
    password: str

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    jobtext: str


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.post("/login")
async def login(data: Login):
    conn = psycopg2.connect(host="103.47.57.28",database="tez",user="postgres",password="kadir123X")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username='{data.username}' AND password='{data.password}'")
    conn.commit()
    returnData = cursor.fetchone()
    if(returnData):
        encoded = jwt.encode({"userId": int(returnData[0])}, "secret", algorithm="HS256")
        return {"token": encoded}
    cursor.close()
    
   
    return {"message": "Login successful"}



@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if(not allowed_file(file.filename, ALLOWED_EXTENSIONS)):
        return {"error": "File type is not allowed"}
    filename = hashlib.sha256(secure_filename(file.filename.replace(".pdf",'') + str(time.time()).replace('.','')).encode('utf-8')).hexdigest() + '.' + file.filename.rsplit('.', 1)[1].lower()
    with open(os.path.join(f"./static/files/{file.filename.replace('.pdf','')}", filename), "wb") as f:
        f.write(contents)
    return {'message' : 'Files successfully uploaded','filename':filename}
    

@app.post("/process-cv")
async def processCV(filename: str):
    allTextList = handleCV(filename)
    return {'message': 'CV successfully processed','textList': allTextList}


@app.post('/jobpost')
async def jobpost(item: Item):

    mylist = processJobText(item.jobtext)
    return {'message': 'CV successfully processed','textList': list(set(mylist)) }

@app.post("/best-job")
async def getPoint(file: UploadFile = File(...)):
   
    contents = await file.read()
    if(not allowed_file(file.filename, ALLOWED_EXTENSIONS)):
        return {"error": "File type is not allowed"}
    
    with open(os.path.join("./temp/", "kadir"), "wb") as f:
        f.write(contents)
    
    cv_keywords = processJobText(pdf_to_text())

    conn = psycopg2.connect(
    host="103.47.57.28",
    database="tez",
    user="postgres",
    password="kadir123X")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobposts")
    jobs = cursor.fetchall()

    scores = {}
    for count,job in enumerate(jobs):
        scores[job[0]] = create_point(cv_keywords, json.loads(job[2]))
    # sort dict by value
    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

    print(sorted_scores)

    
    # top 5 item with key and value
    best_job_keywords = []
    for job in jobs:
        if(job[0] == list(sorted_scores.keys())[0]):
            best_job_keywords = json.loads(job[2])
            break

    return {'point':sorted_scores, "top_five": list(sorted_scores.items())[:5], "cv_keywords": cv_keywords, "best_job_keywords": best_job_keywords}


class jobPost(BaseModel):
    jobPost: str


@app.post("/best-applicant")
async def getPoint(jobPost: jobPost):
   
    job_keywords = processJobText(jobPost.jobPost)

    # print("jobKeywords: ", job_keywords)


    conn = psycopg2.connect(
    host="103.47.57.28",
    database="tez",
    user="postgres",
    password="kadir123X")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cvs")
    cvs = cursor.fetchall()

    scores = {}
    for cv in cvs:
        # print("cv: ", cv[3])
        scores[cv[0]] = create_point(json.loads(cv[3]), job_keywords)
        # print("point: ", create_point(cv[3], job_keywords))
    # sort dict by value
    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

    print(scores)

    
    # # top 5 item with key and value
    # best_job_keywords = []
    # for job in jobs:
    #     if(job[0] == list(sorted_scores.keys())[0]):
    #         best_job_keywords = json.loads(job[2])
    #         break

    best_cv_keywords = []
    for cv in cvs:
        if(cv[0] == list(sorted_scores.keys())[0]):
            best_cv_keywords = json.loads(cv[3])
            break

    return {'point':sorted_scores, "top_five": list(sorted_scores.items())[:5], "job_keywords": job_keywords, "best_cv_keywords":  best_cv_keywords  }




