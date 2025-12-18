"""Anti CV Template - Unconventional, Creative, Story-Driven"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class AntiCVTemplate(BaseTemplate):
    """
    Anti CV Template - Breaks traditional CV conventions
    Features:
    - Story-driven narrative format
    - Skills embedded in context
    - Achievements over duties
    - Personal voice and personality
    - Visual hierarchy without formality
    """
    
    def _get_margins(self):
        """Wider margins for creative look"""
        return (1.0, 1.0, 0.8, 0.8)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header - Creative approach
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(f"Hi, I'm {personal_info['name']}", styles['name']))
        
        # Contact in casual format
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(f"📧 {personal_info['email']}")
        if personal_info.get('phone'):
            contact_parts.append(f"📱 {personal_info['phone']}")
        if personal_info.get('location'):
            contact_parts.append(f"📍 {personal_info['location']}")
        
        if contact_parts:
            elements.append(Paragraph(' | '.join(contact_parts), styles['contact']))
        
        # Social links as icons
        links = []
        if personal_info.get('linkedin'):
            links.append(f"🔗 {personal_info['linkedin'].replace('https://', '')}")
        if personal_info.get('github'):
            links.append(f"💻 {personal_info['github'].replace('https://', '')}")
        
        if links:
            elements.append(Paragraph(' | '.join(links), styles['contact']))
        
        elements.append(Spacer(1, 0.15*inch))
        
        # About Me - Personal narrative
        if resume_data.get('summary') or resume_data.get('objective'):
            elements.append(Paragraph('About Me', styles['section']))
            summary = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary, styles['narrative']))
            elements.append(Spacer(1, 0.15*inch))
        
        # What I Do - Skills in context
        if resume_data.get('skills'):
            elements.append(Paragraph('What I Do', styles['section']))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        # Creative skill presentation
                        skill_box = Table([[Paragraph(f"<b>{category}</b>", styles['skill_header'])]], 
                                        colWidths=[5*inch])
                        skill_box.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0F4F8')),
                            ('LEFTPADDING', (0, 0), (-1, -1), 10),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                            ('TOPPADDING', (0, 0), (-1, -1), 6),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        elements.append(skill_box)
                        elements.append(Paragraph(', '.join(items), styles['skill_items']))
                        elements.append(Spacer(1, 0.08*inch))
            else:
                elements.append(Paragraph(', '.join(skills), styles['narrative']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        # My Journey - Experience as a story
        if resume_data.get('experience'):
            elements.append(Paragraph('My Journey', styles['section']))
            
            for idx, exp in enumerate(resume_data['experience']):
                # Story-style presentation
                date_range = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Now') if not exp.get('current') else 'Now'}"
                
                # Chapter-like format
                chapter = f"<b>Chapter {len(resume_data['experience']) - idx}:</b> {exp.get('position', 'Position')} @ {exp.get('company', 'Company')}"
                elements.append(Paragraph(chapter, styles['journey_title']))
                elements.append(Paragraph(f"<i>{date_range}</i>", styles['journey_date']))
                
                # The story
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        # Combine into narrative
                        story = ' • '.join([item for item in description if item])
                        elements.append(Paragraph(story, styles['narrative']))
                    else:
                        elements.append(Paragraph(description, styles['narrative']))
                
                if exp.get('achievements'):
                    elements.append(Paragraph('<b>Highlights:</b>', styles['highlight_header']))
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"✓ {achievement}", styles['highlight']))
                
                # Visual separator
                if idx < len(resume_data['experience']) - 1:
                    elements.append(HRFlowable(width="30%", thickness=0.5, color=colors.grey, 
                                             spaceAfter=10, spaceBefore=10, hAlign='CENTER'))
        
        # Projects - "Things I've Built"
        if resume_data.get('projects'):
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph('Things I\'ve Built', styles['section']))
            
            for proj in resume_data['projects']:
                proj_name = proj.get('name', 'Project')
                elements.append(Paragraph(f"🚀 <b>{proj_name}</b>", styles['project_title']))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], styles['narrative']))
                
                if proj.get('technologies'):
                    tech_text = f"Built with: {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, styles['tech_stack']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Education - "Where I Learned"
        if resume_data.get('education'):
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph('Where I Learned', styles['section']))
            
            for edu in resume_data['education']:
                field = edu.get('field_of_study') or edu.get('field', '')
                degree = edu.get('degree', 'Degree')
                institution = edu.get('institution', 'Institution')
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                edu_text = f"<b>{degree}</b> in {field}" if field else f"<b>{degree}</b>"
                elements.append(Paragraph(edu_text, styles['edu_title']))
                elements.append(Paragraph(f"{institution} | {date_text}", styles['edu_subtitle']))
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['narrative']))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Certifications - "Badges I've Earned"
        if resume_data.get('certifications'):
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph('Badges I\'ve Earned', styles['section']))
            
            for cert in resume_data['certifications']:
                cert_text = f"🏆 <b>{cert.get('name', 'Certification')}</b> from {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                elements.append(Paragraph(cert_text, styles['narrative']))
            
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create Anti CV specific styles - more creative"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor(self.theme_color),
            alignment=TA_LEFT,
            spaceAfter=6,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_LEFT,
            spaceAfter=3,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=8,
            spaceBefore=10,
        )
        
        styles['narrative'] = ParagraphStyle(
            'Narrative',
            fontName='Helvetica',
            fontSize=10,
            spaceAfter=6,
            leading=14,
            alignment=TA_JUSTIFY,
        )
        
        styles['journey_title'] = ParagraphStyle(
            'JourneyTitle',
            fontName='Helvetica-Bold',
            fontSize=11,
            spaceAfter=2,
        )
        
        styles['journey_date'] = ParagraphStyle(
            'JourneyDate',
            fontName='Helvetica-Oblique',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=6,
        )
        
        styles['highlight_header'] = ParagraphStyle(
            'HighlightHeader',
            fontName='Helvetica-Bold',
            fontSize=9,
            spaceAfter=3,
            spaceBefore=5,
        )
        
        styles['highlight'] = ParagraphStyle(
            'Highlight',
            fontName='Helvetica',
            fontSize=9,
            spaceAfter=3,
            leading=12,
            leftIndent=10,
        )
        
        styles['skill_header'] = ParagraphStyle(
            'SkillHeader',
            fontName='Helvetica-Bold',
            fontSize=10,
        )
        
        styles['skill_items'] = ParagraphStyle(
            'SkillItems',
            fontName='Helvetica',
            fontSize=9,
            spaceAfter=5,
            leftIndent=10,
        )
        
        styles['project_title'] = ParagraphStyle(
            'ProjectTitle',
            fontName='Helvetica-Bold',
            fontSize=11,
            spaceAfter=4,
        )
        
        styles['tech_stack'] = ParagraphStyle(
            'TechStack',
            fontName='Helvetica-Oblique',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=3,
        )
        
        styles['edu_title'] = ParagraphStyle(
            'EduTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            spaceAfter=2,
        )
        
        styles['edu_subtitle'] = ParagraphStyle(
            'EduSubtitle',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=4,
        )
        
        return styles
