"""
Configuration file for the CV-Job Matching System
Contains centralized skill lists and system configurations
"""

# ============================================================
# SKILLS LIST - Central repository of all tracked skills
# ============================================================

SKILLS = [
    # Frontend Frameworks & Libraries
    'HTML',
    'CSS',
    'JavaScript',
    'React',
    'Angular',
    'Vue.js',
    'Bootstrap',
    'jQuery',
    'TypeScript',
    
    # Programming Languages
    'Python',
    'Java',
    'C++',
    'C#',
    'Go',
    'Rust',
    'PHP',
    'Ruby',
    'Swift',
    'Kotlin',
    
    # Build Tools & Module Bundlers
    'Webpack',
    'Babel',
    'ESLint',
    'Prettier',
    
    # Testing Frameworks
    'Jest',
    'Enzyme',
    'Cypress',
    
    # API Technologies
    'RESTful API',
    'GraphQL',
    
    # Backend Technologies
    'Node.js',
    'Express.js',
    '.NET',
    'ASP.NET',
    'Django',
    'Flask',
    'Spring Boot',
    'Laravel',
    'Ruby on Rails',
    
    # Databases
    'MongoDB',
    'MySQL',
    'PostgreSQL',
    
    # Version Control & Command Line
    'Git',
    'GitHub',
    'GitLab',
    'Bitbucket',
    'Command Line',
    
    # Project Management Methodologies
    'Agile',
    'Scrum',
    'Kanban',
    
    # UI/UX & Design
    'UI Design',
    'UX Design',
    'Responsive Design',
    'Accessibility',
    'Cross-Browser Compatibility',
    
    # Performance & Optimization
    'Performance Optimization',
    'SEO',
    'Web Performance',
    
    # Analytics Tools
    'Google Analytics',
    'Google Tag Manager',
    'Google Search Console',
    
    # Design Tools
    'Adobe Photoshop',
    'Adobe Illustrator',
    'Sketch',
    'Figma',
    'InVision',
    'Zeplin',
    
    # Security
    'Web Security',
    'Authentication',
    'Authorization',
    'OAuth',
    'JWT',
    
    # DevOps & CI/CD
    'Continuous Integration',
    'Continuous Deployment',
    'Containerization',
    'Docker',
    'Kubernetes',
    'Microservices',
    'Serverless',
    
    # Cloud Platforms
    'Amazon Web Services',
    'Google Cloud Platform',
    'Microsoft Azure',
    'Firebase',
    'Heroku',
    'Netlify',
    'Vercel',
    'Cloudflare',
    
    # Web Technologies
    'Content Delivery Network',
    'Web Socket',
    'Service Worker',
    'Progressive Web App',
    'Single Page Application',
    'Server-Side Rendering',
    'Static Site Generation',
    
    # CMS & E-commerce
    'Headless CMS',
    'Headless E-commerce',
    'E-commerce Integration',
    'Payment Gateway Integration',
    'Third-Party API Integration',
    
    # Internationalization & Integration
    'Multilingual Website',
    'Chatbot Integration',
    'Video Integration',
    'Audio Integration',
    
    # Advanced Technologies
    'Web Animation',
    'WebRTC',
    'Web Scraping',
    'Data Visualization',
    'Machine Learning',
    'Artificial Intelligence',
    'Blockchain',
    'Cryptocurrency',
    'Decentralized Application',
    
    # Soft Skills - Communication
    'Communication',
    'Collaboration',
    'Teamwork',
    'Active Listening',
    
    # Soft Skills - Problem Solving
    'Problem Solving',
    'Critical Thinking',
    'Creativity',
    'Innovation',
    
    # Soft Skills - Time & Project Management
    'Time Management',
    'Project Management',
    
    # Soft Skills - Leadership
    'Leadership',
    'Mentoring',
    'Empathy',
    
    # Soft Skills - Personal Attributes
    'Open-Mindedness',
    'Flexibility',
    'Adaptability',
    'Curiosity',
    'Continuous Learning',
    'Attention to Detail',
    'Quality Assurance',
    'Attention to User Experience',
    
    # Soft Skills - Business & Client
    'Customer Service',
    'Marketing',
    'Sales',
    'Negotiation',
    'Conflict Resolution',
    
    # Soft Skills - Self-Management
    'Stress Management',
    'Self-Motivation',
    'Self-Discipline',
    'Self-Awareness',
    'Self-Improvement',
    'Self-Confidence',
    'Self-Efficacy',
    
    # Soft Skills - Professional Values
    'Positive Attitude',
    'Professionalism',
    'Integrity',
    'Ethics',
    'Diversity and Inclusion',
    'Cultural Awareness',
    'Global Mindset',
    'Entrepreneurship',
     # Modern Frontend
    'Next.js',
    'Tailwind CSS',
    'Vite',
    'Svelte',
    
    # Data Science & ML
    'TensorFlow',
    'PyTorch',
    'Scikit-learn',
    'Pandas',
    'NumPy',
    'Jupyter',
    
    # DevOps & Infrastructure
    'Terraform',
    'Ansible',
    'Jenkins',
    'GitHub Actions',
    'Nginx',
    'Apache',
    
    # Testing
    'Selenium',
    'Pytest',
    'JUnit',
    
    # Mobile
    'React Native',
    'Flutter',
    
    # Databases & Messaging
    'Redis',
    'Elasticsearch',
    'Kafka',
    'RabbitMQ'
]



# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_skills():
    """
    Returns normalized (lowercase) skill list
    
    Returns:
        list: List of lowercase skill strings
    
    Example:
        >>> skills = get_skills()
        >>> 'react' in skills
        True
    """
    return [skill.lower() for skill in SKILLS]


def get_skills_count():
    """
    Returns total number of skills in the system
    
    Returns:
        int: Total skill count
    """
    return len(SKILLS)


def get_skills_by_category():
    """
    Returns skills organized by category
    
    Returns:
        dict: Dictionary of skill categories
    """
    return {
        'frontend': [
            'html', 'css', 'javascript', 'react', 'angular', 'vue.js',
            'bootstrap', 'jquery', 'typescript', 'next.js', 'tailwind css',
            'vite', 'svelte'
        ],
        'backend': [
            'node.js', 'express.js', 'django', 'flask', 'spring boot',
            'laravel', 'ruby on rails', '.net', 'asp.net'
        ],
        'database': [
            'mongodb', 'mysql', 'postgresql', 'redis', 'elasticsearch'
        ],
        'devops': [
            'git', 'github', 'gitlab', 'bitbucket', 'continuous integration',
            'continuous deployment', 'containerization', 'microservices',
            'serverless', 'docker', 'kubernetes', 'terraform', 'ansible',
            'jenkins', 'github actions', 'nginx', 'apache'
        ],
        'cloud': [
            'amazon web services', 'google cloud platform', 'microsoft azure',
            'firebase', 'heroku', 'netlify', 'vercel', 'cloudflare'
        ],
        'design': [
            'ui design', 'ux design', 'responsive design', 'adobe photoshop',
            'adobe illustrator', 'sketch', 'figma', 'invision', 'zeplin'
        ],
        'testing': [
            'jest', 'enzyme', 'cypress', 'quality assurance', 'selenium',
            'pytest', 'junit'
        ],
        'methodology': [
            'agile', 'scrum', 'kanban', 'project management'
        ],
        'data_science': [
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'jupyter', 'machine learning', 'artificial intelligence',
            'data visualization'
        ],
        'mobile': [
            'react native', 'flutter', 'swift', 'kotlin'
        ],
        'messaging': [
            'kafka', 'rabbitmq'
        ],
        'soft_skills': [
            'communication', 'collaboration', 'teamwork', 'problem solving',
            'critical thinking', 'leadership', 'time management', 'creativity',
            'adaptability', 'continuous learning'
        ]
    }

# ============================================================
# CONFIGURATION CONSTANTS
# ============================================================

# File upload settings
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# CV processing settings
MIN_SKILLS_FOR_QUALITY_CV = 5
MAX_NGRAM_SIZE = 5

# Job matching settings
MIN_JOB_SKILLS = 4  # Minimum skills required in job post for matching

# Database settings
DB_PATH = "tez_db.sqlite"
CV_UPLOAD_PATH = "./static/cvs"




SKILL_SYNONYMS = {
    # Programming Languages
    'javascript': ['js', 'ecmascript', 'es6', 'es2015'],
    'typescript': ['ts'],
    'python': ['py', 'python3'],
    'c++': ['cplusplus', 'cpp'],  # "C++" → "cplusplus" by normalizer
    'c#': ['csharp'],  # "C#" → "csharp" by normalizer
    
    # Frontend Frameworks
    'node.js': ['nodejs', 'node'],  # "Node.js" → "nodejs" by normalizer
    'react': ['reactjs', 'react.js'],  # "React.js" → "reactjs" by normalizer
    'angular': ['angularjs', 'angular.js'],
    'vue.js': ['vuejs', 'vue'],  # "Vue.js" → "vuejs" by normalizer
    'next.js': ['nextjs'],  # "Next.js" → "nextjs" by normalizer
    
    # Backend Frameworks
    'express.js': ['expressjs', 'express'],  # "Express.js" → "expressjs"
    '.net': ['dotnet', 'dot net'],  # ".NET" → "dotnet" by normalizer
    'asp.net': ['aspnet'],
    'django': ['python django'],
    'flask': ['python flask'],
    'spring boot': ['springboot', 'spring'],
    'ruby on rails': ['rails', 'ror'],
    
    # Databases
    'postgresql': ['postgres', 'psql'],
    'mongodb': ['mongo'],
    'mysql': ['my sql'],
    
    # DevOps & Cloud
    'docker': ['containerization'],  # Both are skills, but docker is more specific
    'kubernetes': ['k8s', 'k8'],
    'amazon web services': ['aws'],
    'google cloud platform': ['gcp', 'google cloud'],
    'microsoft azure': ['azure'],
    
    # CI/CD
    'continuous integration': ['ci'],
    'continuous deployment': ['cd'],
    
    # API
    'restful api': ['rest', 'rest api', 'restapi'],
    'graphql': ['gql', 'graph ql'],
     'next.js': ['nextjs', 'next'],
    'tailwind css': ['tailwind', 'tailwindcss'],
    'tensorflow': ['tf'],
    'pytorch': ['torch'],
    'scikit-learn': ['sklearn', 'scikit'],
    'pandas': ['pd'],
    'numpy': ['np'],
    'react native': ['rn', 'reactnative'],
    'github actions': ['gh actions'],
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize_skill(skill):
    """
    Normalizes a skill name using synonyms
    
    Args:
        skill (str): Skill name to normalize
    
    Returns:
        str: Normalized skill name
    
    Example:
        >>> normalize_skill('nodejs')
        'node.js'
        >>> normalize_skill('k8s')
        'kubernetes'
    """
    skill_lower = skill.lower().strip()
    
    # Check if it's already a standard skill
    if skill_lower in get_skills():
        return skill_lower
    
    # Check synonyms
    for standard, synonyms in SKILL_SYNONYMS.items():
        if skill_lower in synonyms:
            return standard
    
    # Return as-is if no match found
    return skill_lower



if __name__ == "__main__":
    # Test the configuration
    print(f"Total skills: {get_skills_count()}")
    print(f"\nFirst 10 skills: {get_skills()[:10]}")
    print(f"\nTesting normalization:")
    print(f"  'nodejs' → '{normalize_skill('nodejs')}'")
    print(f"  'k8s' → '{normalize_skill('k8s')}'")
    print(f"  'reactjs' → '{normalize_skill('reactjs')}'")
    print(f"\nSkill weights:")
    
    