from typing import Dict, Any, List, Tuple
import re


class ATSScorer:
    """ATS (Applicant Tracking System) compatibility scorer"""
    
    # Common ATS-friendly keywords by category
    TECHNICAL_KEYWORDS = [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker',
        'kubernetes', 'git', 'agile', 'scrum', 'ci/cd', 'api', 'rest', 'microservices'
    ]
    
    SOFT_SKILLS = [
        'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
        'project management', 'collaboration', 'time management', 'adaptability'
    ]
    
    ACTION_VERBS = [
        'achieved', 'improved', 'developed', 'created', 'managed', 'led', 'implemented',
        'designed', 'optimized', 'increased', 'reduced', 'launched', 'built', 'established'
    ]
    
    def __init__(self, resume_data: Dict[str, Any]):
        self.resume_data = resume_data
        self.score = 0
        self.feedback = []
        self.missing_keywords = []
        self.improvements = []
    
    def calculate_score(self) -> Tuple[int, List[str], List[str], List[str]]:
        """Calculate overall ATS score"""
        
        # Check for essential sections (40 points)
        self._check_essential_sections()
        
        # Check formatting (20 points)
        self._check_formatting()
        
        # Check keywords and relevance (20 points)
        self._check_keywords()
        
        # Check for quantifiable achievements (10 points)
        self._check_achievements()
        
        # Check contact information (10 points)
        self._check_contact_info()
        
        return self.score, self.feedback, self.missing_keywords, self.improvements
    
    def _check_essential_sections(self):
        """Check for essential resume sections"""
        sections = {
            'experience': 15,
            'education': 10,
            'skills': 10,
            'personal_info': 5
        }
        
        for section, points in sections.items():
            data = self.resume_data.get(section, [])
            if data:
                self.score += points
                self.feedback.append(f"✓ {section.capitalize()} section present")
            else:
                self.feedback.append(f"✗ Missing {section.capitalize()} section")
                self.improvements.append(f"Add {section.capitalize()} section")
    
    def _check_formatting(self):
        """Check for ATS-friendly formatting"""
        points = 0
        
        # Check for bullet points in experience
        experience = self.resume_data.get('experience', [])
        if experience and any(exp.get('achievements') for exp in experience):
            points += 5
            self.feedback.append("✓ Uses bullet points for achievements")
        else:
            self.improvements.append("Use bullet points to list achievements")
        
        # Check for date formats
        if experience and any(exp.get('start_date') for exp in experience):
            points += 5
            self.feedback.append("✓ Includes dates for experience")
        else:
            self.improvements.append("Add dates to your experience entries")
        
        # Check for clear job titles
        if experience and all(exp.get('position') and exp.get('company') for exp in experience):
            points += 5
            self.feedback.append("✓ Clear job titles and companies")
        
        # Check summary or objective
        if self.resume_data.get('summary') or self.resume_data.get('objective'):
            points += 5
            self.feedback.append("✓ Includes professional summary/objective")
        else:
            self.improvements.append("Add a professional summary at the top")
        
        self.score += points
    
    def _check_keywords(self):
        """Check for relevant keywords"""
        points = 0
        
        # Get all text content
        all_text = self._get_all_text().lower()
        
        # Check technical keywords
        found_technical = [kw for kw in self.TECHNICAL_KEYWORDS if kw.lower() in all_text]
        if len(found_technical) >= 5:
            points += 7
            self.feedback.append(f"✓ Contains {len(found_technical)} technical keywords")
        else:
            self.missing_keywords.extend([kw for kw in self.TECHNICAL_KEYWORDS[:10] if kw not in found_technical])
            self.improvements.append("Include more relevant technical keywords")
        
        # Check soft skills
        found_soft = [kw for kw in self.SOFT_SKILLS if kw.lower() in all_text]
        if len(found_soft) >= 3:
            points += 7
            self.feedback.append(f"✓ Contains {len(found_soft)} soft skills")
        else:
            self.improvements.append("Add more soft skills (leadership, communication, etc.)")
        
        # Check action verbs
        found_verbs = [verb for verb in self.ACTION_VERBS if verb.lower() in all_text]
        if len(found_verbs) >= 5:
            points += 6
            self.feedback.append(f"✓ Uses {len(found_verbs)} strong action verbs")
        else:
            self.improvements.append("Use more action verbs (achieved, improved, developed, etc.)")
        
        self.score += points
    
    def _check_achievements(self):
        """Check for quantifiable achievements"""
        points = 0
        
        # Look for numbers/percentages in achievements
        experience = self.resume_data.get('experience', [])
        has_numbers = False
        
        for exp in experience:
            achievements = exp.get('achievements', [])
            for achievement in achievements:
                if re.search(r'\d+[%$]?|\$\d+', achievement):
                    has_numbers = True
                    break
            if has_numbers:
                break
        
        if has_numbers:
            points += 10
            self.feedback.append("✓ Includes quantifiable achievements with numbers")
        else:
            self.improvements.append("Add numbers and metrics to quantify your achievements (e.g., 'Increased sales by 25%')")
        
        self.score += points
    
    def _check_contact_info(self):
        """Check for complete contact information"""
        points = 0
        personal_info = self.resume_data.get('personal_info', {})
        
        required_fields = ['name', 'email', 'phone']
        missing = [field for field in required_fields if not personal_info.get(field)]
        
        if not missing:
            points += 5
            self.feedback.append("✓ Complete contact information")
        else:
            self.improvements.append(f"Add missing contact info: {', '.join(missing)}")
        
        # Bonus for professional links
        if personal_info.get('linkedin') or personal_info.get('github'):
            points += 5
            self.feedback.append("✓ Includes professional profile links")
        else:
            self.improvements.append("Add LinkedIn or GitHub profile link")
        
        self.score += points
    
    def _get_all_text(self) -> str:
        """Extract all text from resume data"""
        text_parts = []
        
        # Skills
        text_parts.extend(self.resume_data.get('skills', []))
        
        # Experience
        for exp in self.resume_data.get('experience', []):
            text_parts.append(exp.get('position', ''))
            text_parts.append(exp.get('company', ''))
            text_parts.append(exp.get('description', ''))
            text_parts.extend(exp.get('achievements', []))
        
        # Education
        for edu in self.resume_data.get('education', []):
            text_parts.append(edu.get('degree', ''))
            text_parts.append(edu.get('field_of_study', ''))
            text_parts.append(edu.get('description', ''))
        
        # Summary/Objective
        text_parts.append(self.resume_data.get('summary', ''))
        text_parts.append(self.resume_data.get('objective', ''))
        
        return ' '.join(text_parts)


def calculate_ats_score(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main function to calculate ATS score"""
    scorer = ATSScorer(resume_data)
    score, feedback, missing_keywords, improvements = scorer.calculate_score()
    
    return {
        'score': min(score, 100),  # Cap at 100
        'feedback': '\n'.join(feedback),
        'missing_keywords': missing_keywords[:10],  # Top 10
        'improvements': improvements
    }
