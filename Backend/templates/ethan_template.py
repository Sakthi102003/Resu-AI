"""Ethan's Resume Template - Clean, Professional, Two-Column Layout"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class EthanTemplate(BaseTemplate):
    """
    Ethan's Resume Template
    Features:
    - Clean, professional design
    - Two-column layout for better space utilization
    - Modern typography
    - Clear visual hierarchy
    """
    
    def _get_margins(self):
        """Narrow margins for two-column layout"""
        return (0.5, 0.5, 0.6, 0.6)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header Section
        personal_info = resume_data.get('personal_info', {})
        
        # Name - Prominent
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], styles['name']))
        
        # Contact info in columns
        contact_data = []
        left_contact = []
        right_contact = []
        
        if personal_info.get('phone'):
            left_contact.append(f"☎ {personal_info['phone']}")
        if personal_info.get('email'):
            left_contact.append(f"✉ {personal_info['email']}")
        
        if personal_info.get('linkedin'):
            right_contact.append(f"in/ {personal_info['linkedin'].split('/')[-1]}")
        if personal_info.get('github'):
            right_contact.append(f"github/ {personal_info['github'].split('/')[-1]}")
        if personal_info.get('location'):
            right_contact.append(f"📍 {personal_info['location']}")
        
        if left_contact or right_contact:
            left_str = '<br/>'.join(left_contact) if left_contact else ''
            right_str = '<br/>'.join(right_contact) if right_contact else ''
            
            contact_table = Table([
                [Paragraph(left_str, styles['contact_left']), 
                 Paragraph(right_str, styles['contact_right'])]
            ], colWidths=[3.5*inch, 3.5*inch])
            contact_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            elements.append(contact_table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Summary
        if resume_data.get('summary') or resume_data.get('objective'):
            elements.append(Paragraph('SUMMARY', styles['section']))
            summary = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary, styles['body']))
            elements.append(Spacer(1, 0.12*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('EXPERIENCE', styles['section']))
            
            for exp in resume_data['experience']:
                # Company and dates
                company = exp.get('company', 'Company')
                position = exp.get('position', 'Position')
                date_range = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                # Create table for alignment
                exp_header = Table([
                    [Paragraph(f"<b>{company}</b>", styles['company']),
                     Paragraph(date_range, styles['date'])]
                ], colWidths=[5*inch, 2*inch])
                exp_header.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_header)
                
                # Position
                elements.append(Paragraph(f"<i>{position}</i>", styles['position']))
                
                # Responsibilities
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
                institution = edu.get('institution', 'Institution')
                field = edu.get('field_of_study') or edu.get('field', '')
                degree = edu.get('degree', 'Degree')
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                # Institution and date
                edu_header = Table([
                    [Paragraph(f"<b>{institution}</b>", styles['company']),
                     Paragraph(date_text, styles['date'])]
                ], colWidths=[5*inch, 2*inch])
                edu_header.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(edu_header)
                
                # Degree
                degree_text = f"<i>{degree}"
                if field:
                    degree_text += f" in {field}"
                degree_text += "</i>"
                elements.append(Paragraph(degree_text, styles['position']))
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['body']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Skills
        if resume_data.get('skills'):
            elements.append(Paragraph('SKILLS', styles['section']))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                skill_table_data = []
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skill_table_data.append([
                            Paragraph(f"<b>{category}:</b>", styles['skill_cat']),
                            Paragraph(', '.join(items), styles['body'])
                        ])
                
                if skill_table_data:
                    skill_table = Table(skill_table_data, colWidths=[1.5*inch, 5.5*inch])
                    skill_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ]))
                    elements.append(skill_table)
            else:
                elements.append(Paragraph(', '.join(skills), styles['body']))
            
            elements.append(Spacer(1, 0.08*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', styles['section']))
            
            for proj in resume_data['projects']:
                proj_name = proj.get('name', 'Project')
                elements.append(Paragraph(f"<b>{proj_name}</b>", styles['company']))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], styles['body']))
                
                if proj.get('technologies'):
                    tech_text = f"<i>Tech Stack:</i> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, styles['tech']))
                
                elements.append(Spacer(1, 0.06*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', styles['section']))
            
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b> - {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" | {cert['date']}"
                elements.append(Paragraph(cert_text, styles['body']))
            
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create Ethan template specific styles"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
        
        styles['contact_left'] = ParagraphStyle(
            'ContactLeft',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
        
        styles['contact_right'] = ParagraphStyle(
            'ContactRight',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT,
            spaceAfter=4,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=6,
            spaceBefore=8,
            borderWidth=0,
            borderPadding=(0, 0, 1, 0),
        )
        
        styles['company'] = ParagraphStyle(
            'Company',
            fontName='Helvetica-Bold',
            fontSize=10,
            spaceAfter=2,
        )
        
        styles['position'] = ParagraphStyle(
            'Position',
            fontName='Helvetica-Oblique',
            fontSize=10,
            spaceAfter=3,
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
            spaceAfter=2,
            leading=11,
            leftIndent=12,
        )
        
        styles['skill_cat'] = ParagraphStyle(
            'SkillCat',
            fontName='Helvetica-Bold',
            fontSize=9,
        )
        
        styles['tech'] = ParagraphStyle(
            'Tech',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=3,
        )
        
        return styles
