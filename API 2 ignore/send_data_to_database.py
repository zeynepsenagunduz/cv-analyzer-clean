import psycopg2
import requests
from helper import processJobText, pdf_to_text
import codecs
import os 
import json
conn = psycopg2.connect(
    host="103.47.57.28",
    database="tez",
    user="postgres",
    password="kadir123X")



path = "./CV_Example/"


directory = "./CV_Example/"

cv_raws = []
cv_keywords = []
for i in range(10):
    cv_raws.append(pdf_to_text(path+str(i+1)+".pdf"))

for cv_raw in cv_raws:
    cv_keywords.append(processJobText(cv_raw))

cursor = conn.cursor()
for raw,keyword in zip(cv_raws,cv_keywords):
    print("raw",raw)
    print("--------------------------------------------------")
    print("keyword",keyword)
    cursor.execute("INSERT INTO cvs (cv_raw_text,cv_keywords) VALUES (%s,%s)", (raw.replace("\x00", "\uFFFD"),json.dumps(keyword).replace("\x00", "\uFFFD")))
    conn.commit()
    

cursor.close()
    




# read_data_keywords = []
# for count,i in enumerate(all_text):
#     read_data_keywords.append(processJobText(i))
#     print(count)





# cursor = conn.cursor()
# for raw,keyword in zip(all_text,read_data_keywords):
#     print(raw)
#     print("--------------------------------------------------")
#     print(keyword)
#     cursor.execute("INSERT INTO jobposts (jobpost_raw,jobpost_keywords) VALUES (%s,%s)", (raw,json.dumps(keyword)))
#     conn.commit()

# cursor.close()





