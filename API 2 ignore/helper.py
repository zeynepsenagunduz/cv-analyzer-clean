import PyPDF2
import string
import os

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

def pdf_to_text():
    pdf_reader = PyPDF2.PdfReader(open("./temp/kadir", 'rb'))
    all_text = []
    for page in pdf_reader.pages:
        all_text.append(page.extract_text().strip().lower())
    return ' '.join(all_text)


def extractPdf(filePath):
    pdfFileObj = open(f'./static/files/{filePath}', 'rb')
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
    SKILLSPATH = './skills.txt'
    with open(SKILLSPATH, 'r') as f:
        skills = [x.lower().translate(str.maketrans('', '', string.punctuation)) for x in f.read().splitlines()]
    return skills

def createSubArray(arr, sub_arr_size):
    sub_arr = []
    for i in range(len(arr)):
        if i + sub_arr_size <= len(arr):
            item = ''
            for j in arr[i:i + sub_arr_size]:
                item += str(str(j) + '-')
            sub_arr.append(item[:-1].replace('-',' '))
    return sub_arr
    


def handleCV(filename):
    allTextList = extractPdf(filename)
    skills = getSkills()
    # oneWordSkills = [x for x in skills if len(x.split()) == 1]
    # twoWordSkills = [x for x in skills if len(x.split()) == 2]
    # threeWordSkills = [x for x in skills if len(x.split()) == 3]
    # fourWordSkills = [x for x in skills if len(x.split()) == 4]
    # fiveWordSkills = [x for x in skills if len(x.split()) == 5]

    # oneWordTextList = createSubArray(allTextList, 1)
    # twoWordTextList = createSubArray(allTextList, 2)
    # threeWordTextList = createSubArray(allTextList, 3)
    # fourWordTextList = createSubArray(allTextList, 4)
    # fiveWordTextList = createSubArray(allTextList, 5)


    # #write threeWordTextList to txt file 
    # with open('./threeWordTextList.txt', 'w') as f:
    #     for item in threeWordTextList:
    #         f.write("%s \n" % item)
    
    # #write threeWordSkills to txt file
    # with open('./threeWordSkills.txt', 'w') as f:
    #     for item in threeWordSkills:
    #         f.write("%s \n" % item)

    intersect = []
    for i in range(5):
        intersect += intersectOfTwoLists([x for x in skills if len(x.split()) == i+1],createSubArray(allTextList, i+1))

    print(f'intersect : {intersect}')
    print(f'lenght of intersect {len(intersect)}')
    return  intersect





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
    


def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_point(cv_keywords,jobpost_keywords):
    if(len(jobpost_keywords) == 0):
        return 0
    return (len(set(cv_keywords).intersection(jobpost_keywords)) / len(jobpost_keywords)) * 100




# if __name__ == "__main__":
#     print(getSkills())





