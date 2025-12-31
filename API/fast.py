from fastapi import FastAPI, File, UploadFile,HTTPException, Query
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from helper import allowed_file, handleCV, processJobText, create_point, pdf_to_text,remove_special_characters
from fastapi.middleware.cors import CORSMiddleware
from db import get_db_connection
from collections import Counter
import json
import os 
import uuid
import ast
from rank_bm25 import BM25Okapi
from fastapi.responses import FileResponse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def safe_keywords(raw):
    """
    DB'den gelen keywords alanını güvenle listeye çevirir.
    Kabul ettikleri:
      - JSON: '["html","css"]'
      - boş/None: '' / None
      - python list string: "['html','css']"  (fallback)
      - düz metin: 'html css react' (fallback)
    """
    if raw is None:
        return []
    s = str(raw).strip()
    if not s:
        return []

    # 1) JSON dene
    try:
        data = json.loads(s)
        if isinstance(data, list):
            return [str(x).strip().lower() for x in data if str(x).strip()]
    except Exception:
        pass

    # 2) Python list string (tek tırnaklı) dene
    try:
        data = ast.literal_eval(s)
        if isinstance(data, list):
            return [str(x).strip().lower() for x in data if str(x).strip()]
    except Exception:
        pass

    # 3) düz metin fallback
    return [w for w in remove_special_characters(s).lower().split() if w]



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
    
"""""
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

"""
@app.post("/best-job")
async def getPoint(userid: BestJobs):
    cv_keywords = processJobText(pdf_to_text(userid.userid))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, jobpost, jobpost_keywords,userid FROM jobposts")
    jobs = cursor.fetchall()

    if not jobs:
        conn.close()
        return {"top_five": [], "cv_keywords": cv_keywords, "best_job_keywords": [], "courses": []}

    scores = {}
    job_kw_map = {}   # id -> keywords list
    job_text_map = {} # id -> jobpost text
    job_user_map = {}  # id -> userid


    for job in jobs:
        job_id = job[0]
        job_text = job[1]
        raw_kw = job[2]
        jobposts_userid = job[3]   # ✅ jobposts.userid


        kw_list = safe_keywords(raw_kw)   # ✅ burada patlamaz
        job_kw_map[job_id] = kw_list
        job_text_map[job_id] = job_text
        job_user_map[job_id] = jobposts_userid  # ✅


        scores[job_id] = create_point(cv_keywords, kw_list)

    # skora göre sırala
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # en iyi job keywords
    best_job_id = sorted_scores[0][0]
    best_job_keywords = job_kw_map.get(best_job_id, [])

    # top 5 response
    top5 = sorted_scores[:5]
    new_list = []
    for job_id, point in top5:
        new_list.append({
            "id": job_id,
            "userid": job_user_map.get(job_id),  #  dosya adı
            "text": job_text_map.get(job_id, ""),
            "keywords": job_kw_map.get(job_id, []),
            "point": int(point)
        })

    conn.close()

    courses = recommenderFunction(best_job_keywords, cv_keywords)

    return {
        "top_five": new_list,
        "cv_keywords": cv_keywords,
        "best_job_keywords": best_job_keywords,
        "courses": courses
    }


# ============================================================
# BM25 RANKING ALGORITHM
# ============================================================

# ============================================================
# BM25 RANKING ALGORITHM
# ============================================================

def bm25_matching(all_cv_texts, job_keywords_text):
    """
    BM25 Okapi algoritması ile CV-Job matching
    
    BM25 avantajları:
    - Frekans doygunluğu (aynı kelime 100 kere tekrar ederse fazla puan vermiyor)
    - Uzunluk normalizasyonu (uzun dokümanlar avantajlı değil)
    - TF-IDF'ten daha dengeli skorlar
    
    Args:
        all_cv_texts: Tüm CV keyword metinleri (list of strings)
        job_keywords_text: Job post keyword metni (string)
    
    Returns:
        dict: {cv_index: score} (0-100 arası)
    """
    try:
        # DEBUG
        print(f"DEBUG BM25 - CV sayısı: {len(all_cv_texts)}")
        print(f"DEBUG BM25 - Job text: {job_keywords_text[:100]}")
        
        # Boş kontrol
        if not all_cv_texts or not job_keywords_text:
            print("DEBUG BM25 - Boş input!")
            return {}
        
        # Tokenize (kelimelere ayır)
        tokenized_corpus = []
        for cv_text in all_cv_texts:
            tokens = cv_text.lower().split()
            tokenized_corpus.append(tokens)
        
        print(f"DEBUG BM25 - İlk CV tokens: {tokenized_corpus[0][:10] if tokenized_corpus else 'BOŞ'}")
        
        tokenized_query = job_keywords_text.lower().split()
        print(f"DEBUG BM25 - Job tokens: {tokenized_query[:10]}")
        
        # BM25 modeli oluştur (k1=1.5, b=0.75 - standart değerler)
        bm25 = BM25Okapi(tokenized_corpus, k1=1.5, b=0.75)
        
        # Her CV için BM25 skoru hesapla
        raw_scores = bm25.get_scores(tokenized_query)
        print(f"DEBUG BM25 - Raw scores (ilk 5): {raw_scores[:5] if len(raw_scores) > 0 else 'BOŞ'}")
        print(f"DEBUG BM25 - Max raw score: {max(raw_scores) if len(raw_scores) > 0 else 0}")
        
        # Skorları normalize et (0-100 arası)
        scores = {}
        max_score = max(raw_scores) if len(raw_scores) > 0 and max(raw_scores) > 0 else 1
        
        for i, raw_score in enumerate(raw_scores):
            # Normalize
            normalized = (raw_score / max_score) * 100
            
            # Sınırla (0-100)
            normalized = max(0.0, min(100.0, normalized))
            
            scores[i] = round(normalized, 2)
        
        print(f"DEBUG BM25 - Final scores (ilk 5): {list(scores.items())[:5]}")
        
        return scores
        
    except Exception as e:
        print(f"BM25 error: {e}")
        import traceback
        traceback.print_exc()
        return {}


@app.post("/best-applicant")
async def best_applicant(userid: str = Query(...)):
    print("=" * 50)
    print("ENDPOINT ÇAĞRILDI!")
    print(f"userid: {userid}")
    print("=" * 50)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Job post'u al
    cursor.execute("SELECT jobpost FROM jobposts WHERE userid = ?", (userid,))
    jobpost_row = cursor.fetchone()
    
    if not jobpost_row:
        conn.close()
        return {"top_five": [], "best_cv_keywords": [], "message": "Job post bulunamadı"}
    
    jobpost_text = jobpost_row[0]
    job_keywords = processJobText(jobpost_text)
    job_keywords_text = " ".join(job_keywords)
    
    # Tüm CV'leri al
    cursor.execute("SELECT id, userid, keywords FROM cvs")
    cvs = cursor.fetchall()
    
    # Kullanıcı bilgilerini al
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    user_map = {str(u[0]): {"username": u[1], "email": u[2]} for u in users}
    
    # ═══════════════════════════════════════════════════════
    # YENİ: BM25 RANKING ALGORITHM
    # ═══════════════════════════════════════════════════════
    
    # Tüm CV keyword metinlerini hazırla
    all_cv_texts = []
    cv_index_to_userid = {}
    
    for i, row in enumerate(cvs):
        cv_id = row[0]
        cv_userid = row[1]
        raw_kw = row[2]
        
        # CV keywords'ü text'e çevir
        cv_keywords_text = raw_kw.replace(",", " ").replace(";", " ")
        cv_keywords_text = cv_keywords_text.replace('"', '').replace('[', '').replace(']', '')
        cv_keywords_text = cv_keywords_text.strip()
        all_cv_texts.append(cv_keywords_text)
        cv_index_to_userid[i] = cv_userid
    
    # BM25 ile skorla
    index_scores = bm25_matching(all_cv_texts, job_keywords_text)
    
    # Index'leri userid'lere çevir
    scores = {}
    for index, score in index_scores.items():
        userid_item = cv_index_to_userid.get(index)
        if userid_item:
            scores[userid_item] = score
    
    # ═══════════════════════════════════════════════════════
    
    # Skorlara göre sırala
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top5 = sorted_scores[:5]
    
    # Sonuç listesi oluştur
    new_list = []
    for userid_item, point in top5:
        user_info = user_map.get(str(userid_item), {"username": "Unknown", "email": "N/A"})
        new_list.append({
            "userid": userid_item,
            "username": user_info["username"],
            "email": user_info["email"],
            "point": int(point)
        })
    
    # En iyi CV'nin keywords'ünü al
    best_cv_keywords = []
    if top5:
        best_userid = top5[0][0]
        cursor.execute("SELECT keywords FROM cvs WHERE userid = ?", (best_userid,))
        best_cv_row = cursor.fetchone()
        if best_cv_row:
            try:
                from helper import safe_keywords
                best_cv_keywords = safe_keywords(best_cv_row[0])
            except:
                best_cv_keywords = best_cv_row[0].split(",")
    
    conn.close()
    
    return {
        "top_five": new_list,
        "best_cv_keywords": best_cv_keywords
    }
  

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


@app.get("/api/analytics/overview")
def get_analytics_overview():
    """
    Genel sistem istatistikleri
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Toplam CV sayısı
    cursor.execute("SELECT COUNT(*) FROM cvs")
    total_cvs = cursor.fetchone()[0]
    
    # Toplam job posting sayısı
    cursor.execute("SELECT COUNT(*) FROM jobposts")
    total_jobs = cursor.fetchone()[0]
    
    # En popüler skill'ler (CV'lerde en çok geçen)
    cursor.execute("""
        SELECT keywords FROM cvs WHERE keywords IS NOT NULL AND keywords != '[]'
    """)
    all_cv_skills = []
    for row in cursor.fetchall():
        try:
            skills = json.loads(row[0])
            all_cv_skills.extend(skills)
        except:
            pass
    
    skill_counts = Counter(all_cv_skills)
    top_skills = skill_counts.most_common(20)
    
    conn.close()
    
    return {
        "total_cvs": total_cvs,
        "total_jobs": total_jobs,
        "total_matches": 0,
        "avg_match_score": 0,
        "top_skills": [{"skill": s[0], "count": s[1]} for s in top_skills]
    }


@app.get("/api/analytics/skill-trends")
def get_skill_trends():
    """
    Skill trendleri - hangi skill'ler en çok aranıyor
    """
    from config import get_skills_by_category
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Job posting'lerde en çok aranan skill'ler
    cursor.execute("""
        SELECT jobpost_keywords FROM jobposts 
        WHERE jobpost_keywords IS NOT NULL AND jobpost_keywords != '[]'
    """)
    
    all_job_skills = []
    for row in cursor.fetchall():
        try:
            skills = json.loads(row[0])
            all_job_skills.extend(skills)
        except:
            pass
    
    skill_counts = Counter(all_job_skills)
    
    # En çok aranan 30 skill
    trending = skill_counts.most_common(30)
    
    # Kategorize et
    def categorize_skill(skill):
        categories = get_skills_by_category()
        for category, skills in categories.items():
            if skill.lower() in [s.lower() for s in skills]:
                return category
        return "other"
    
    conn.close()
    
    return {
        "trending_skills": [
            {
                "skill": s[0],
                "demand": s[1],
                "category": categorize_skill(s[0])
            } 
            for s in trending
        ]
    }

@app.get("/api/user/profile/{userid}")
def get_user_profile(userid: str):
    """
    Kullanıcı profil bilgileri ve öneriler
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kullanıcı bilgileri
    cursor.execute("SELECT username, email, role, has_cv FROM users WHERE id = ?", (userid,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {
        "username": user[0],
        "email": user[1],
        "role": user[2],
        "has_cv": user[3]
    }
    
    # Kullanıcının skill'leri
    user_skills = []
    if user[3]:  # has_cv
        cursor.execute("SELECT keywords FROM cvs WHERE userid = ?", (userid,))
        cv = cursor.fetchone()
        if cv and cv[0]:
            user_skills = json.loads(cv[0])
    
    # En çok aranan skill'ler (job postings'ten)
    cursor.execute("""
        SELECT jobpost_keywords FROM jobposts 
        WHERE jobpost_keywords IS NOT NULL AND jobpost_keywords != '[]'
    """)
    
    all_job_skills = []
    for row in cursor.fetchall():
        try:
            skills = json.loads(row[0])
            all_job_skills.extend(skills)
        except:
            pass
    
    skill_counts = Counter(all_job_skills)
    
    # Kullanıcıda OLMAYAN ama çok aranan skill'ler
    recommended_skills = []
    for skill, count in skill_counts.most_common(50):
        if skill not in user_skills:
            recommended_skills.append({
                "skill": skill,
                "demand": count
            })
        if len(recommended_skills) >= 5:
            break
    
    # Kullanıcının skill istatistikleri
    total_user_skills = len(user_skills)
    total_job_skills = len(set(all_job_skills))
    
    # Coverage hesapla
    user_skills_in_demand = [s for s in user_skills if s in all_job_skills]
    coverage = (len(user_skills_in_demand) / total_user_skills * 100) if total_user_skills > 0 else 0
    
    # Her skill için demand bilgisi ekle (YENİ!)
    skills_with_demand = []
    for skill in user_skills:
        skills_with_demand.append({
            "skill": skill,
            "in_demand": skill in all_job_skills,
            "demand_count": skill_counts.get(skill, 0)
        })
    
    conn.close()
    
    return {
        "user": user_data,
        "skills": user_skills,
        "skills_with_demand": skills_with_demand,  # YENİ!
        "skill_count": total_user_skills,
        "skills_in_demand": len(user_skills_in_demand),
        "market_coverage": round(coverage, 1),
        "recommended_skills": recommended_skills
    }

# ============================================================
# CV FILE ENDPOINT
# ============================================================

@app.get("/api/user/cv/{userid}")
def get_user_cv(userid: str):
    """
    Kullanıcının yüklediği CV PDF dosyasını döndür
    """
    cv_path = f"static/cvs/{userid}.pdf"  # ← DÜZELT
    
    if not os.path.exists(cv_path):
        raise HTTPException(status_code=404, detail="CV dosyası bulunamadı")
    
    return FileResponse(
        path=cv_path,
        media_type="application/pdf",
        filename=f"cv_{userid}.pdf"
    )


# ============================================================
# APPLICATION ENDPOINTS
# ============================================================



@app.post("/api/apply")
def apply_to_job(userid: str, jobpostid: int, cover_letter: str = ""):
    """
    İş ilanına başvuru yap
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Daha önce başvuru yapılmış mı kontrol et
    cursor.execute("""
        SELECT id FROM applications 
        WHERE userid = ? AND jobpostid = ?
    """, (userid, jobpostid))
    
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu iş ilanına zaten başvurdunuz")
    
    # Matching score hesapla
    # Kullanıcının CV'si
    cursor.execute("SELECT keywords FROM cvs WHERE userid = ?", (userid,))
    cv_row = cursor.fetchone()
    user_skills = json.loads(cv_row[0]) if cv_row and cv_row[0] else []
    
    # Job post'un gereksinimleri
    cursor.execute("SELECT jobpost_keywords FROM jobposts WHERE id = ?", (jobpostid,))
    job_row = cursor.fetchone()
    job_skills = json.loads(job_row[0]) if job_row and job_row[0] else []
    
    # Matching score hesapla (basit yöntem)
    if len(job_skills) == 0:
        match_score = 0
    else:
        matched_skills = set(user_skills) & set(job_skills)
        match_score = (len(matched_skills) / len(job_skills)) * 100
    
    # Başvuruyu kaydet
    cursor.execute("""
        INSERT INTO applications (userid, jobpostid, match_score, cover_letter)
        VALUES (?, ?, ?, ?)
    """, (userid, jobpostid, round(match_score, 2), cover_letter))
    
    conn.commit()
    application_id = cursor.lastrowid
    conn.close()
    
    return {
        "success": True,
        "application_id": application_id,
        "match_score": round(match_score, 2),
        "message": "Başvurunuz başarıyla kaydedildi!"
    }


@app.get("/api/applications/user/{userid}")
def get_user_applications(userid: str):
    """
    Kullanıcının yaptığı tüm başvuruları getir
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.id,
            a.jobpostid,
            a.applied_at,
            a.status,
            a.match_score,
            j.userid
        FROM applications a
        JOIN jobposts j ON a.jobpostid = j.id
        WHERE a.userid = ?
        ORDER BY a.applied_at DESC
    """, (userid,))
    
    applications = []
    for row in cursor.fetchall():
        applications.append({
            "id": row[0],
            "jobpostid": row[1],
            "applied_at": row[2],
            "status": row[3],
            "match_score": row[4],
            "job_userid": row[5]
        })
    
    conn.close()
    return {"applications": applications}


@app.get("/api/applications/job/{jobpostid}")
def get_job_applications(jobpostid: int):
    """
    Bir iş ilanına gelen başvuruları getir (HeadHunter için)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.id,
            a.userid,
            a.applied_at,
            a.status,
            a.match_score,
            a.cover_letter,
            u.username,
            u.email
        FROM applications a
        JOIN users u ON a.userid = u.id
        WHERE a.jobpostid = ?
        ORDER BY a.match_score DESC, a.applied_at DESC
    """, (jobpostid,))
    
    applications = []
    for row in cursor.fetchall():
        applications.append({
            "id": row[0],
            "userid": row[1],
            "applied_at": row[2],
            "status": row[3],
            "match_score": row[4],
            "cover_letter": row[5],
            "username": row[6],
            "email": row[7]
        })
    
    conn.close()
    return {"applications": applications}


@app.put("/api/applications/{application_id}/status")
def update_application_status(application_id: int, status: str):
    """
    Başvuru durumunu güncelle (HeadHunter için)
    status: pending, viewed, accepted, rejected
    """
    valid_statuses = ["pending", "viewed", "accepted", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Geçersiz durum")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE applications 
        SET status = ?
        WHERE id = ?
    """, (status, application_id))
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Başvuru durumu güncellendi"}

# ============================================================
# HEADHUNTER PROFILE ENDPOINT
# ============================================================

@app.get("/api/headhunter/profile/{userid}")
def get_headhunter_profile(userid: str):
    """
    HeadHunter profil bilgileri
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kullanıcı bilgileri
    cursor.execute("SELECT username, email, has_jobpost FROM users WHERE id = ?", (userid,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    conn.close()
    
    return {
        "username": user[0],
        "email": user[1],
        "has_jobpost": user[2]
    }

# ============================================================
# HEADHUNTER APPLICATIONS PAGE ENDPOINT
# ============================================================

@app.get("/api/headhunter/applications/{userid}")
def get_headhunter_applications(userid: str):
    """
    HeadHunter'ın iş ilanına gelen başvurular + algoritma önerileri
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. HeadHunter'ın job post id'sini bul
    cursor.execute("SELECT id FROM jobposts WHERE userid = ?", (userid,))
    jobpost = cursor.fetchone()
    
    if not jobpost:
        conn.close()
        return {
            "top_five": [],
            "applications": [],
            "message": "Henüz iş ilanı yüklenmemiş"
        }
    
    jobpost_id = jobpost[0]
    
    # 2. En iyi 5 adayı al (algoritma önerisi - /best-applicant'tan)
    # Job post'un keyword'lerini al
    cursor.execute("SELECT jobpost FROM jobposts WHERE id = ?", (jobpost_id,))
    jobtext_row = cursor.fetchone()
    
    if not jobtext_row:
        conn.close()
        return {"top_five": [], "applications": []}
    
    jobtext = jobtext_row[0]
    job_keywords = processJobText(jobtext)
    
    # CV'leri al ve skorla
    cursor.execute("SELECT id, userid, keywords FROM cvs")
    cvs = cursor.fetchall()
    
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    user_map = {str(u[0]): {"username": u[1], "email": u[2]} for u in users}
    
    scores = {}
    for row in cvs:
        cv_userid = row[1]
        raw_kw = row[2]
        kw_list = safe_keywords(raw_kw)
        scores[cv_userid] = create_point(kw_list, job_keywords)
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top5 = sorted_scores[:5]
    
    # 3. Bu iş ilanına yapılan başvuruları al
    cursor.execute("""
        SELECT 
            a.userid,
            a.applied_at,
            a.match_score
        FROM applications a
        WHERE a.jobpostid = ?
        ORDER BY a.applied_at DESC
    """, (jobpost_id,))
    
    applications_raw = cursor.fetchall()
    application_userids = set([str(app[0]) for app in applications_raw])
    
    # 4. Top 5'i formatla (başvuru durumu ile)
    top_five_list = []
    for u, p in top5:
        user_info = user_map.get(str(u), {"username": "Unknown", "email": "N/A"})
        has_applied = str(u) in application_userids
        top_five_list.append({
            "userid": u,
            "username": user_info["username"],
            "email": user_info["email"],
            "point": int(p),
            "has_applied": has_applied
        })
    
    # 5. Tüm başvuruları formatla
    applications_list = []
    for app in applications_raw:
        user_info = user_map.get(str(app[0]), {"username": "Unknown", "email": "N/A"})
        applications_list.append({
            "userid": app[0],
            "username": user_info["username"],
            "email": user_info["email"],
            "applied_at": app[1],
            "match_score": app[2]
        })
    
    conn.close()
    
    return {
        "top_five": top_five_list,
        "applications": applications_list
    }