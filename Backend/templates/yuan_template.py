"""Yuan's Resume Template - Minimalist, Elegant, Sophisticated"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class YuanTemplate(BaseTemplate):
    """
    Yuan's Resume Template
    Features:
    - Minimalist design philosophy
    - Elegant typography
    - Sophisticated color accents
    - Whitespace optimization
    - Modern professional aesthetic
    """
    
    def _get_margins(self):
        """Generous margins for elegance"""
        return (0.8, 0.8, 0.8, 0.8)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header - Minimalist elegance
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], styles['name']))
        
        # Tagline or title if in summary
        if resume_data.get('summary'):
            summary = resume_data.get('summary', '')
            # Use first sentence as tagline if short
            if len(summary) < 100:
                elements.append(Paragraph(summary, styles['tagline']))
        
        # Contact - Elegant layout
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        
        if contact_parts:
            elements.append(Paragraph(' • '.join(contact_parts), styles['contact']))
        
        # Links
        if personal_info.get('linkedin') or personal_info.get('github') or personal_info.get('website'):
            links = []
            if personal_info.get('website'):
                links.append(personal_info['website'].replace('https://', '').replace('http://', ''))
            if personal_info.get('linkedin'):
                links.append(f"LinkedIn: {personal_info['linkedin'].split('/')[-1]}")
            if personal_info.get('github'):
                links.append(f"GitHub: {personal_info['github'].split('/')[-1]}")
            
            elements.append(Paragraph(' • '.join(links), styles['links']))
        
        # Elegant divider
        elements.append(HRFlowable(width="40%", thickness=0.5, color=colors.HexColor(self.theme_color), 
                                  spaceAfter=12, spaceBefore=8, hAlign='CENTER'))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('Experience', styles['section']))
            elements.append(Spacer(1, 0.05*inch))
            
            for exp in resume_data['experience']:
                # Position - Prominent
                elements.append(Paragraph(exp.get('position', 'Position'), styles['role']))
                
                # Company and dates - Subtle
                company = exp.get('company', 'Company')
                date_range = f"{exp.get('start_date', '')}–{exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                company_date = Table([
                    [Paragraph(company, styles['company']),
                     Paragraph(date_range, styles['date'])]
                ], colWidths=[4.5*inch, 1.5*inch])
                company_date.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(company_date)
                
                elements.append(Spacer(1, 0.04*inch))
                
                # Achievements - Clean presentation
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"— {item}", styles['achievement']))
                    else:
                        elements.append(Paragraph(f"— {description}", styles['achievement']))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"— {achievement}", styles['achievement']))
                
                elements.append(Spacer(1, 0.12*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('Education', styles['section']))
            elements.append(Spacer(1, 0.05*inch))
            
            for edu in resume_data['education']:
                # Degree and Field
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = edu.get('degree', 'Degree')
                if field:
                    degree_text += f" in {field}"
                
                elements.append(Paragraph(degree_text, styles['role']))
                
                # Institution and date
                institution = edu.get('institution', 'Institution')
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')}–{edu.get('end_date', '')}"
                    if date_range.strip() != '–':
                        date_text = date_range
                
                edu_info = Table([
                    [Paragraph(institution, styles['company']),
                     Paragraph(date_text, styles['date'])]
                ], colWidths=[4.5*inch, 1.5*inch])
                edu_info.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(edu_info)
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['detail']))
                
                elements.append(Spacer(1, 0.12*inch))
        
        # Skills - Elegant presentation
        if resume_data.get('skills'):
            elements.append(Paragraph('Expertise', styles['section']))
            elements.append(Spacer(1, 0.05*inch))
            
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        # Elegant skill boxes
                        skill_header = Paragraph(category, styles['skill_category'])
                        elements.append(skill_header)
                        
                        skill_box = Table([[Paragraph(', '.join(items), styles['skill_items'])]], 
                                        colWidths=[6*inch])
                        skill_box.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
                            ('LEFTPADDING', (0, 0), (-1, -1), 12),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                            ('TOPPADDING', (0, 0), (-1, -1), 6),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        elements.append(skill_box)
                        elements.append(Spacer(1, 0.06*inch))
            else:
                elements.append(Paragraph(', '.join(skills), styles['detail']))
            
            elements.append(Spacer(1, 0.08*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('Selected Projects', styles['section']))
            elements.append(Spacer(1, 0.05*inch))
            
            for proj in resume_data['projects']:
                proj_name = proj.get('name', 'Project')
                elements.append(Paragraph(proj_name, styles['role']))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], styles['detail']))
                
                if proj.get('technologies'):
                    tech_text = ', '.join(proj['technologies'])
                    elements.append(Paragraph(tech_text, styles['tech_stack']))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Certifications & Awards
        if resume_data.get('certifications') or resume_data.get('awards'):
            elements.append(Paragraph('Recognitions', styles['section']))
            elements.append(Spacer(1, 0.05*inch))
            
            if resume_data.get('awards'):
                for award in resume_data['awards']:
                    elements.append(Paragraph(f"— {award}", styles['achievement']))
            
            if resume_data.get('certifications'):
                for cert in resume_data['certifications']:
                    cert_text = f"— {cert.get('name', 'Certification')}"
                    if cert.get('issuer'):
                        cert_text += f", {cert['issuer']}"
                    if cert.get('date'):
                        cert_text += f" ({cert['date']})"
                    elements.append(Paragraph(cert_text, styles['achievement']))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create Yuan template styles - minimalist and elegant"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=4,
            leading=28,
        )
        
        styles['tagline'] = ParagraphStyle(
            'Tagline',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=2,
        )
        
        styles['links'] = ParagraphStyle(
            'Links',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor(self.theme_color),
            alignment=TA_CENTER,
            spaceAfter=4,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=4,
            spaceBefore=12,
            leading=16,
        )
        
        styles['role'] = ParagraphStyle(
            'Role',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=2,
        )
        
        styles['company'] = ParagraphStyle(
            'Company',
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=2,
        )
        
        styles['date'] = ParagraphStyle(
            'Date',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT,
        )
        
        styles['achievement'] = ParagraphStyle(
            'Achievement',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#2a2a2a'),
            spaceAfter=3,
            leading=12,
            leftIndent=8,
        )
        
        styles['detail'] = ParagraphStyle(
            'Detail',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=3,
            leading=11,
        )
        
        styles['skill_category'] = ParagraphStyle(
            'SkillCategory',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=3,
        )
        
        styles['skill_items'] = ParagraphStyle(
            'SkillItems',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#2a2a2a'),
        )
        
        styles['tech_stack'] = ParagraphStyle(
            'TechStack',
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=3,
        )
        
        return styles
