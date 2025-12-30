import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db_connection
from config import get_skills  # ✅ Centralized skill list
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
    """
    Extracts skills from job posting text
    
    Args:
        jobText (str): Raw job posting text
    
    Returns:
        list: List of matched skills found in the job posting
    """
    processedText = jobText.strip()\
                          .replace('\n',' ')\
                          .translate(str.maketrans('', '', string.punctuation))\
                          .lower()\
                          .split()
    
    skills = get_skills()  # ✅ Now using centralized skill list from config.py

    intersect = []
    for i in range(5):
        intersect += intersectOfTwoLists(
            [x for x in skills if len(x.split()) == i+1],
            createSubArray(processedText, i+1)
        )

    print(f'intersect : {intersect}')
    print(f'lenght of intersect {len(intersect)}')
    return intersect
    

def remove_special_characters(text):
    # define the set of special characters and punctuation marks
    special_chars = string.punctuation + '\n\t'

    # create a translation table to remove the special characters
    translator = str.maketrans('', '', special_chars)

    # remove the special characters from the text
    text = text.translate(translator)

    # remove whitespace from the text

    return text


def jobpostToDatabase():
    """
    Processes job posting text files and stores them in database
    Extracts skills from each job posting
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'older_codes', 'jobposts')
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        return
    
    files = sorted([f for f in os.listdir(path) if f.endswith('.txt')], 
                   key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 999999)
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
    """
    Recommends courses based on missing skills
    
    Args:
        jobKeywords (list): Skills required in job posting
        cvKeywords (list): Skills found in user's CV
    
    Returns:
        list: Recommended courses for missing skills, or None if no missing skills
    """
    courses = []
    notMatchingKeywords = []
    
    # Find skills that are in job but not in CV
    for keyword in jobKeywords:
        if keyword not in cvKeywords:
            notMatchingKeywords.append(keyword)
    
    if len(notMatchingKeywords) == 0:
        return None
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find courses that match missing skills
        for i in notMatchingKeywords:
            cursor.execute("SELECT * FROM courses WHERE keywords LIKE ?", (f'%{i}%',))
            result = cursor.fetchall()
            if result != None:
                for course in result:
                    courses.append(list(course))
        conn.close()

    return courses

   
if __name__ == "__main__":
    jobpostToDatabase()
