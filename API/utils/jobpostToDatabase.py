# from fastapi import FastAPI, File, UploadFile
# from  pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# import hashlib
# import time
# from werkzeug.utils import secure_filename
# import os 
# from helper import allowed_file, handleCV, processJobText, create_point, pdf_to_text
# from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db_connection
import string
import json


def intersectOfTwoLists(list1, list2):
    intersectList = []
    for item in list1:
        if(item in list2):
            intersectList.append(item)
    # for item in list1:
    #     if(binary_search(list2, 0, len(list2)-1, item) != -1):
    #         intersectList.append(item)

    return intersectList




def createSubArray(arr, sub_arr_size):
    sub_arr = []
    for i in range(len(arr)):
        if i + sub_arr_size <= len(arr):
            item = ''
            for j in arr[i:i + sub_arr_size]:
                item += str(str(j) + '-')
            sub_arr.append(item[:-1].replace('-',' '))
    return sub_arr
    

def processJobText(jobText):
    # skills = getSkills()
    processedText = jobText.strip().replace('\n',' ').translate(str.maketrans('', '', string.punctuation)).lower().split()
    # skills = getSkills()
    skills =  [i.lower() for i in ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration', 'Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application','Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship']]

    intersect = []
    for i in range(5):
        intersect += intersectOfTwoLists([x for x in skills if len(x.split()) == i+1],createSubArray(processedText, i+1))

    print(f'intersect : {intersect}')
    print(f'lenght of intersect {len(intersect)}')
    return  intersect
    

def remove_special_characters(text):
    # define the set of special characters and punctuation marks
    special_chars = string.punctuation + '\n\t'

    # create a translation table to remove the special characters
    translator = str.maketrans('', '', special_chars)

    # remove the special characters from the text
    text = text.translate(translator)

    # remove whitespace from the text

    return text


# this function will return error but ignore it. it works 180 job posts. Its enough for now
def jobpostToDatabase():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'older_codes', 'jobposts')
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        return
    
    files = sorted([f for f in os.listdir(path) if f.endswith('.txt')], key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 999999)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for file in files:
        try:
            file_path = os.path.join(path, file)
            with open(file_path, 'r', encoding='iso-8859-1') as f:
                data = remove_special_characters(f.read().strip())
            
            if not data:
                continue
                
            intersect = processJobText(data)
            cursor.execute("INSERT INTO jobposts (jobpost, jobpost_keywords) VALUES (?, ?)", 
                          (data, json.dumps(intersect)))
            print(f"Inserted jobpost from {file}")
        except Exception as e:
            print(f'error processing {file}: {e}')
            continue
    
    conn.commit()
    conn.close()
    print(f"Total {len(files)} jobposts processed.")
           
                    



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


   
if __name__ == "__main__":
    jobpostToDatabase()


