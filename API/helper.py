import PyPDF2
import string
import os
from config import get_skills  # ✅ Centralized skill list


def normalize_text_for_skills(text):
    """
    Normalizes text while preserving special skill formats like Node.js, C++, C#
    
    Args:
        text (str): Raw text to normalize
    
    Returns:
        list: List of normalized words
    
    Example:
        >>> normalize_text_for_skills("I know Node.js and C++")
        ['i', 'know', 'nodejs', 'and', 'cplusplus']
    """
    # Step 1: Convert to lowercase
    text = text.lower()
    
    # Step 2: Replace special skill patterns BEFORE removing punctuation
    # This preserves skills like "Node.js" → "nodejs", "C++" → "cplusplus"
    replacements = {
        'node.js': ' nodejs ',
        'vue.js': ' vuejs ',
        'next.js': ' nextjs ',
        'express.js': ' expressjs ',
        'react.js': ' reactjs ',
        'angular.js': ' angularjs ',
        'c++': ' cplusplus ',
        'c#': ' csharp ',
        '.net': ' dotnet ',
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    # Step 3: Remove newlines
    text = text.replace('\n', ' ')
    
    # Step 4: NOW remove punctuation (special skills are already protected)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Step 5: Split into words and return
    return text.split()


def expand_with_synonyms(skills_list):
    """
    Expands a skill list by adding their main skill equivalents from synonyms
    
    Args:
        skills_list (list): List of normalized skills (e.g., ['nodejs', 'cplusplus'])
    
    Returns:
        list: Expanded list with main skills (e.g., ['nodejs', 'node.js', 'cplusplus', 'c++'])
    
    Example:
        >>> expand_with_synonyms(['nodejs', 'cplusplus'])
        ['nodejs', 'node.js', 'cplusplus', 'c++']
    """
    from config import SKILL_SYNONYMS
    
    expanded = list(skills_list)  # Copy original list
    
    # For each skill in the list
    for skill in skills_list:
        # Check each main skill and its synonyms
        for main_skill, synonyms in SKILL_SYNONYMS.items():
            # If current skill is a synonym of main_skill
            if skill in synonyms:
                # Add the main skill to the list
                if main_skill not in expanded:
                    expanded.append(main_skill)
            # If current skill IS the main skill
            elif skill == main_skill:
                # Add all synonyms
                for syn in synonyms:
                    if syn not in expanded:
                        expanded.append(syn)
    
    return expanded


def binary_search(arr, low, high, x):

    if high >= low:

        mid = (high + low) // 2

        if arr[mid].strip() == x.strip():
            return mid

        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        return -1


def intersectOfTwoLists(list1, list2):
    intersectList = []
    for item in list1:
        if(item in list2):
            intersectList.append(item)
    # for item in list1:
    #     if(binary_search(list2, 0, len(list2)-1, item) != -1):
    #         intersectList.append(item)

    return intersectList


def pdf_to_text(id):
    id = int(id)
    pdf_reader = PyPDF2.PdfReader(open(f"./static/cvs/{id}.pdf", 'rb'))
    all_text = []
    for page in pdf_reader.pages:
        all_text.append(page.extract_text().strip().lower())
    return ' '.join(all_text)


def extractPdf(filePath):
    pdfFileObj = open(f'./static/cvs/{filePath}', 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    allChunks = []
    allTextList = []

    for i in range(len(pdfReader.pages)):

        pageObj = pdfReader.pages[i]
        rawText = pageObj.extract_text().strip().replace('\n',' ').translate(str.maketrans('', '', string.punctuation)).lower().split()

        allTextList += rawText 

    pdfFileObj.close() 
    allChunks =  allTextList
    # [allChunks.append(allTextList[i:i+2]) for i in range(0, len(allTextList), 2)] 
    for i in range(0, len(allTextList), 2):
        # allChunks.append(allTextList[i:i+2])
        for k in allTextList[i:i+2]:
            allChunks.append(k)
    # [allChunks.append(allTextList[i:i+3]) for i in range(0, len(allTextList), 3)]
    for i in range(0, len(allTextList), 3):
        # allChunks.append(allTextList[i:i+3])
        for k in allTextList[i:i+3]:
            allChunks.append(k)
    # [allChunks.append(allTextList[i:i+4]) for i in range(0, len(allTextList), 4)]
    for i in range(0, len(allTextList), 4):
        # allChunks.append(allTextList[i:i+4])
        for k in allTextList[i:i+4]:
            allChunks.append(k)
    # [allChunks.append(allTextList[i:i+5]) for i in range(0, len(allTextList), 5)]
    for i in range(0, len(allTextList), 5):
        # allChunks.append(allTextList[i:i+5])
        for k in allTextList[i:i+5]:
            allChunks.append(k)

    return allChunks


def getSkills():
    """
    DEPRECATED: Use get_skills() from config.py instead
    This function is kept for backward compatibility
    """
    return get_skills()


def createSubArray(arr, sub_arr_size):
    sub_arr = []
    for i in range(len(arr)):
        if i + sub_arr_size <= len(arr):
            item = ''
            for j in arr[i:i + sub_arr_size]:
                item += str(str(j) + '-')
            sub_arr.append(item[:-1].replace('-',' '))
    return sub_arr
    

def remove_special_characters(text):
    # define the set of special characters and punctuation marks
    special_chars = string.punctuation + '\n\t'

    # create a translation table to remove the special characters
    translator = str.maketrans('', '', special_chars)

    # remove the special characters from the text
    text = text.translate(translator)

    # remove whitespace from the text

    return text




def handleCV(filename):
    """
    Extracts skills from a CV PDF file with improved skill detection
    
    Args:
        filename (str): Name of the PDF file in ./static/cvs/
    
    Returns:
        list: List of matched skills found in the CV
    """
    # Extract text from PDF (old method for compatibility)
    allTextList = extractPdf(filename)
    
    # Convert to string and normalize with special skill protection
    text = ' '.join(allTextList)
    processedText = normalize_text_for_skills(text)
    
    # Expand with synonyms for better matching
    expandedText = expand_with_synonyms(processedText)
    
    skills = get_skills()  # ✅ Using centralized skill list from config.py
   
    intersect = []
    for i in range(5):
        intersect += intersectOfTwoLists(
            [x for x in skills if len(x.split()) == i+1],
            createSubArray(expandedText, i+1)
        )

    print(f'intersect : {intersect}')
    print(f'lenght of intersect {len(intersect)}')
    return intersect



def processJobText(jobText):
    """
    Extracts skills from a job posting text with improved skill detection
    
    Args:
        jobText (str): Raw job posting text
    
    Returns:
        list: List of matched skills found in the job posting
    
    Example:
        >>> processJobText("We need React, Node.js, and Docker experience")
        ['react', 'node.js', 'docker']
    """
    # Use new normalize function that protects special skills
    processedText = normalize_text_for_skills(jobText)
    
    # Expand with synonyms for better matching
    expandedText = expand_with_synonyms(processedText)
    
    skills = get_skills()  # ✅ Using centralized skill list from config.py

    intersect = []
    for i in range(5):
        intersect += intersectOfTwoLists(
            [x for x in skills if len(x.split()) == i+1],
            createSubArray(expandedText, i+1)
        )

    print(f'intersect : {intersect}')
    print(f'lenght of intersect {len(intersect)}')
    return intersect



def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_point(cv_keywords, jobpost_keywords):
    """
    Calculates matching percentage between CV and job posting
    
    Args:
        cv_keywords (list): Skills found in CV
        jobpost_keywords (list): Skills found in job posting
    
    Returns:
        float: Matching percentage (0-100)
    """
    if(len(jobpost_keywords) <= 4):
        return 0
    return (len(set(cv_keywords).intersection(jobpost_keywords)) / len(jobpost_keywords)) * 100


# if __name__ == "__main__":
#     print(getSkills())