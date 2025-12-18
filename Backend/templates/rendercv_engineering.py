"""RenderCV EngineeringResume Theme - Technical, Data-Driven, Results-Focused"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class RenderCVEngineeringTemplate(BaseTemplate):
    """
    RenderCV EngineeringResume Theme
    Features:
    - Technical and quantitative focus
    - Metrics-driven accomplishments
    - Skills-first approach
    - Clean, scannable layout
    - Optimal for engineering and technical roles
    """
    
    def _get_margins(self):
        """Balanced margins"""
        return (0.6, 0.6, 0.7, 0.7)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'].upper(), styles['name']))
        
        # Contact - Single line
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'].split('/')[-1])
        if personal_info.get('github'):
            contact_parts.append(f"github.com/{personal_info['github'].split('/')[-1]}")
        
        if contact_parts:
            elements.append(Paragraph(' | '.join(contact_parts), styles['contact']))
        
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(self.theme_color), 
                                  spaceAfter=10, spaceBefore=6))
        
        # Technical Skills - FIRST for engineering
        if resume_data.get('skills'):
            elements.append(Paragraph('TECHNICAL SKILLS', styles['section']))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                # Create table for clean layout
                skill_data = []
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skill_data.append([
                            Paragraph(f"<b>{category}</b>", styles['skill_cat']),
                            Paragraph(', '.join(items), styles['skill_items'])
                        ])
                
                if skill_data:
                    skill_table = Table(skill_data, colWidths=[1.3*inch, 5.2*inch])
                    skill_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    elements.append(skill_table)
            else:
                elements.append(Paragraph(', '.join(skills), styles['body']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        # Professional Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('PROFESSIONAL EXPERIENCE', styles['section']))
            
            for exp in resume_data['experience']:
                # Company and Position
                company_position = f"<b>{exp.get('company', 'Company')}</b> — {exp.get('position', 'Position')}"
                date_range = f"{exp.get('start_date', '')} – {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                exp_header = Table([
                    [Paragraph(company_position, styles['exp_title']),
                     Paragraph(date_range, styles['date'])]
                ], colWidths=[4.8*inch, 1.7*inch])
                exp_header.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_header)
                
                # Location if available
                if exp.get('location'):
                    elements.append(Paragraph(f"<i>{exp['location']}</i>", styles['location']))
                
                # Achievements - Engineering focus on metrics
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"• {item}", styles['bullet']))
                    else:
                        elements.append(Paragraph(f"• {description}", styles['bullet']))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", styles['bullet']))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', styles['section']))
            
            for proj in resume_data['projects']:
                proj_name = proj.get('name', 'Project')
                
                # Project name with tech stack
                if proj.get('technologies'):
                    proj_header = f"<b>{proj_name}</b> | <i>{', '.join(proj['technologies'])}</i>"
                else:
                    proj_header = f"<b>{proj_name}</b>"
                
                elements.append(Paragraph(proj_header, styles['proj_title']))
                
                if proj.get('description'):
                    elements.append(Paragraph(f"• {proj['description']}", styles['bullet']))
                
                if proj.get('url'):
                    elements.append(Paragraph(f"URL: {proj['url']}", styles['url']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', styles['section']))
            
            for edu in resume_data['education']:
                institution = edu.get('institution', 'Institution')
                field = edu.get('field_of_study') or edu.get('field', '')
                degree = edu.get('degree', 'Degree')
                
                degree_text = f"<b>{institution}</b> — {degree}"
                if field:
                    degree_text += f", {field}"
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} – {edu.get('end_date', '')}"
                    if date_range.strip() != '–':
                        date_text = date_range
                
                if date_text:
                    edu_header = Table([
                        [Paragraph(degree_text, styles['exp_title']),
                         Paragraph(date_text, styles['date'])]
                    ], colWidths=[4.8*inch, 1.7*inch])
                    edu_header.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_header)
                else:
                    elements.append(Paragraph(degree_text, styles['exp_title']))
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['body']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', styles['section']))
            
            cert_items = []
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b>"
                if cert.get('issuer'):
                    cert_text += f" — {cert['issuer']}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                cert_items.append(cert_text)
            
            for cert_text in cert_items:
                elements.append(Paragraph(cert_text, styles['body']))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create EngineeringResume theme styles"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor(self.theme_color),
            alignment=TA_LEFT,
            spaceAfter=3,
            leading=20,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=5,
            spaceBefore=8,
            textTransform='uppercase',
        )
        
        styles['exp_title'] = ParagraphStyle(
            'ExpTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            spaceAfter=1,
        )
        
        styles['date'] = ParagraphStyle(
            'Date',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT,
        )
        
        styles['location'] = ParagraphStyle(
            'Location',
            fontName='Helvetica-Oblique',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=3,
        )
        
        styles['body'] = ParagraphStyle(
            'Body',
            fontName='Helvetica',
            fontSize=9,
            spaceAfter=3,
            leading=11,
        )
        
        styles['bullet'] = ParagraphStyle(
            'Bullet',
            fontName='Helvetica',
            fontSize=9,
            spaceAfter=2,
            leading=11,
            leftIndent=12,
        )
        
        styles['skill_cat'] = ParagraphStyle(
            'SkillCat',
            fontName='Helvetica-Bold',
            fontSize=9,
        )
        
        styles['skill_items'] = ParagraphStyle(
            'SkillItems',
            fontName='Helvetica',
            fontSize=9,
        )
        
        styles['proj_title'] = ParagraphStyle(
            'ProjTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            spaceAfter=2,
        )
        
        styles['url'] = ParagraphStyle(
            'URL',
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#0000EE'),
            spaceAfter=2,
        )
        
        return styles
