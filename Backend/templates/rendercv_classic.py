"""RenderCV Classic Theme - Academic, Traditional, Elegant"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class RenderCVClassicTemplate(BaseTemplate):
    """
    RenderCV Classic Theme
    Features:
    - Traditional academic style
    - LaTeX-inspired formatting
    - Serif fonts
    - Formal structure
    - Optimal for academic and research positions
    """
    
    def _get_margins(self):
        """Classic margins"""
        return (1.0, 1.0, 1.0, 1.0)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header - Classic centered style with name and location
        personal_info = resume_data.get('personal_info', {})
        
        # Name
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], styles['name']))
        
        # Location on separate line below name
        if personal_info.get('location'):
            elements.append(Paragraph(personal_info['location'], styles['location']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Contact info line - email, phone, links ALL on one line
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('website'):
            website = personal_info['website']
            display = website.replace('https://', '').replace('http://', '').replace('www.', '')
            contact_parts.append(display)
        if personal_info.get('linkedin'):
            linkedin = personal_info['linkedin']
            display = linkedin.replace('https://', '').replace('http://', '').replace('www.', '').replace('linkedin.com/in/', '')
            contact_parts.append(f'linkedin.com/in/{display}')
        if personal_info.get('github'):
            github = personal_info['github']
            display = github.replace('https://', '').replace('http://', '').replace('www.', '').replace('github.com/', '')
            contact_parts.append(f'github.com/{display}')
        
        if contact_parts:
            contact_text = ' · '.join(contact_parts)
            elements.append(Paragraph(contact_text, styles['contact']))
            elements.append(Spacer(1, 0.05*inch))
        
        # Horizontal rule
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, 
                                  spaceAfter=10, spaceBefore=6))
        
        # Objective/Summary
        if resume_data.get('summary') or resume_data.get('objective'):
            elements.append(Paragraph('Summary', styles['section']))
            summary = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary, styles['justified']))
            elements.append(Spacer(1, 0.12*inch))
        
        # Education - First in academic style
        if resume_data.get('education'):
            elements.append(Paragraph('Education', styles['section']))
            
            for edu in resume_data['education']:
                # Institution
                elements.append(Paragraph(edu.get('institution', 'Institution'), styles['item_title']))
                
                # Degree and field
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = edu.get('degree', 'Degree')
                if field:
                    degree_text += f", {field}"
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                # Create two-column layout
                if date_text:
                    edu_table = Table([
                        [Paragraph(f"<i>{degree_text}</i>", styles['item_subtitle']),
                         Paragraph(date_text, styles['date'])]
                    ], colWidths=[4*inch, 1.5*inch])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_table)
                else:
                    elements.append(Paragraph(f"<i>{degree_text}</i>", styles['item_subtitle']))
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", styles['body']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('Experience', styles['section']))
            
            for exp in resume_data['experience']:
                # Position
                elements.append(Paragraph(exp.get('position', 'Position'), styles['item_title']))
                
                # Company and dates
                company = exp.get('company', 'Company')
                date_range = f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                exp_table = Table([
                    [Paragraph(f"<i>{company}</i>", styles['item_subtitle']),
                     Paragraph(date_range, styles['date'])]
                ], colWidths=[4*inch, 1.5*inch])
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_table)
                
                # Description
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"• {item}", styles['body']))
                    else:
                        elements.append(Paragraph(description, styles['justified']))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", styles['body']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Publications (if available)
        if resume_data.get('publications'):
            elements.append(Paragraph('Publications', styles['section']))
            for pub in resume_data['publications']:
                pub_text = f"{pub.get('authors', '')}, \"{pub.get('title', '')}\", <i>{pub.get('venue', '')}</i>, {pub.get('year', '')}"
                elements.append(Paragraph(pub_text, styles['body']))
                elements.append(Spacer(1, 0.05*inch))
        
        # Research/Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('Projects', styles['section']))
            
            for proj in resume_data['projects']:
                elements.append(Paragraph(proj.get('name', 'Project'), styles['item_title']))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], styles['justified']))
                
                if proj.get('technologies'):
                    tech_text = f"<i>Technologies:</i> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, styles['tech']))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Skills
        if resume_data.get('skills'):
            elements.append(Paragraph('Skills', styles['section']))
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
            
            elements.append(Spacer(1, 0.08*inch))
        
        # Honors & Awards
        if resume_data.get('certifications') or resume_data.get('awards'):
            elements.append(Paragraph('Honors & Awards', styles['section']))
            
            if resume_data.get('awards'):
                for award in resume_data['awards']:
                    elements.append(Paragraph(f"• {award}", styles['body']))
            
            if resume_data.get('certifications'):
                for cert in resume_data['certifications']:
                    cert_text = f"• {cert.get('name', 'Certification')} - {cert.get('issuer', 'Issuer')}"
                    if cert.get('date'):
                        cert_text += f" ({cert['date']})"
                    elements.append(Paragraph(cert_text, styles['body']))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create Classic theme styles - LaTeX inspired"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Times-Bold',
            fontSize=20,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=3,
        )
        
        styles['location'] = ParagraphStyle(
            'Location',
            fontName='Times-Roman',
            fontSize=11,
            textColor=colors.HexColor('#004F90'),
            alignment=TA_CENTER,
            spaceAfter=0,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Times-Roman',
            fontSize=10,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=3,
        )
        
        styles['links'] = ParagraphStyle(
            'Links',
            fontName='Times-Roman',
            fontSize=9,
            textColor=colors.HexColor('#0000EE'),
            alignment=TA_CENTER,
            spaceAfter=4,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Times-Bold',
            fontSize=12,
            textColor=colors.black,
            spaceAfter=6,
            spaceBefore=10,
        )
        
        styles['item_title'] = ParagraphStyle(
            'ItemTitle',
            fontName='Times-Bold',
            fontSize=11,
            spaceAfter=2,
        )
        
        styles['item_subtitle'] = ParagraphStyle(
            'ItemSubtitle',
            fontName='Times-Italic',
            fontSize=10,
            spaceAfter=3,
        )
        
        styles['date'] = ParagraphStyle(
            'Date',
            fontName='Times-Roman',
            fontSize=10,
            alignment=TA_RIGHT,
        )
        
        styles['body'] = ParagraphStyle(
            'Body',
            fontName='Times-Roman',
            fontSize=10,
            spaceAfter=3,
            leading=12,
            leftIndent=12,
        )
        
        styles['justified'] = ParagraphStyle(
            'Justified',
            fontName='Times-Roman',
            fontSize=10,
            spaceAfter=5,
            leading=12,
            alignment=TA_JUSTIFY,
        )
        
        styles['tech'] = ParagraphStyle(
            'Tech',
            fontName='Times-Roman',
            fontSize=10,
            spaceAfter=3,
        )
        
        return styles
