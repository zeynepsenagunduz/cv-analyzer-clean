import json
import os
import codecs


def cross_check():

    # Define the directory containing the files
    directory = "./Datas/"

    all_text = []
    # Loop through each file in the directory
    for i in range(1, 291):
        # Construct the filename
        filename = str(i) + ".txt"
        # Check if the file exists
        if os.path.exists(os.path.join(directory, filename)):
            # Open the file using codecs and remove any non-UTF-8 characters
            with codecs.open(os.path.join(directory, filename), "r", "utf-8", "ignore") as file:
                # Read the contents of the file
                contents = file.read()
                # Do something with the contents of the file
                all_text.append(tuple(contents.strip().lower().split()))


    # skills_list = []

    # with open('skills.txt', 'r') as f:
    #     for line in f:
    #         skills_list.append(line.strip().lower())

    skills_list = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration', 'Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application','Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship']
    for i in skills_list:
        if(len(i) == 3):
            print(i)

    keyword_counts = {}

    list_converted = []
    for i in list(set(all_text)):
        list_converted.append(list(i))

    for count,each_job in enumerate(list_converted):
        print(f"Process {count} of {len(list_converted)}")
        counter = {}
        for each_word_for_job in each_job:
            for each_skill in skills_list:
                each_skill = each_skill.lower()
                if each_word_for_job == each_skill:
                    if each_skill in counter:
                        counter[each_skill] += 1
                    else:
                        counter[each_skill] = 1
        
        keyword_counts[count] = counter


    with open('keyword_counts.json', 'w') as f:
        json.dump(keyword_counts, f)


def find_stats():
    with open('keyword_counts.json', 'r') as f:
        keyword_counts = json.load(f)
    
    keyword_list = []
    for i in range(len(list(keyword_counts.keys()))):
        for j in list(keyword_counts[str(i)].keys()):
            keyword_list.append(j)
    
    # find keyword frequency
    keyword_frequency = {}
    for i in keyword_list:
        if i in keyword_frequency:
            keyword_frequency[i] += 1
        else:
            keyword_frequency[i] = 1
    
    # sort the dictionary by value
    keyword_frequency = {k: v for k, v in sorted(keyword_frequency.items(), key=lambda item: item[1], reverse=True)}
    print(keyword_frequency)

    # write this dictionary to a file
    with open('keyword_frequency.json', 'w') as f:
        json.dump(keyword_frequency, f)

                   




if __name__ == "__main__":
    cross_check()
    find_stats()



