import networkx as nx

# def rank_keywords(cvs, keywords, top_n=10):
#     # Create a directed graph
#     G = nx.DiGraph()

#     # Add each keyword as a node
#     for kw in keywords:
#         G.add_node(kw)

#     # Add edges between keywords that appear in the same CV
#     for cv in cvs:
#         for kw1 in keywords:
#             if kw1 in cv:
#                 for kw2 in keywords:
#                     if kw1 != kw2 and kw2 in cv:
#                         G.add_edge(kw1, kw2)

#     # Calculate the PageRank score for each keyword
#     scores = nx.pagerank(G)

#     # Sort the keywords by their PageRank score and return the top N
#     top_keywords = sorted(scores, key=scores.get, reverse=True)[:top_n]

#     return top_keywords


def rank_keywords(cvs, keywords, top_n=10):
    # Create a directed graph with weighted edges
    G = nx.DiGraph()

    for kw in keywords:
        G.add_node(kw)

    for cv in cvs:
        for kw1 in keywords:
            if kw1 in cv:
                for kw2 in keywords:
                    if kw1 != kw2 and kw2 in cv:
                        # Increment edge weight for keyword pair
                        if G.has_edge(kw1, kw2):
                            G[kw1][kw2]["weight"] += 1
                        else:
                            G.add_edge(kw1, kw2, weight=1)

    # Calculate the PageRank score for each keyword
    scores = nx.pagerank(G, weight="weight")

    # Sort the keywords by their PageRank score and return the top N
    top_keywords = sorted(scores, key=scores.get, reverse=True)[:top_n]

    return top_keywords


# cvs = ["I have experience in HTML and CSS.", "I am proficient in JavaScript and React."]
# keywords = ["HTML", "CSS", "JavaScript", "React"]

cvs = []

for count in range(1,6):
    with open(f"./example_resumes/res-{count}.txt", "r") as f:
        words = []
        for word in list(f.read().strip().split()):
            words.append(word.lower())

        cvs.append(words)

keywords = ['Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application','Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship', 'HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration']

top_keywords = rank_keywords(cvs, keywords, top_n=5)
print(top_keywords)

# result should like this
# ['React', 'JavaScript', 'HTML']

# Top_n icin agirliklandirma nasil olacak ? 
# cv ile is postu arasindaki agirliklandirma yapildi. 

# haftaya kadar frekans bazli agirliklandirma ile page_rank algoritmasini gercek datalar ile karsilastir
# sonrasinda hangi algoritma ile ilerlemek istedigine karar ver. 




# hard_skills = ['HTML5', 'CSS3', 'JavaScript', 'TypeScript', 'React', 'Vue.js', 'Angular', 'jQuery', 'Bootstrap', 'Sass', 'LESS', 'Webpack', 'Gulp', 'Grunt', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'React Native', 'Ionic', 'Flutter', 'NativeScript', 'Electron', 'Three.js', 'D3.js', 'Chart.js', 'Highcharts', 'Figma', 'Sketch', 'Photoshop', 'Illustrator', 'Zeplin', 'InVision', 'Webflow', 'WordPress', 'Shopify', 'Magento', 'WooCommerce', 'BigCommerce', 'PrestaShop', 'Drupal', 'Joomla', 'Gatsby', 'Next.js', 'Nuxt.js', 'Express.js', 'Koa.js', 'Meteor', 'Nginx', 'Apache', 'AWS', 'Google Cloud Platform', 'Microsoft Azure', 'Docker', 'Kubernetes', 'CircleCI', 'Travis CI', 'Jenkins', 'Git', 'GitHub', 'Bitbucket', 'GitLab', 'SVN', 'Continuous Integration', 'Continuous Deployment', 'Agile Methodologies', 'Scrum', 'Kanban', 'Lean UX', 'User Research', 'Wireframing', 'Prototyping', 'Interaction Design', 'Information Architecture', 'Accessibility', 'Performance Optimization', 'SEO', 'SEM', 'Google Analytics', 'Google Tag Manager', 'A/B Testing', 'User Testing', 'Conversion Rate Optimization', 'Heatmaps', 'Click Tracking', 'Session Recording', 'Content Management Systems', 'Version Control', 'REST APIs', 'GraphQL', 'WebSocket', 'OAuth', 'JSON Web Tokens', 'Firebase', 'MongoDB', 'MySQL', 'PostgreSQL', 'Redis', 'Elasticsearch', 'AWS Lambda', 'Serverless Architecture', 'Microservices', 'Node.js', 'Python', 'Ruby', 'PHP', 'Java', 'C#', 'C++', 'Swift', 'Objective-C', 'Kotlin', 'Rust', 'Scala', 'Haskell', 'WebRTC', 'Peer-to-Peer Networking', 'WebSockets', 'WebRTC Data Channels', 'Real-Time Communication', 'Web Audio API', 'Web MIDI API', 'WebGL', 'WebVR', 'WebXR', 'ARCore', 'ARKit', 'A-Frame', 'Unity', 'Unreal Engine']


# # Hard Skills
# hard_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration', 'Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application']
# all_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Bootstrap', 'jQuery', 'TypeScript', 'Webpack', 'Babel', 'ESLint', 'Prettier', 'Jest', 'Enzyme', 'Cypress', 'RESTful API', 'GraphQL', 'Node.js', 'Express.js', 'MongoDB', 'MySQL', 'PostgreSQL', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Command Line', 'Agile', 'Scrum', 'Kanban', 'UI Design', 'UX Design', 'Responsive Design', 'Accessibility', 'Cross-Browser Compatibility', 'Performance Optimization', 'SEO', 'Google Analytics', 'Google Tag Manager', 'Google Search Console', 'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'InVision', 'Zeplin', 'Web Performance', 'Web Security', 'Continuous Integration', 'Continuous Deployment', 'Containerization', 'Microservices', 'Serverless', 'Amazon Web Services', 'Google Cloud Platform', 'Microsoft Azure', 'Firebase', 'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Content Delivery Network', 'Web Socket', 'Service Worker', 'Progressive Web App', 'Single Page Application', 'Server-Side Rendering', 'Static Site Generation', 'Headless CMS', 'Headless E-commerce', 'E-commerce Integration', 'Payment Gateway Integration', 'Third-Party API Integration', 'Authentication', 'Authorization', 'OAuth', 'JWT', 'Multilingual Website', 'Chatbot Integration', 'Video Integration', 'Audio Integration', 'Web Animation', 'WebRTC', 'Web Scraping', 'Data Visualization', 'Machine Learning', 'Artificial Intelligence', 'Blockchain', 'Cryptocurrency', 'Decentralized Application','Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship']

# # Soft Skills
# soft_skills = ['Communication', 'Collaboration', 'Teamwork', 'Problem Solving', 'Critical Thinking', 'Time Management', 'Project Management', 'Leadership', 'Mentoring', 'Empathy', 'Active Listening', 'Open-Mindedness', 'Flexibility', 'Adaptability', 'Creativity', 'Innovation', 'Curiosity', 'Continuous Learning', 'Attention to Detail', 'Quality Assurance', 'Attention to User Experience', 'Customer Service', 'Marketing', 'Sales', 'Negotiation', 'Conflict Resolution', 'Stress Management', 'Self-Motivation', 'Self-Discipline', 'Self-Awareness', 'Self-Improvement', 'Self-Confidence', 'Self-Efficacy', 'Positive Attitude', 'Professionalism', 'Integrity', 'Ethics', 'Diversity and Inclusion', 'Cultural Awareness', 'Global Mindset', 'Entrepreneurship']
