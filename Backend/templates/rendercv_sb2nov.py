"""RenderCV sb2nov Theme - Popular GitHub Template Style, Compact, Information-Dense"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from .base_template import BaseTemplate
from typing import Dict, Any


class RenderCVSb2novTemplate(BaseTemplate):
    """
    RenderCV sb2nov Theme - Based on popular GitHub resume template
    Features:
    - Compact, information-dense layout
    - Single-page optimization
    - Clear section separation
    - Maximum content in minimal space
    - GitHub resume style
    """
    
    def _get_margins(self):
        """Tight margins for max content"""
        return (0.4, 0.4, 0.5, 0.5)
    
    def generate(self, resume_data: Dict[str, Any]):
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Header - Compact
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], styles['name']))
        
        # Contact - Very compact, single line
        contact_parts = []
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'].split('/')[-1])
        if personal_info.get('github'):
            contact_parts.append(personal_info['github'].split('/')[-1])
        
        if contact_parts:
            elements.append(Paragraph(' · '.join(contact_parts), styles['contact']))
        
        # Thin separator
        sep_table = Table([['']], colWidths=[7.2*inch])
        sep_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(sep_table)
        
        # Education - Top priority in sb2nov style
        if resume_data.get('education'):
            elements.append(Paragraph('Education', styles['section']))
            
            for edu in resume_data['education']:
                institution = edu.get('institution', 'Institution')
                field = edu.get('field_of_study') or edu.get('field', '')
                degree = edu.get('degree', 'Degree')
                
                date_text = edu.get('graduation_date', '')
                if not date_text:
                    date_range = f"{edu.get('start_date', '')} -- {edu.get('end_date', '')}"
                    if date_range.strip() != '--':
                        date_text = date_range
                
                # Institution and Date
                edu_row1 = Table([
                    [Paragraph(f"<b>{institution}</b>", styles['item_bold']),
                     Paragraph(date_text, styles['date'])]
                ], colWidths=[5.5*inch, 1.7*inch])
                edu_row1.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(edu_row1)
                
                # Degree and GPA
                degree_gpa = f"{degree}"
                if field:
                    degree_gpa += f" in {field}"
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    degree_gpa += f"; GPA: {gpa}"
                
                elements.append(Paragraph(degree_gpa, styles['item_detail']))
                elements.append(Spacer(1, 0.06*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('Experience', styles['section']))
            
            for exp in resume_data['experience']:
                company = exp.get('company', 'Company')
                position = exp.get('position', 'Position')
                date_range = f"{exp.get('start_date', '')} -- {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                location = exp.get('location', '')
                
                # Company and Location/Date
                exp_row1 = Table([
                    [Paragraph(f"<b>{company}</b>", styles['item_bold']),
                     Paragraph(location if location else date_range, styles['date'])]
                ], colWidths=[5.5*inch, 1.7*inch])
                exp_row1.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_row1)
                
                # Position and Date (if location was shown above)
                exp_row2 = Table([
                    [Paragraph(f"<i>{position}</i>", styles['item_detail']),
                     Paragraph(date_range if location else '', styles['date_small'])]
                ], colWidths=[5.5*inch, 1.7*inch])
                exp_row2.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_row2)
                
                # Achievements - Very compact
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description[:4]:  # Limit to 4 bullets for space
                            if item:
                                elements.append(Paragraph(f"• {item}", styles['bullet']))
                    else:
                        elements.append(Paragraph(f"• {description}", styles['bullet']))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements'][:3]:  # Limit
                        elements.append(Paragraph(f"• {achievement}", styles['bullet']))
                
                elements.append(Spacer(1, 0.06*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('Projects', styles['section']))
            
            for proj in resume_data['projects']:
                proj_name = proj.get('name', 'Project')
                
                # Project with tech stack inline
                if proj.get('technologies'):
                    proj_header = f"<b>{proj_name}</b> | {', '.join(proj['technologies'][:5])}"  # Limit tech stack
                else:
                    proj_header = f"<b>{proj_name}</b>"
                
                elements.append(Paragraph(proj_header, styles['item_bold']))
                
                if proj.get('description'):
                    # Keep description short
                    desc = proj['description']
                    if len(desc) > 200:
                        desc = desc[:197] + '...'
                    elements.append(Paragraph(f"• {desc}", styles['bullet']))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Technical Skills - Compact table format
        if resume_data.get('skills'):
            elements.append(Paragraph('Technical Skills', styles['section']))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                skill_rows = []
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skill_rows.append([
                            Paragraph(f"<b>{category}:</b>", styles['skill_label']),
                            Paragraph(', '.join(items), styles['skill_value'])
                        ])
                
                if skill_rows:
                    skill_table = Table(skill_rows, colWidths=[1.2*inch, 6*inch])
                    skill_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                        ('TOPPADDING', (0, 0), (-1, -1), 1),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                    ]))
                    elements.append(skill_table)
            else:
                elements.append(Paragraph(', '.join(skills), styles['item_detail']))
            
            elements.append(Spacer(1, 0.05*inch))
        
        # Certifications - Very compact
        if resume_data.get('certifications'):
            elements.append(Paragraph('Certifications', styles['section']))
            
            cert_list = []
            for cert in resume_data['certifications']:
                cert_str = cert.get('name', 'Certification')
                if cert.get('issuer'):
                    cert_str += f" ({cert['issuer']})"
                cert_list.append(cert_str)
            
            # All on one line if possible
            elements.append(Paragraph(' • '.join(cert_list), styles['item_detail']))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create sb2nov theme styles - compact and dense"""
        styles = {}
        
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Times-Bold',
            fontSize=20,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=2,
        )
        
        styles['contact'] = ParagraphStyle(
            'Contact',
            fontName='Times-Roman',
            fontSize=9,
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=3,
        )
        
        styles['section'] = ParagraphStyle(
            'Section',
            fontName='Times-Bold',
            fontSize=11,
            textColor=colors.black,
            spaceAfter=4,
            spaceBefore=6,
            textTransform='uppercase',
        )
        
        styles['item_bold'] = ParagraphStyle(
            'ItemBold',
            fontName='Times-Bold',
            fontSize=10,
            spaceAfter=1,
        )
        
        styles['item_detail'] = ParagraphStyle(
            'ItemDetail',
            fontName='Times-Italic',
            fontSize=9,
            spaceAfter=2,
        )
        
        styles['date'] = ParagraphStyle(
            'Date',
            fontName='Times-Roman',
            fontSize=9,
            alignment=TA_RIGHT,
        )
        
        styles['date_small'] = ParagraphStyle(
            'DateSmall',
            fontName='Times-Italic',
            fontSize=9,
            alignment=TA_RIGHT,
        )
        
        styles['bullet'] = ParagraphStyle(
            'Bullet',
            fontName='Times-Roman',
            fontSize=9,
            spaceAfter=1,
            leading=10,
            leftIndent=10,
        )
        
        styles['skill_label'] = ParagraphStyle(
            'SkillLabel',
            fontName='Times-Bold',
            fontSize=9,
        )
        
        styles['skill_value'] = ParagraphStyle(
            'SkillValue',
            fontName='Times-Roman',
            fontSize=9,
        )
        
        return styles
