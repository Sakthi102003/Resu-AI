"""Resume parser - extracts data from PDF/DOCX files"""
from typing import Dict, Any, List
import re


def extract_email(text: str) -> str:
    """Extract email from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    phone_patterns = [
        r'\+?1?\s*\(?([0-9]{3})\)?[\s.-]?([0-9]{3})[\s.-]?([0-9]{4})',
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ""


def extract_urls(text: str) -> Dict[str, str]:
    """Extract LinkedIn, GitHub, and portfolio URLs"""
    urls = {
        'linkedin': '',
        'github': '',
        'portfolio': ''
    }
    
    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if match:
        urls['linkedin'] = f"https://{match.group(0)}"
    
    # GitHub
    github_pattern = r'github\.com/[\w-]+'
    match = re.search(github_pattern, text, re.IGNORECASE)
    if match:
        urls['github'] = f"https://{match.group(0)}"
    
    return urls


def extract_skills(text: str) -> List[str]:
    """Extract skills from text using common patterns"""
    common_skills = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
        'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD',
        'Git', 'GitHub', 'GitLab', 'Jira', 'Agile', 'Scrum',
        'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'NLP',
        'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills


def parse_resume_text(text: str) -> Dict[str, Any]:
    """Parse resume text and extract structured data"""
    
    # Extract personal info
    personal_info = {
        'name': '',  # Would need more sophisticated NER for names
        'email': extract_email(text),
        'phone': extract_phone(text),
        'location': '',
    }
    
    # Extract URLs
    urls = extract_urls(text)
    personal_info.update(urls)
    
    # Extract skills
    skills = extract_skills(text)
    
    # Basic structure (would need more sophisticated parsing for real use)
    resume_data = {
        'personal_info': personal_info,
        'objective': '',
        'summary': '',
        'experience': [],
        'education': [],
        'skills': skills,
        'projects': [],
        'certifications': [],
        'languages': [],
        'awards': []
    }
    
    return resume_data


def parse_pdf_resume(file_path: str) -> Dict[str, Any]:
    """Parse PDF resume file"""
    try:
        from pypdf import PdfReader
        
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return parse_resume_text(text)
    except Exception as e:
        return {
            'error': f"Failed to parse PDF: {str(e)}",
            'personal_info': {},
            'skills': []
        }


def parse_docx_resume(file_path: str) -> Dict[str, Any]:
    """Parse DOCX resume file"""
    try:
        from docx import Document
        
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return parse_resume_text(text)
    except Exception as e:
        return {
            'error': f"Failed to parse DOCX: {str(e)}",
            'personal_info': {},
            'skills': []
        }
