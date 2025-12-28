#!/usr/bin/env python3
"""
Kurs verilerini veritabanına ekler
"""
from db import get_db_connection, init_database
import os

# Sistemdeki skills listesine göre kurslar ve keywordleri
courses_data = [
    {
        "name": "React - The Complete Guide",
        "keywords": "react javascript frontend ui design single page application",
        "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux"
    },
    {
        "name": "Angular - Complete Guide",
        "keywords": "angular typescript frontend single page application",
        "link": "https://www.udemy.com/course/the-complete-guide-to-angular-2"
    },
    {
        "name": "Vue.js - Complete Guide",
        "keywords": "vue.js javascript frontend single page application",
        "link": "https://www.udemy.com/course/vuejs-2-the-complete-guide"
    },
    {
        "name": "Node.js - Complete Developer Guide",
        "keywords": "node.js express.js javascript backend restful api",
        "link": "https://www.udemy.com/course/nodejs-the-complete-guide"
    },
    {
        "name": "MongoDB - The Complete Developer's Guide",
        "keywords": "mongodb database nosql",
        "link": "https://www.udemy.com/course/mongodb-the-complete-developers-guide"
    },
    {
        "name": "PostgreSQL - Complete Course",
        "keywords": "postgresql database sql relational database",
        "link": "https://www.udemy.com/course/postgresql-complete-course"
    },
    {
        "name": "MySQL - Complete Course",
        "keywords": "mysql database sql relational database",
        "link": "https://www.udemy.com/course/mysql-complete-course"
    },
    {
        "name": "GraphQL with React",
        "keywords": "graphql react restful api",
        "link": "https://www.udemy.com/course/graphql-with-react-course"
    },
    {
        "name": "TypeScript - The Complete Guide",
        "keywords": "typescript javascript webpack babel",
        "link": "https://www.udemy.com/course/typescript-the-complete-developers-guide"
    },
    {
        "name": "JavaScript - The Complete Guide",
        "keywords": "javascript webpack babel eslint prettier",
        "link": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced"
    },
    {
        "name": "Git & GitHub - Complete Guide",
        "keywords": "git github gitlab bitbucket version control",
        "link": "https://www.udemy.com/course/git-complete"
    },
    {
        "name": "AWS Certified Solutions Architect",
        "keywords": "amazon web services aws cloud serverless microservices",
        "link": "https://www.udemy.com/course/aws-certified-solutions-architect-associate"
    },
    {
        "name": "Microsoft Azure Fundamentals",
        "keywords": "microsoft azure cloud serverless microservices",
        "link": "https://www.udemy.com/course/azure-fundamentals"
    },
    {
        "name": "Google Cloud Platform - Complete Guide",
        "keywords": "google cloud platform cloud serverless microservices",
        "link": "https://www.udemy.com/course/google-cloud-platform"
    },
    {
        "name": "Docker & Kubernetes - Complete Guide",
        "keywords": "docker kubernetes containerization microservices continuous deployment",
        "link": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide"
    },
    {
        "name": "Microservices Architecture",
        "keywords": "microservices serverless continuous integration continuous deployment",
        "link": "https://www.udemy.com/course/microservices-with-node-js-and-react"
    },
    {
        "name": "CI/CD with Jenkins",
        "keywords": "continuous integration continuous deployment jenkins",
        "link": "https://www.udemy.com/course/jenkins-from-zero-to-hero"
    },
    {
        "name": "Testing with Jest",
        "keywords": "jest testing unit testing",
        "link": "https://www.udemy.com/course/jest-testing"
    },
    {
        "name": "Cypress - End-to-End Testing",
        "keywords": "cypress testing end to end testing",
        "link": "https://www.udemy.com/course/cypress-tutorial"
    },
    {
        "name": "Webpack & Babel - Complete Guide",
        "keywords": "webpack babel javascript build tools",
        "link": "https://www.udemy.com/course/webpack-2-the-complete-developers-guide"
    },
    {
        "name": "ESLint & Prettier Setup",
        "keywords": "eslint prettier code quality javascript",
        "link": "https://www.udemy.com/course/eslint-prettier"
    },
    {
        "name": "RESTful API Design",
        "keywords": "restful api rest api json",
        "link": "https://www.udemy.com/course/rest-api-design"
    },
    {
        "name": "Express.js - Complete Guide",
        "keywords": "express.js node.js backend restful api",
        "link": "https://www.udemy.com/course/nodejs-express-tutorial"
    },
    {
        "name": "Bootstrap - Complete Course",
        "keywords": "bootstrap css responsive design ui design",
        "link": "https://www.udemy.com/course/bootstrap-4-bootcamp"
    },
    {
        "name": "jQuery - Complete Course",
        "keywords": "jquery javascript frontend",
        "link": "https://www.udemy.com/course/jquery-tutorial"
    },
    {
        "name": "Firebase - Complete Guide",
        "keywords": "firebase cloud serverless authentication",
        "link": "https://www.udemy.com/course/firebase-react"
    },
    {
        "name": "Heroku Deployment",
        "keywords": "heroku cloud deployment continuous deployment",
        "link": "https://www.udemy.com/course/deploy-nodejs-heroku"
    },
    {
        "name": "Netlify & Vercel Deployment",
        "keywords": "netlify vercel cloud deployment static site generation",
        "link": "https://www.udemy.com/course/netlify-vercel-deployment"
    },
    {
        "name": "Web Performance Optimization",
        "keywords": "web performance performance optimization seo",
        "link": "https://www.udemy.com/course/web-performance"
    },
    {
        "name": "Web Security Fundamentals",
        "keywords": "web security authentication authorization oauth jwt",
        "link": "https://www.udemy.com/course/web-security"
    },
    {
        "name": "OAuth & JWT Authentication",
        "keywords": "oauth jwt authentication authorization",
        "link": "https://www.udemy.com/course/oauth-jwt-authentication"
    },
    {
        "name": "Progressive Web App (PWA)",
        "keywords": "progressive web app service worker web performance",
        "link": "https://www.udemy.com/course/progressive-web-apps"
    },
    {
        "name": "Server-Side Rendering with Next.js",
        "keywords": "server-side rendering next.js react static site generation",
        "link": "https://www.udemy.com/course/nextjs-react"
    },
    {
        "name": "WebSocket Programming",
        "keywords": "web socket real-time communication",
        "link": "https://www.udemy.com/course/websocket-programming"
    },
    {
        "name": "SEO Optimization",
        "keywords": "seo google analytics google search console performance optimization",
        "link": "https://www.udemy.com/course/seo-training"
    },
    {
        "name": "Google Analytics & Tag Manager",
        "keywords": "google analytics google tag manager google search console seo",
        "link": "https://www.udemy.com/course/google-analytics"
    },
    {
        "name": "Figma - UI/UX Design",
        "keywords": "figma ui design ux design responsive design",
        "link": "https://www.udemy.com/course/figma-ui-ux-design"
    },
    {
        "name": "Adobe Photoshop for Web Design",
        "keywords": "adobe photoshop ui design",
        "link": "https://www.udemy.com/course/adobe-photoshop-web-design"
    },
    {
        "name": "Sketch - UI Design",
        "keywords": "sketch ui design ux design",
        "link": "https://www.udemy.com/course/sketch-ui-design"
    },
    {
        "name": "Agile & Scrum Masterclass",
        "keywords": "agile scrum kanban project management",
        "link": "https://www.udemy.com/course/agile-scrum-masterclass"
    },
    {
        "name": "Kanban Methodology",
        "keywords": "kanban agile project management",
        "link": "https://www.udemy.com/course/kanban-methodology"
    },
    {
        "name": "Accessibility (A11y) for Web",
        "keywords": "accessibility responsive design ui design",
        "link": "https://www.udemy.com/course/web-accessibility"
    },
    {
        "name": "Cross-Browser Compatibility",
        "keywords": "cross-browser compatibility web performance",
        "link": "https://www.udemy.com/course/cross-browser-compatibility"
    },
    {
        "name": "Machine Learning Fundamentals",
        "keywords": "machine learning artificial intelligence data visualization",
        "link": "https://www.udemy.com/course/machine-learning"
    },
    {
        "name": "Data Visualization with D3.js",
        "keywords": "data visualization javascript",
        "link": "https://www.udemy.com/course/data-visualization-d3js"
    },
    {
        "name": "Web Scraping with Python",
        "keywords": "web scraping data visualization",
        "link": "https://www.udemy.com/course/web-scraping"
    },
    {
        "name": "Blockchain & Cryptocurrency",
        "keywords": "blockchain cryptocurrency decentralized application",
        "link": "https://www.udemy.com/course/blockchain-cryptocurrency"
    },
    {
        "name": "WebRTC Programming",
        "keywords": "webrtc video integration audio integration",
        "link": "https://www.udemy.com/course/webrtc-programming"
    },
    {
        "name": "Web Animation Techniques",
        "keywords": "web animation javascript css",
        "link": "https://www.udemy.com/course/web-animation"
    },
    {
        "name": "Headless CMS Development",
        "keywords": "headless cms server-side rendering static site generation",
        "link": "https://www.udemy.com/course/headless-cms"
    },
    {
        "name": "E-commerce Integration",
        "keywords": "e-commerce integration payment gateway integration",
        "link": "https://www.udemy.com/course/ecommerce-integration"
    },
    {
        "name": "Payment Gateway Integration",
        "keywords": "payment gateway integration e-commerce integration",
        "link": "https://www.udemy.com/course/payment-gateway-integration"
    },
    {
        "name": "Third-Party API Integration",
        "keywords": "third-party api integration restful api",
        "link": "https://www.udemy.com/course/third-party-api-integration"
    },
    {
        "name": "Multilingual Website Development",
        "keywords": "multilingual website internationalization",
        "link": "https://www.udemy.com/course/multilingual-website"
    },
    {
        "name": "Chatbot Integration",
        "keywords": "chatbot integration artificial intelligence",
        "link": "https://www.udemy.com/course/chatbot-integration"
    },
    {
        "name": "Content Delivery Network (CDN)",
        "keywords": "content delivery network cloudflare web performance",
        "link": "https://www.udemy.com/course/cdn-cloudflare"
    },
    {
        "name": "Command Line Mastery",
        "keywords": "command line git github",
        "link": "https://www.udemy.com/course/command-line-mastery"
    },
    {
        "name": "Problem Solving & Critical Thinking",
        "keywords": "problem solving critical thinking",
        "link": "https://www.udemy.com/course/problem-solving-critical-thinking"
    },
    {
        "name": "Time Management for Developers",
        "keywords": "time management project management",
        "link": "https://www.udemy.com/course/time-management-developers"
    },
    {
        "name": "Project Management Fundamentals",
        "keywords": "project management agile scrum",
        "link": "https://www.udemy.com/course/project-management-fundamentals"
    },
    {
        "name": "Leadership & Team Management",
        "keywords": "leadership mentoring collaboration teamwork",
        "link": "https://www.udemy.com/course/leadership-team-management"
    },
    {
        "name": "Communication Skills",
        "keywords": "communication collaboration teamwork active listening",
        "link": "https://www.udemy.com/course/communication-skills"
    },
    {
        "name": "Quality Assurance & Testing",
        "keywords": "quality assurance attention to detail testing",
        "link": "https://www.udemy.com/course/quality-assurance-testing"
    }
]

def add_courses():
    """Kursları veritabanına ekler"""
    # Veritabanının var olduğundan emin ol
    if not os.path.exists("tez_db.sqlite"):
        print("Veritabanı bulunamadı. Önce init_db.py çalıştırın.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Mevcut kursları kontrol et
    cursor.execute("SELECT COUNT(*) FROM courses")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Veritabanında {existing_count} kurs zaten var. Yine de eklemek istiyor musunuz? (y/n)")
        response = input().lower()
        if response != 'y':
            print("İşlem iptal edildi.")
            conn.close()
            return
        # Mevcut kursları temizle (opsiyonel)
        # cursor.execute("DELETE FROM courses")
        # conn.commit()
    
    added_count = 0
    for course in courses_data:
        try:
            cursor.execute(
                "INSERT INTO courses (name, keywords, link) VALUES (?, ?, ?)",
                (course["name"], course["keywords"], course["link"])
            )
            added_count += 1
            print(f"✓ Eklendi: {course['name']}")
        except Exception as e:
            print(f"✗ Hata ({course['name']}): {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\nToplam {added_count} kurs eklendi.")

if __name__ == "__main__":
    add_courses()

