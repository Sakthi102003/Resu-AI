"""Auto CV Template - Modern, Automated, ATS-Friendly"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class AutoCVTemplate(BaseTemplate):
    """
    Auto CV Template - Modern and ATS-optimized
    Features:
    - Clean, professional layout
    - ATS-friendly formatting
    - Automatic section ordering
    - Skills-first approach
    """
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'].upper(), styles['name']))
        
        # Contact - One line
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'].replace('https://', ''))
        
        if contact_parts:
            elements.append(Paragraph(' • '.join(contact_parts), styles['contact']))
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Professional Summary
        if resume_data.get('summary') or resume_data.get('objective'):
            elements.append(Paragraph('PROFESSIONAL SUMMARY', styles['section']))
            summary = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary, styles['body']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Skills - Prominently displayed
        if resume_data.get('skills'):
            elements.append(Paragraph('CORE COMPETENCIES', styles['section']))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skill_text = f"<b>{category}:</b> {', '.join(items)}"
                        elements.append(Paragraph(skill_text, styles['body']))
            else:
                elements.append(Paragraph(', '.join(skills), styles['body']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        # Professional Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('PROFESSIONAL EXPERIENCE', styles['section']))
            
            for exp in resume_data['experience']:
                # Position and Company
                title = f"<b>{exp.get('position', 'Position')}</b> | {exp.get('company', 'Company')}"
                date_range = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                title_cell = Paragraph(title, styles['item_title'])
                date_cell = Paragraph(date_range, styles['date'])
                
                exp_table = Table([[title_cell, date_cell]], colWidths=[5*inch, 1.5*inch])
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_table)
                
                # Achievements
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
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', styles['section']))
            
            for edu in resume_data['education']:
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = f"<b>{edu.get('degree', 'Degree')}</b>"
                if field:
                    degree_text += f" in {field}"
                degree_text += f" | {edu.get('institution', 'Institution')}"
                
                degree_cell = Paragraph(degree_text, styles['item_title'])
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                if date_text:
                    date_cell = Paragraph(date_text, styles['date'])
                    edu_table = Table([[degree_cell, date_cell]], colWidths=[5*inch, 1.5*inch])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_table)
                else:
                    elements.append(degree_cell)
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['body']))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', styles['section']))
            
            for proj in resume_data['projects']:
                proj_title = f"<b>{proj.get('name', 'Project')}</b>"
                elements.append(Paragraph(proj_title, styles['item_title']))
                
                if proj.get('description'):
                    elements.append(Paragraph(f"• {proj['description']}", styles['bullet']))
                
                if proj.get('technologies'):
                    tech_text = f"<i>Technologies:</i> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, styles['body']))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', styles['section']))
            
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b> - {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                elements.append(Paragraph(cert_text, styles['body']))
            
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create Auto CV specific styles"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.HexColor(self.theme_color),
            alignment=TA_CENTER,
            spaceAfter=4,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=6,
            spaceBefore=10,
            borderWidth=0,
            borderPadding=(0, 0, 2, 0),
            borderColor=colors.HexColor(self.theme_color),
        )
        
        styles['item_title'] = ParagraphStyle(
            'ItemTitle',
            fontName='Helvetica-Bold',
            fontSize=10,
            spaceAfter=2,
        )
        
        styles['date'] = ParagraphStyle(
            'Date',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT,
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
            spaceAfter=3,
            leading=11,
            leftIndent=12,
        )
        
        return styles
