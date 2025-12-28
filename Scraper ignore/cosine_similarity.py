import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os 
import codecs


def calc_cosine_similarity():
    resumes = []

    for count in range(1,6):
        with open(f"./example_resumes/res-{count}.txt", "r") as f:
            words = re.sub(r'[^\w\s]', ' ', re.sub('\n',' ', f.read().lower().strip()))
            resumes.append(words)

    job_post = []
    # Loop through each file in the directory
   
    # Construct the filename
    filename = "./Datas/6.txt"
    # Check if the file exists
    if os.path.exists(os.path.join(filename)):
        # Open the file using codecs and remove any non-UTF-8 characters
        with codecs.open(os.path.join(filename), "r", "utf-8", "ignore") as file:
            # Read the contents of the file
            contents = file.read()
            # Do something with the contents of the file
            job_post = contents.lower().strip()

            job_post = re.sub(r'[^\w\s]', ' ', job_post)
    
    all_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration', 'Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application','Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship']
    # Create a CountVectorizer to convert the resumes and job post to vectors of word frequencies
    vectorizer = CountVectorizer(vocabulary=all_skills)

    # Convert the resumes and job post to vectors
    resume_vectors = vectorizer.fit_transform(resumes)
    job_post_vector = vectorizer.fit_transform([job_post])

    # Compute the cosine similarity between each resume and the job post
    similarity_scores = cosine_similarity(resume_vectors, job_post_vector)


    # Define the score range
    min_score = 1
    max_score = 100

    # Assign a numerical score to each pair based on the similarity score
    score_range = max_score - min_score
    scores = []
    for i in range(len(resumes)):
        score = int(min_score + similarity_scores[i][0] * score_range)
        scores.append(score)
    
    print(scores)


    


if __name__ == "__main__":
    calc_cosine_similarity()