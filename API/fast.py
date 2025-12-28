from fastapi import FastAPI, File, UploadFile,HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from helper import allowed_file, handleCV, processJobText, create_point, pdf_to_text,remove_special_characters
from fastapi.middleware.cors import CORSMiddleware
from db import get_db_connection
import json
import os 
import uuid


class Login(BaseModel):
    username: str
    password: str

class BestJobs(BaseModel):
    userid: str


class Register(BaseModel):
    username: str
    mail: str
    password: str
    role: str
    has_cv: bool
    has_jobpost: bool

class AddCourses(BaseModel):
    name: str
    keywords: str
    link: str
    id: int = None

app = FastAPI()

app.mount("/static/cvs", StaticFiles(directory="./static/cvs"), name="static")
app.mount("/static/jobposts", StaticFiles(directory="./static/jobposts"), name="static")

# CORS ayarları
origins = [
    "*"  # Tüm originlere izin ver
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm headerlara izin ver
    expose_headers=["*"],  # Tüm headerları expose et
    max_age=3600,  # Preflight isteklerinin cache süresi (saniye)
)

class Item(BaseModel):
    jobtext: str

ALLOWED_EXTENSIONS = set(['pdf','txt'])

@app.post("/login")
async def login(data: Login):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (data.username, data.password))
    returnData = cursor.fetchone()
    
    if(returnData == None):
        conn.close()
        return {"message": "Login failed"}
    else:
        # Debug: Tüm sütunları ve değerlerini yazdır
        print(f"Login result - Full row: {dict(returnData)}")
        print(f"Login result - All columns: {returnData.keys() if hasattr(returnData, 'keys') else 'No keys'}")
        print(f"Login result - Index 0 (id): {returnData[0]}")
        print(f"Login result - Index 1 (username): {returnData[1]}")
        print(f"Login result - Index 2 (email): {returnData[2]}")
        print(f"Login result - Index 3 (password): {returnData[3]}")
        print(f"Login result - Index 4 (role): {returnData[4]}")
        print(f"Login result - Index 5 (has_cv): {returnData[5]}")
        print(f"Login result - Index 6 (has_jobpost): {returnData[6]}")
        print(f"Login result - Index 7 (credit): {returnData[7] if len(returnData) > 7 else 'N/A'}")
        
        # Hem index hem de sütun ismiyle erişmeyi dene
        try:
            role_by_name = returnData['role']
            print(f"Role by name ['role']: {role_by_name}")
        except Exception as e:
            print(f"Error accessing role by name: {e}")
        
        role_value = returnData[4]  # Index 4 = role sütunu
        print(f"Role value (index 4): {role_value}, Type: {type(role_value)}")
        
        conn.close()
        return {
            "userid": int(returnData[0]), 
            "role": str(returnData[4]),  # Index 4 kullan
            "has_cv": bool(returnData[5]), 
            "has_jobpost": bool(returnData[6])
        }


@app.post("/register")
async def register(data: Register):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (data.username,))
    result = cursor.fetchone()
    if result:
        conn.close()
        return {"message": "Username already exists"}
    print(f"Register - Role value: {data.role}, Type: {type(data.role)}")
    cursor.execute("INSERT INTO users (username, email, password, role, has_cv, has_jobpost) VALUES (?, ?, ?, ?, ?, ?)", 
                   (data.username, data.mail, data.password, str(data.role), 0, 0))
    conn.commit()
    
    # Kaydedilen değeri kontrol et
    cursor.execute("SELECT role FROM users WHERE username=?", (data.username,))
    saved_role = cursor.fetchone()
    print(f"Register - Saved role value: {saved_role['role'] if saved_role else 'None'}, Type: {type(saved_role['role']) if saved_role else 'None'}")
    
    conn.close()
    return {"message": "Registration successful"}



@app.post("/upload/cv")
async def create_upload_file(userid: str, file: UploadFile = File(...)):
    contents = await file.read()
    if(not allowed_file(file.filename, ALLOWED_EXTENSIONS)):
        return {"error": "File type is not allowed"}
    filename = userid
    with open(f"./static/cvs/{userid}.pdf", "wb") as f:
        f.write(contents)

    conn = get_db_connection()
    cursor = conn.cursor()      
    cursor.execute("UPDATE users SET has_cv = 1 WHERE id = ?", (userid,))
    cv_keywords = json.dumps(handleCV(f'{userid}.pdf'))
    print('--------------')
    print(cv_keywords)
    cursor.execute("INSERT INTO cvs (userid, keywords) VALUES (?, ?)", (userid, cv_keywords))
    conn.commit()
    conn.close()

    return {'message' : 'Files successfully uploaded'}

""""
@app.post("/upload/jobpost")
async def create_upload_file(userid: str, file: UploadFile = File(...)):
    contents = await file.read()
    if(not allowed_file(file.filename, ['txt'])):
        return {"error": "File type is not allowed"}
    filename = userid
    with open(f"./static/jobposts/{userid}.txt", "wb") as f:
        f.write(contents)

        

    conn = get_db_connection()
    cursor = conn.cursor()      
    cursor.execute("UPDATE users SET has_jobpost = 1 WHERE id = ?", (userid,))
    conn.commit()
    conn.close()
    return {'message' : 'Files successfully uploaded'}
   
"""

@app.post("/upload/jobpost")
async def create_upload_file(userid: str, file: UploadFile = File(...)):
    contents = await file.read()

    if not allowed_file(file.filename, ['txt']):
        return {"error": "File type is not allowed"}

      

    os.makedirs("./static/jobposts", exist_ok=True)
    with open(f"./static/jobposts/{userid}.txt", "wb") as f:
        f.write(contents)

    
    try:
        job_text = contents.decode("utf-8")
    except UnicodeDecodeError:
        job_text = contents.decode("iso-8859-1", errors="ignore")

    job_text = job_text.strip()

    # Keyword çıkar
    job_keywords = processJobText(job_text)

    # jobpost + keyword kaydet + has_jobpost güncelle
    conn = get_db_connection()
    cursor = conn.cursor()
   
    cursor.execute("UPDATE users SET has_jobpost = 1 WHERE id = ?", (userid,))

    cursor.execute(
        "INSERT INTO jobposts (jobpost, jobpost_keywords,userid) VALUES (?, ?, ?)",
        (job_text, json.dumps(job_keywords), userid)
    )
    conn.commit()
    conn.close()

    return {"message": "Jobpost uploaded and saved to database"}







def recommenderFunction(jobKeywords, cvKeywords):
    # this function gets best job match keywords and user cv keywords. Extracts not matching keywords and searches 
    # if there is any course that matches with not matching keywords. If there is, it returns that course.
    # jobKeywords is list 
    # cvKeywords is list
    courses = []
    notMatchingKeywords = []
    for keyword in jobKeywords :
        if keyword not in cvKeywords:
            notMatchingKeywords.append(keyword)
    
    if(len(notMatchingKeywords) == 0):
        return None
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        for i in notMatchingKeywords:
            cursor.execute("SELECT * FROM courses WHERE keywords LIKE ?", (f'%{i}%',))
            result = cursor.fetchall()
            if(result != None):
                for course in result:
                    courses.append(list(course))
        conn.close()


    return courses
    

@app.post("/best-job")
async def getPoint(userid: BestJobs):

    cv_keywords = processJobText(pdf_to_text(userid.userid))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobposts")
    jobs = cursor.fetchall()

    scores = {}
    for count,job in enumerate(jobs):
        print("jobs")
        if len(jobs) > 0:
            print(job[2] if len(job) > 2 else "N/A")
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

        #  "top_five": [
        #         [
        #         13,
        #         85.71428571428571
        #         ],
        #         [
        #         181,
        #         85.71428571428571
        #         ],
        #         [
        #         53,
        #         83.33333333333334
        #         ],
        #         [
        #         65,
        #         83.33333333333334
        #         ],
        #         [
        #         68,
        #         83.33333333333334
        #         ]
        #     ]
    
    new_list = list(sorted_scores.items())[:5].copy()
    
    for count,i in enumerate(list(sorted_scores.items())[:5]):
        cursor.execute("SELECT jobpost, jobpost_keywords FROM jobposts WHERE id=?", (i[0],))
        result = cursor.fetchone()
        new_list[count] = {"text": result[0], "keywords": remove_special_characters(result[1]).split(' '), "point": int(i[1])}

    conn.close()
    courses = recommenderFunction(best_job_keywords, cv_keywords)
    return {"top_five": new_list, "cv_keywords": cv_keywords, "best_job_keywords": best_job_keywords,"courses": courses}


@app.post("/best-applicant")
async def getPoint(userid: str):

    with open(f"./static/jobposts/{userid}.txt", "r") as f:
        jobtext = f.read()
   
    job_keywords = processJobText(jobtext)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cvs")
    cvs = cursor.fetchall()

    scores = {}
    for cv in cvs:
        scores[cv[1]] = create_point(json.loads(cv[2]), job_keywords)
    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

    best_cv_keywords = []
    for cv in cvs:
        if(cv[1] == list(sorted_scores.keys())[0]):
            best_cv_keywords = json.loads(cv[2])
            break
    
    new_list = list(sorted_scores.items())[:5].copy()

    for count,i in enumerate(list(sorted_scores.items())[:5]):
        new_list[count] = {"userid": i[0], "point": int(i[1])}

    conn.close()

    return {"top_five": new_list , "job_keywords": job_keywords, "best_cv_keywords":  best_cv_keywords  }




@app.get("/get-credit")
async def getPoint(userid: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT credit FROM users WHERE id=?", (userid,))
    credit = cursor.fetchone()[0]
    conn.close()
    return {
        "credit": credit
    }

@app.post("/set-credit")
async def getPoint(userid: str, amount: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT credit FROM users WHERE id=?", (userid,))
    credit = cursor.fetchone()[0]

    newCredit = credit + amount

    try:
        cursor.execute("UPDATE users SET credit = ? WHERE id=?", (newCredit, userid))
        conn.commit()
        conn.close()
        return {
            "credit": newCredit
        }
    except:
        conn.close()
        return {"message": "Error"}

@app.get("/decrease-credit")
async def getPoint(userid: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT credit FROM users WHERE id=?", (userid,))
    credit = cursor.fetchone()[0]


    print("credit: ", credit)

    newCredit = credit - 1

    if(newCredit < 0):
        conn.close()
        raise HTTPException(status_code=400, detail="Not enough credit")
    else:
        try:
            cursor.execute("UPDATE users SET credit = ? WHERE id = ?", (newCredit, userid))
            print(f"UPDATE users SET credit = {newCredit} WHERE id={userid}")
            conn.commit()
            conn.close()
            return {
                "credit": newCredit
            }
        except Exception as e:
            conn.close()
            print("exception", e)
            raise HTTPException(status_code=500, detail="Database error")

    

@app.get("/delete-cv/{userid}")
async def delete_cv(userid: str):
    conn = get_db_connection()
    cursor = conn.cursor()      
    cursor.execute("UPDATE users SET has_cv = 0 WHERE id = ?", (userid,))
    cursor.execute("DELETE FROM cvs  WHERE userid = ?", (userid,))
    conn.commit()
    conn.close()

    try:
        os.remove(f"./static/cvs/{userid}.pdf")
    except:
        pass

    return {"message": "CV deleted successfully"}

@app.get("/delete-jobpost/{userid}")
async def delete_cv(userid: str):
    conn = get_db_connection()
    cursor = conn.cursor()      
    cursor.execute("UPDATE users SET has_jobpost = 0 WHERE id = ?", (userid,))
    cursor.execute("DELETE FROM jobposts  WHERE userid = ?", (userid,))
    conn.commit()
    conn.close()

    try:
        os.remove(f"./static/jobposts/{userid}.txt")
    except:
        pass

    return {"message": "CV deleted successfully"}


@app.get("/admin/create-invite-code")
async def generateInviteCode():
    myuuid = uuid.uuid4()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invitecodes (code) VALUES (?)", (str(myuuid),))
    conn.commit()
    conn.close()
    return {"invite_code": "http://localhost:5173/register/" + str(myuuid)}

@app.get("/check-invite-code/{invite_code}")
async def checkInvideCodeIsValid(invite_code: str):
    print(invite_code)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invitecodes WHERE code = ?", (invite_code,))
    result = cursor.fetchone()
    conn.close()

    if(result == None):
        raise HTTPException(status_code=400, detail="Invite code is not valid")
    else:
        if(result[2] == 1):
            raise HTTPException(status_code=400, detail="Invite code is not valid")
        raise HTTPException(status_code=200, detail="Invite code is valid")


@app.post("/admin/add-courses")
async def add_courses(addCourses: AddCourses):
    conn = get_db_connection()
    cursor = conn.cursor()      
    cursor.execute("INSERT INTO courses (name, keywords, link) VALUES (?, ?, ?)", 
                   (addCourses.name, addCourses.keywords, addCourses.link))
    conn.commit()
    conn.close()
    return {"message": "Course added successfully"}


@app.get("/admin/get-courses")
async def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    result = cursor.fetchall()
    conn.close()
    return {"courses": [list(row) for row in result]}


@app.get("/admin/get-course/{courseid}")
async def get_courses(courseid: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE id=?", (courseid,))
    result = cursor.fetchone()
    conn.close()
    return {"courses": list(result) if result else None}


@app.post("/admin/edit-courses")
async def edit_courses(addCourses: AddCourses):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE courses SET name = ?, keywords = ?, link = ? WHERE id = ?", 
                   (addCourses.name, addCourses.keywords, addCourses.link, addCourses.id))
    conn.commit()
    conn.close()

    return {"courses": addCourses}



@app.get("/admin/delete-course/{courseid}")
async def edit_courses(courseid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = ?", (courseid,))
    conn.commit()
    conn.close()
    return {"courses": True}



@app.get("/admin/stats")
async def get_stats():
    stats = {}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE has_cv = 1")
    result = cursor.fetchone()
    stats['applicantCount'] = int(result[0])
    cursor.execute("SELECT COUNT(*) FROM users WHERE has_jobpost = 1")
    result = cursor.fetchone()
    stats['headHunterCount'] = int(result[0])
    cursor.execute("SELECT COUNT(*) FROM cvs")
    result = cursor.fetchone()
    stats['cvCount'] = int(result[0])
    cursor.execute("SELECT COUNT(*) FROM jobposts")
    result = cursor.fetchone()
    stats['jobPostCount'] = int(result[0])
    conn.close()

    return {"stats": stats}







