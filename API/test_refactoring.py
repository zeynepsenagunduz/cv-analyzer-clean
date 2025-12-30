#!/usr/bin/env python3
"""
Comprehensive test script for refactored code
Run this after adding config.py and updated files
"""

import sys
import os

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST: {name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def test_config():
    """Test 1: Config module"""
    print_test("Config Module")
    
    try:
        from config import get_skills, normalize_skill, get_skill_weight, get_skills_count
        print_success("Config import successful")
        
        # Test skill count
        count = get_skills_count()
        if count == 106:
            print_success(f"Skill count correct: {count}")
        else:
            print_error(f"Skill count wrong: {count} (expected 106)")
            return False
        
        # Test get_skills
        skills = get_skills()
        if isinstance(skills, list) and len(skills) == 106:
            print_success(f"get_skills() works: {len(skills)} skills loaded")
        else:
            print_error("get_skills() failed")
            return False
        
        # Test normalize_skill
        tests = [
            ('nodejs', 'node.js'),
            ('k8s', 'kubernetes'),
            ('reactjs', 'react'),
        ]
        
        for input_val, expected in tests:
            result = normalize_skill(input_val)
            if result == expected:
                print_success(f"normalize_skill('{input_val}') → '{result}'")
            else:
                print_error(f"normalize_skill('{input_val}') → '{result}' (expected '{expected}')")
                return False
        
        # Test skill weights
        weight = get_skill_weight('react')
        if weight == 3.0:
            print_success(f"get_skill_weight('react') = {weight}")
        else:
            print_warning(f"get_skill_weight('react') = {weight} (expected 3.0)")
        
        return True
        
    except ImportError as e:
        print_error(f"Cannot import config: {e}")
        print_warning("Make sure config.py is in the same directory")
        return False
    except Exception as e:
        print_error(f"Config test failed: {e}")
        return False


def test_helper():
    """Test 2: Helper module"""
    print_test("Helper Module")
    
    try:
        from helper import handleCV, processJobText, create_point
        print_success("Helper import successful")
        
        # Test processJobText
        test_text = "We need React, Node.js, MongoDB, TypeScript, Docker and Kubernetes skills"
        result = processJobText(test_text)
        
        if isinstance(result, list):
            print_success(f"processJobText() works: Found {len(result)} skills")
            print(f"   Skills: {result[:5]}...")
            
            # Check if expected skills are found
            expected_skills = ['react', 'node.js', 'mongodb', 'typescript', 'docker', 'kubernetes']
            found_skills = [s for s in expected_skills if s in result]
            
            if len(found_skills) >= 4:
                print_success(f"Found {len(found_skills)}/{len(expected_skills)} expected skills")
            else:
                print_warning(f"Only found {len(found_skills)}/{len(expected_skills)} expected skills")
        else:
            print_error("processJobText() returned wrong type")
            return False
        
        # Test create_point
        cv_skills = ['react', 'node.js', 'mongodb', 'git']
        job_skills = ['react', 'node.js', 'angular', 'docker', 'kubernetes']
        score = create_point(cv_skills, job_skills)
        
        if isinstance(score, (int, float)) and 0 <= score <= 100:
            print_success(f"create_point() works: {score}%")
            print(f"   CV: {cv_skills}")
            print(f"   Job: {job_skills}")
        else:
            print_error(f"create_point() returned invalid score: {score}")
            return False
        
        return True
        
    except ImportError as e:
        print_error(f"Cannot import helper: {e}")
        return False
    except Exception as e:
        print_error(f"Helper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test 3: Database connection"""
    print_test("Database Connection")
    
    try:
        from db import get_db_connection
        print_success("DB import successful")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'cvs', 'jobposts', 'courses', 'invitecodes']
        missing = [t for t in expected_tables if t not in tables]
        
        if not missing:
            print_success(f"All tables exist: {tables}")
        else:
            print_error(f"Missing tables: {missing}")
            conn.close()
            return False
        
        # Test courses table
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        print_success(f"Courses table: {course_count} courses")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Database test failed: {e}")
        return False


def test_integration():
    """Test 4: Integration test"""
    print_test("Integration Test")
    
    try:
        from config import get_skills
        from helper import processJobText, create_point
        
        # Simulate real scenario
        job_text = """
        Senior Full Stack Developer
        
        Required Skills:
        - React and TypeScript
        - Node.js and Express.js
        - MongoDB or PostgreSQL
        - Docker and Kubernetes
        - Git and GitHub
        - RESTful API design
        
        Nice to have:
        - AWS or Azure
        - GraphQL
        - Microservices
        """
        
        cv_text = """
        Experienced developer with:
        - React and JavaScript (5 years)
        - Node.js and Express.js
        - MongoDB
        - Git, GitHub
        - Docker
        """
        
        # Extract skills
        job_skills = processJobText(job_text)
        cv_skills = processJobText(cv_text)
        
        print_success(f"Job posting: {len(job_skills)} skills extracted")
        print(f"   {job_skills}")
        
        print_success(f"CV: {len(cv_skills)} skills extracted")
        print(f"   {cv_skills}")
        
        # Calculate match
        score = create_point(cv_skills, job_skills)
        print_success(f"Match score: {score}%")
        
        # Find missing skills
        missing = set(job_skills) - set(cv_skills)
        if missing:
            print_warning(f"Missing skills: {list(missing)[:5]}...")
        else:
            print_success("All skills matched!")
        
        return True
        
    except Exception as e:
        print_error(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_paths():
    """Test 5: File paths"""
    print_test("File Path Check")
    
    paths_to_check = [
        './static/cvs',
        './static/jobposts',
        './tez_db.sqlite',
        './config.py',
        './helper.py',
        './db.py',
        './fast.py'
    ]
    
    all_ok = True
    for path in paths_to_check:
        if os.path.exists(path):
            print_success(f"Found: {path}")
        else:
            print_warning(f"Not found: {path}")
            if path in ['./config.py', './helper.py']:
                all_ok = False
    
    return all_ok


def main():
    print(f"\n{BLUE}{'='*60}")
    print("  REFACTORING TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    
    tests = [
        ("File Paths", test_file_paths),
        ("Config Module", test_config),
        ("Helper Module", test_helper),
        ("Database", test_database),
        ("Integration", test_integration),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("  TEST SUMMARY")
    print(f"{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{name:.<40} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    
    if passed == total:
        print(f"{GREEN}✅ ALL TESTS PASSED ({passed}/{total}){RESET}")
        print(f"{GREEN}🎉 Refactoring başarılı! Projeye ekleyebilirsin.{RESET}")
        return 0
    else:
        print(f"{RED}❌ SOME TESTS FAILED ({passed}/{total}){RESET}")
        print(f"{YELLOW}⚠️  Başarısız testleri kontrol et.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
