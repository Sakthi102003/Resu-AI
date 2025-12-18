"""Sample resume data for testing templates"""

# Sample resume data with comprehensive information
SAMPLE_RESUME = {
    "personal_info": {
        "name": "Alex Johnson",
        "email": "alex.johnson@email.com",
        "phone": "+1 (555) 123-4567",
        "location": "San Francisco, CA",
        "linkedin": "https://linkedin.com/in/alexjohnson",
        "github": "https://github.com/alexjohnson",
        "website": "https://alexjohnson.dev"
    },
    "summary": "Full-stack software engineer with 5+ years of experience building scalable web applications. Specialized in React, Python, and cloud technologies. Passionate about creating user-centric solutions and mentoring junior developers.",
    "experience": [
        {
            "position": "Senior Software Engineer",
            "company": "TechCorp Inc.",
            "location": "San Francisco, CA",
            "start_date": "Jan 2021",
            "end_date": "Present",
            "current": True,
            "description": [
                "Led development of microservices architecture serving 1M+ daily active users",
                "Reduced API response time by 40% through optimization and caching strategies",
                "Mentored team of 5 junior engineers, improving code quality and development speed",
                "Implemented CI/CD pipeline reducing deployment time from 2 hours to 15 minutes"
            ],
            "achievements": [
                "Received 'Outstanding Performance' award Q3 2023",
                "Open-sourced internal tool with 500+ GitHub stars"
            ]
        },
        {
            "position": "Software Engineer",
            "company": "StartupXYZ",
            "location": "Palo Alto, CA",
            "start_date": "Jun 2019",
            "end_date": "Dec 2020",
            "current": False,
            "description": [
                "Built real-time chat application using WebSocket and React",
                "Developed RESTful APIs in Python/Django serving 50K+ requests per hour",
                "Collaborated with design team to implement pixel-perfect UI components",
                "Participated in code reviews and improved team coding standards"
            ]
        },
        {
            "position": "Software Engineering Intern",
            "company": "BigTech Corp",
            "location": "Mountain View, CA",
            "start_date": "Jun 2018",
            "end_date": "Aug 2018",
            "current": False,
            "description": [
                "Developed internal dashboard using React and D3.js for data visualization",
                "Automated testing processes, increasing test coverage from 60% to 85%",
                "Presented final project to 50+ engineers and product managers"
            ]
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "institution": "Stanford University",
            "location": "Stanford, CA",
            "graduation_date": "May 2019",
            "start_date": "Sep 2015",
            "end_date": "May 2019",
            "gpa": "3.85/4.0",
            "description": "Relevant Coursework: Algorithms, Machine Learning, Web Development, Database Systems"
        },
        {
            "degree": "High School Diploma",
            "institution": "Lincoln High School",
            "location": "San Jose, CA",
            "graduation_date": "Jun 2015",
            "gpa": "4.0/4.0"
        }
    ],
    "skills": [
        {
            "category": "Languages",
            "items": ["Python", "JavaScript", "TypeScript", "Go", "SQL", "HTML/CSS"]
        },
        {
            "category": "Frameworks & Libraries",
            "items": ["React", "Node.js", "FastAPI", "Django", "Flask", "Next.js", "TailwindCSS"]
        },
        {
            "category": "Tools & Technologies",
            "items": ["Git", "Docker", "Kubernetes", "AWS", "PostgreSQL", "MongoDB", "Redis"]
        },
        {
            "category": "Methodologies",
            "items": ["Agile/Scrum", "CI/CD", "Test-Driven Development", "Microservices", "RESTful APIs"]
        }
    ],
    "projects": [
        {
            "name": "ResumeAI - AI-Powered Resume Builder",
            "description": "Built full-stack application with React frontend and FastAPI backend. Integrated OpenAI GPT for resume optimization. Deployed on AWS with Docker/Kubernetes. 10K+ users in first month.",
            "technologies": ["React", "FastAPI", "OpenAI", "Docker", "AWS", "PostgreSQL"],
            "url": "https://github.com/alexjohnson/resumeai"
        },
        {
            "name": "Task Manager Pro",
            "description": "Developed collaborative task management tool with real-time updates using WebSocket. Implemented drag-and-drop interface and notification system. Used by 3 startups.",
            "technologies": ["React", "Node.js", "Socket.io", "MongoDB"],
            "url": "https://github.com/alexjohnson/taskmanager"
        },
        {
            "name": "ML Price Predictor",
            "description": "Created machine learning model to predict housing prices with 92% accuracy. Built web interface for predictions. Dataset of 50K+ properties.",
            "technologies": ["Python", "Scikit-learn", "Flask", "Pandas"],
            "url": "https://github.com/alexjohnson/ml-predictor"
        }
    ],
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect - Associate",
            "issuer": "Amazon Web Services",
            "date": "2023"
        },
        {
            "name": "Google Cloud Professional Developer",
            "issuer": "Google Cloud",
            "date": "2022"
        },
        {
            "name": "MongoDB Certified Developer",
            "issuer": "MongoDB Inc.",
            "date": "2021"
        }
    ],
    "awards": [
        "Hackathon Winner - TechConf 2022 (1st place out of 200 teams)",
        "Dean's List - All semesters at Stanford University",
        "National Merit Scholar - 2015"
    ],
    "languages": [
        "English (Native)",
        "Spanish (Professional working proficiency)",
        "Mandarin (Elementary proficiency)"
    ]
}

# Minimal resume for testing edge cases
MINIMAL_RESUME = {
    "personal_info": {
        "name": "Jane Smith",
        "email": "jane@email.com"
    },
    "skills": ["Python", "JavaScript"],
    "experience": [],
    "education": []
}

# Creative role resume
CREATIVE_RESUME = {
    "personal_info": {
        "name": "Maria Garcia",
        "email": "maria@creative.studio",
        "phone": "+1-555-987-6543",
        "location": "Los Angeles, CA",
        "website": "https://mariagarcia.design"
    },
    "summary": "Award-winning UX/UI designer with 7 years of experience creating delightful digital experiences. Specialized in user research, interaction design, and design systems. Passionate about accessibility and inclusive design.",
    "experience": [
        {
            "position": "Lead UX Designer",
            "company": "Creative Agency",
            "start_date": "2020",
            "end_date": "Present",
            "current": True,
            "description": [
                "Led design for Fortune 500 clients resulting in 150% increase in user engagement",
                "Established design system used across 20+ products",
                "Conducted user research with 500+ participants across 5 countries",
                "Mentored team of 8 designers and fostered collaborative culture"
            ]
        }
    ],
    "skills": [
        {"category": "Design Tools", "items": ["Figma", "Adobe XD", "Sketch", "Photoshop", "Illustrator"]},
        {"category": "Skills", "items": ["User Research", "Wireframing", "Prototyping", "Usability Testing", "Design Systems"]}
    ],
    "projects": [
        {
            "name": "Mobile Banking Redesign",
            "description": "Complete redesign of banking app used by 2M+ customers. Improved task completion rate by 60% and reduced support tickets by 40%.",
            "technologies": ["Figma", "User Research", "A/B Testing"]
        }
    ],
    "education": [
        {
            "degree": "Master of Fine Arts",
            "field_of_study": "Interaction Design",
            "institution": "Rhode Island School of Design",
            "graduation_date": "2016"
        }
    ],
    "certifications": [
        {"name": "Google UX Design Professional Certificate", "issuer": "Google", "date": "2021"}
    ],
    "awards": [
        "Webby Awards - Best User Experience (2023)",
        "CSS Design Awards - Website of the Year (2022)"
    ]
}

# Academic/Research resume
ACADEMIC_RESUME = {
    "personal_info": {
        "name": "Dr. Robert Chen",
        "email": "r.chen@university.edu",
        "phone": "+1-555-246-8135",
        "location": "Cambridge, MA"
    },
    "summary": "Computer Science researcher with focus on machine learning and natural language processing. Published 15+ peer-reviewed papers with 500+ citations. Seeking tenure-track position in top-tier research university.",
    "education": [
        {
            "degree": "Ph.D.",
            "field_of_study": "Computer Science",
            "institution": "MIT",
            "graduation_date": "2021",
            "gpa": "4.0/4.0",
            "description": "Dissertation: 'Neural Approaches to Semantic Understanding in Large Language Models'"
        },
        {
            "degree": "M.S.",
            "field_of_study": "Computer Science",
            "institution": "Stanford University",
            "graduation_date": "2017",
            "gpa": "3.95/4.0"
        },
        {
            "degree": "B.S.",
            "field_of_study": "Mathematics & Computer Science",
            "institution": "UC Berkeley",
            "graduation_date": "2015",
            "gpa": "3.92/4.0"
        }
    ],
    "experience": [
        {
            "position": "Postdoctoral Researcher",
            "company": "MIT Computer Science & AI Lab",
            "start_date": "2021",
            "end_date": "Present",
            "current": True,
            "description": [
                "Leading research project on interpretable machine learning funded by NSF grant ($500K)",
                "Published 5 papers in top-tier conferences (NeurIPS, ICML, ACL)",
                "Mentoring 3 PhD students and 2 undergraduate researchers",
                "Teaching assistant for graduate-level ML course (50+ students)"
            ]
        }
    ],
    "publications": [
        {
            "title": "Attention Is All You Need (Improved)",
            "authors": "Chen, R., Smith, J., Johnson, A.",
            "venue": "NeurIPS 2023",
            "year": "2023"
        }
    ],
    "skills": [
        {"category": "Research Areas", "items": ["Machine Learning", "NLP", "Deep Learning", "Interpretability"]},
        {"category": "Programming", "items": ["Python", "PyTorch", "TensorFlow", "R", "MATLAB"]}
    ],
    "awards": [
        "Best Paper Award - NeurIPS 2023",
        "NSF Graduate Research Fellowship - 2017-2020",
        "Outstanding Graduate Student Award - MIT (2021)"
    ],
    "certifications": []
}


def get_sample_resume(resume_type="full"):
    """
    Get sample resume data for testing
    
    Args:
        resume_type: One of 'full', 'minimal', 'creative', 'academic'
    
    Returns:
        dict: Resume data
    """
    resumes = {
        'full': SAMPLE_RESUME,
        'minimal': MINIMAL_RESUME,
        'creative': CREATIVE_RESUME,
        'academic': ACADEMIC_RESUME
    }
    return resumes.get(resume_type, SAMPLE_RESUME)
