import os
from werkzeug.security import generate_password_hash
from database.db import db

def seed_data():
    # 1. Clear existing data (optional, for clean slate)
    print("Clearing old data...")
    db.users.delete_many({})
    db.aptitude_questions.delete_many({})
    db.coding_problems.delete_many({})
    db.interview_questions.delete_many({})
    db.companies.delete_many({})
    db.resources.delete_many({})
    db.mock_tests.delete_many({})
    
    # 2. Add Admin User
    admin_user = {
        "name": "Admin",
        "email": "admin@example.com",
        "password": generate_password_hash("admin123"),
        "role": "admin"
    }
    db.users.insert_one(admin_user)
    print("Added default admin (admin@example.com / admin123)")

    # 3. Add 20 Aptitude Questions
    aptitude_data = [
        {"question": "What is 20% of 250?", "options": ["25", "40", "50", "60"], "answer": "50", "explanation": "20/100 × 250 = 50", "category": "Quantitative Aptitude", "difficulty": "Easy"},
        {"question": "A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?", "options": ["120 metres", "180 metres", "324 metres", "150 metres"], "answer": "150 metres", "explanation": "Speed = 60 * (5/18) m/sec = 50/3 m/sec. Length = Speed * Time = (50/3) * 9 = 150 m.", "category": "Quantitative Aptitude", "difficulty": "Medium"},
        {"question": "Find the missing number in the series: 2, 5, 10, 17, 26, ?", "options": ["32", "37", "41", "39"], "answer": "37", "explanation": "The differences are 3, 5, 7, 9, 11. 26+11 = 37.", "category": "Logical Reasoning", "difficulty": "Easy"},
        {"question": "Look at this series: 36, 34, 30, 28, 24, ... What number should come next?", "options": ["20", "22", "23", "26"], "answer": "22", "explanation": "Alternating subtraction of 2, then 4.", "category": "Logical Reasoning", "difficulty": "Easy"},
        {"question": "Choose the word which is different from the rest.", "options": ["Chicken", "Snake", "Swan", "Crocodile"], "answer": "Chicken", "explanation": "Others can live in water, chicken cannot.", "category": "Verbal Ability", "difficulty": "Easy"},
        {"question": "Antonym of 'ENORMOUS'", "options": ["Soft", "Average", "Tiny", "Weak"], "answer": "Tiny", "explanation": "Enormous means huge.", "category": "Verbal Ability", "difficulty": "Easy"},
        {"question": "A can do a work in 15 days and B in 20 days. If they work on it together for 4 days, then the fraction of the work that is left is:", "options": ["1/4", "1/10", "7/15", "8/15"], "answer": "8/15", "explanation": "A's 1 day work = 1/15, B's = 1/20. Together 1 day = 7/60. 4 days = 28/60 = 7/15. Left = 1 - 7/15 = 8/15.", "category": "Quantitative Aptitude", "difficulty": "Medium"},
        {"question": "If A is the brother of B; B is the sister of C; and C is the father of D, how D is related to A?", "options": ["Brother", "Sister", "Nephew", "Cannot be determined"], "answer": "Cannot be determined", "explanation": "Gender of D is unknown.", "category": "Logical Reasoning", "difficulty": "Medium"},
        {"question": "Average of 5 numbers is 20. If one number is excluded, average becomes 15. The excluded number is:", "options": ["35", "40", "45", "50"], "answer": "40", "explanation": "Total of 5 = 100. Total of 4 = 60. Excluded = 100 - 60 = 40.", "category": "Quantitative Aptitude", "difficulty": "Easy"},
        {"question": "Synonym of 'CANDID'", "options": ["Apparent", "Explicit", "Frank", "Bright"], "answer": "Frank", "explanation": "Candid means truthful and straightforward.", "category": "Verbal Ability", "difficulty": "Medium"},
        {"question": "Insert the missing number: 16, 33, 65, 131, 261, (...) ", "options": ["523", "521", "613", "721"], "answer": "523", "explanation": "Each number is twice the previous plus 1, 2, 3... -> 16*2+1=33, 33*2-1=65, 65*2+1=131, 131*2-1=261, 261*2+1=523.", "category": "Logical Reasoning", "difficulty": "Hard"},
        {"question": "Data Interpretation: Table shows sales. Q: What is the total?", "options": ["100", "200", "300", "400"], "answer": "200", "explanation": "Dummy sum.", "category": "Data Interpretation", "difficulty": "Easy"},
        {"question": "A bag contains 6 black and 8 white balls. One ball is drawn at random. What is the probability that the ball drawn is white?", "options": ["3/4", "4/7", "1/8", "3/7"], "answer": "4/7", "explanation": "P = 8/14 = 4/7", "category": "Quantitative Aptitude", "difficulty": "Easy"},
        {"question": "What is the next number: 1, 4, 9, 16, ?", "options": ["20", "25", "30", "36"], "answer": "25", "explanation": "Squares of 1, 2, 3, 4, 5.", "category": "Logical Reasoning", "difficulty": "Easy"},
        {"question": "Which of the following is not a prime number?", "options": ["31", "61", "71", "91"], "answer": "91", "explanation": "91 is divisible by 7 (13*7).", "category": "Quantitative Aptitude", "difficulty": "Easy"},
        {"question": "Choose correctly spelt word", "options": ["Accomodation", "Accommodation", "Accomodasion", "Accomadation"], "answer": "Accommodation", "explanation": "Correct spelling is Accommodation.", "category": "Verbal Ability", "difficulty": "Medium"},
        {"question": "The sum of ages of 5 children born at the intervals of 3 years each is 50 years. What is the age of the youngest child?", "options": ["4", "8", "10", "None"], "answer": "4", "explanation": "x+(x+3)+(x+6)+(x+9)+(x+12)=50 -> 5x+30=50 -> 5x=20 -> x=4.", "category": "Quantitative Aptitude", "difficulty": "Medium"},
        {"question": "Pointing to a photograph of a boy Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?", "options": ["Brother", "Uncle", "Cousin", "Father"], "answer": "Father", "explanation": "The only son of his mother is Suresh himself. So the boy is his son.", "category": "Logical Reasoning", "difficulty": "Easy"},
        {"question": "I am facing South. I turn right and walk 20 m. Then I turn right again and walk 10 m. Then I turn left and walk 10 m and then turning right walk 20 m. Then I turn right again and walk 60 m. In which direction am I from the starting point?", "options": ["North", "North-West", "East", "North-East"], "answer": "North-East", "explanation": "Draw the path.", "category": "Logical Reasoning", "difficulty": "Hard"},
        {"question": "Data Interpretation: Graph shows... Q: Find ratio.", "options": ["1:2", "2:3", "3:4", "4:5"], "answer": "1:2", "explanation": "Dummy ratio.", "category": "Data Interpretation", "difficulty": "Easy"}
    ]
    db.aptitude_questions.insert_many(aptitude_data)
    print("Added aptitude questions.")

    # 4. Add 10 Coding Problems
    coding_data = [
        {"title": "Two Sum", "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.", "difficulty": "Easy", "topic": "Arrays", "example_input": "nums = [2,7,11,15], target = 9", "example_output": "[0,1]", "constraints": "2 <= nums.length <= 10^4", "expected_approach": "Use a hash map to store the difference and index."},
        {"title": "Reverse String", "description": "Write a function that reverses a string.", "difficulty": "Easy", "topic": "Strings", "example_input": "s = ['h','e','l','l','o']", "example_output": "['o','l','l','e','h']", "constraints": "1 <= s.length <= 10^5", "expected_approach": "Use two pointers, swap front and back."},
        {"title": "Binary Search", "description": "Given a sorted array, find target index.", "difficulty": "Easy", "topic": "Searching", "example_input": "nums=[-1,0,3,5,9,12], target=9", "example_output": "4", "constraints": "sorted array", "expected_approach": "mid = left + (right - left) / 2"},
        {"title": "Merge Sort", "description": "Sort an array using merge sort.", "difficulty": "Medium", "topic": "Sorting", "example_input": "[5,2,3,1]", "example_output": "[1,2,3,5]", "constraints": "O(n log n)", "expected_approach": "Divide and conquer."},
        {"title": "Reverse Linked List", "description": "Reverse a singly linked list.", "difficulty": "Easy", "topic": "Linked Lists", "example_input": "head = [1,2,3,4,5]", "example_output": "[5,4,3,2,1]", "constraints": "Nodes 0 to 5000", "expected_approach": "Iterative or recursive approach."},
        {"title": "Valid Parentheses", "description": "Determine if input string has valid parentheses.", "difficulty": "Easy", "topic": "Stack", "example_input": "'()[]{}'", "example_output": "true", "constraints": "1 <= s.length <= 10^4", "expected_approach": "Use a stack to keep track of open brackets."},
        {"title": "Implement Queue using Stacks", "description": "Implement a FIFO queue using only two stacks.", "difficulty": "Easy", "topic": "Queue", "example_input": "push(1), push(2), peek(), pop()", "example_output": "1, 1", "constraints": "Valid ops", "expected_approach": "Transfer items between two stacks on pop/peek."},
        {"title": "Fibonacci Number", "description": "Calculate n-th Fibonacci number.", "difficulty": "Easy", "topic": "Recursion", "example_input": "n = 3", "example_output": "2", "constraints": "0 <= n <= 30", "expected_approach": "Memoization or iterative bottom-up."},
        {"title": "Longest Substring Without Repeating Characters", "description": "Find length of longest substring without repeating characters.", "difficulty": "Medium", "topic": "Strings", "example_input": "s = 'abcabcbb'", "example_output": "3", "constraints": "0 <= s.length <= 5*10^4", "expected_approach": "Sliding window."},
        {"title": "Maximum Subarray", "description": "Find contiguous subarray with largest sum.", "difficulty": "Medium", "topic": "Arrays", "example_input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "example_output": "6", "constraints": "O(n)", "expected_approach": "Kadane's Algorithm."}
    ]
    db.coding_problems.insert_many(coding_data)
    print("Added coding problems.")

    # 5. Add 15 Interview Questions
    interview_data = [
        {"question": "Tell me about yourself.", "category": "HR Interview Questions", "model_answer": "Start with present, go to past, then future. Highlight relevant skills.", "difficulty": "Easy"},
        {"question": "What are your strengths and weaknesses?", "category": "HR Interview Questions", "model_answer": "Strength: quick learner. Weakness: perfectionist (frame positively).", "difficulty": "Easy"},
        {"question": "Why should we hire you?", "category": "HR Interview Questions", "model_answer": "Match your skills with the job description.", "difficulty": "Medium"},
        {"question": "Where do you see yourself in five years?", "category": "HR Interview Questions", "model_answer": "Taking on more responsibilities, leading a team.", "difficulty": "Medium"},
        {"question": "Why do you want to join our company?", "category": "HR Interview Questions", "model_answer": "Research the company, mention their recent projects or work culture.", "difficulty": "Medium"},
        {"question": "Describe a time you faced a conflict.", "category": "Behavioral Questions", "model_answer": "Use STAR method (Situation, Task, Action, Result).", "difficulty": "Hard"},
        {"question": "How do you handle pressure?", "category": "Behavioral Questions", "model_answer": "Prioritize tasks, take breaks, stay organized.", "difficulty": "Medium"},
        {"question": "What is Object-Oriented Programming?", "category": "Technical Interview Questions", "model_answer": "Paradigm based on objects. Key concepts: Encapsulation, Abstraction, Inheritance, Polymorphism.", "difficulty": "Easy"},
        {"question": "Explain normalization in DBMS.", "category": "Technical Interview Questions", "model_answer": "Organizing data to reduce redundancy. 1NF, 2NF, 3NF.", "difficulty": "Medium"},
        {"question": "Difference between Process and Thread.", "category": "Technical Interview Questions", "model_answer": "Process is a program in execution, thread is a segment of a process.", "difficulty": "Medium"},
        {"question": "What is the OSI model?", "category": "Technical Interview Questions", "model_answer": "7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.", "difficulty": "Medium"},
        {"question": "Explain Binary Search Tree.", "category": "Technical Interview Questions", "model_answer": "Left child < parent, right child > parent.", "difficulty": "Medium"},
        {"question": "What are RESTful APIs?", "category": "Technical Interview Questions", "model_answer": "Representational State Transfer. Uses HTTP methods like GET, POST, PUT, DELETE.", "difficulty": "Easy"},
        {"question": "Difference between list and tuple in Python.", "category": "Technical Interview Questions", "model_answer": "List is mutable, tuple is immutable.", "difficulty": "Easy"},
        {"question": "How do you communicate complex technical details to non-technical stakeholders?", "category": "Communication Questions", "model_answer": "Use analogies, avoid jargon, focus on business impact.", "difficulty": "Hard"}
    ]
    db.interview_questions.insert_many(interview_data)
    print("Added interview questions.")

    # 6. Add 5 Companies
    company_data = [
        {"name": "TCS", "description": "Tata Consultancy Services is an Indian multinational information technology services and consulting company.", "job_roles": "Ninja, Digital", "skills": "Java, Python, DBMS, Aptitude", "eligibility": "60% throughout, no active backlogs", "selection_process": "NQT (Aptitude + Coding), Technical Interview, HR", "difficulty": "Medium", "frequently_asked": "Arrays, Strings, OOPS", "interview_questions": "What is polymorphism? Explain SQL joins."},
        {"name": "Infosys", "description": "Infosys Limited is an Indian multinational information technology company.", "job_roles": "System Engineer, Specialist Programmer", "skills": "C++, Python, Web Dev", "eligibility": "60% or 6.5 CGPA", "selection_process": "Online Test, Technical, HR", "difficulty": "Medium", "frequently_asked": "Puzzles, DBMS", "interview_questions": "Write a query to find 2nd highest salary."},
        {"name": "Amazon", "description": "Amazon is an American multinational technology company focusing on e-commerce, cloud computing.", "job_roles": "SDE-1", "skills": "DSA, System Design, Java/C++", "eligibility": "7.0 CGPA", "selection_process": "Online Assessment (DSA), 3-4 Tech rounds, Bar Raiser", "difficulty": "Hard", "frequently_asked": "Graphs, DP, Trees", "interview_questions": "Design an LRU Cache."},
        {"name": "Microsoft", "description": "Microsoft Corporation is an American multinational technology corporation.", "job_roles": "Software Engineer", "skills": "DSA, OOPS, OS", "eligibility": "7.0 CGPA", "selection_process": "Online Coding, 3 Tech rounds, AA round", "difficulty": "Hard", "frequently_asked": "Linked Lists, Strings, OS Concepts", "interview_questions": "Reverse a linked list in groups of k."},
        {"name": "Wipro", "description": "Wipro is a leading global information technology, consulting and business process services company.", "job_roles": "Project Engineer", "skills": "Java, SQL, Aptitude", "eligibility": "60% throughout", "selection_process": "NLTH, Technical Interview, HR", "difficulty": "Easy", "frequently_asked": "Core Java, SQL queries", "interview_questions": "Difference between abstract class and interface."}
    ]
    db.companies.insert_many(company_data)
    print("Added companies.")

    # 7. Add 5 Study Resources
    resource_data = [
        {"title": "Quantitative Aptitude Formulas", "description": "Quick cheat sheet for all major quant topics.", "category": "Aptitude notes", "content": "1. Speed = Distance/Time... 2. Simple Interest = P*R*T/100...", "date_added": "2023-10-01"},
        {"title": "Top 50 HR Questions", "description": "A comprehensive list of HR questions with answers.", "category": "Interview tips", "content": "1. Tell me about yourself... 2. Strengths and Weaknesses...", "date_added": "2023-10-02"},
        {"title": "Resume Writing Best Practices", "description": "How to make your resume stand out.", "category": "Resume tips", "content": "Keep it 1 page. Use action verbs. Highlight achievements.", "date_added": "2023-10-03"},
        {"title": "Operating Systems Quick Revision", "description": "Key OS concepts for interviews.", "category": "Technical preparation notes", "content": "Deadlock conditions: Mutual Exclusion, Hold and Wait, No preemption, Circular Wait.", "date_added": "2023-10-04"},
        {"title": "SDE Roadmap 2024", "description": "Step by step guide to crack SDE roles.", "category": "Placement preparation roadmaps", "content": "Month 1: Learn a language. Month 2: Basic DSA. Month 3: Advanced DSA. Month 4: Core Subjects.", "date_added": "2023-10-05"}
    ]
    db.resources.insert_many(resource_data)
    print("Added resources.")
    
    # 8. Add 2 Mock Tests
    mock_test_data = [
        {"title": "TCS NQT Mock Test 1", "duration": 60, "total_questions": 10, "questions": aptitude_data[:10]},
        {"title": "Infosys Mock Test 1", "duration": 45, "total_questions": 10, "questions": aptitude_data[10:20]}
    ]
    db.mock_tests.insert_many(mock_test_data)
    print("Added mock tests.")

    print("Seed complete!")

if __name__ == '__main__':
    seed_data()
