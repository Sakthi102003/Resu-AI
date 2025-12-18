from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from io import BytesIO
from typing import Dict, Any


class PDFGenerator:
    """Generate professional PDF resumes"""
    
    def __init__(self, template: str = "modern", theme_color: str = "#3B82F6"):
        self.template = template
        self.theme_color = theme_color
        self.buffer = BytesIO()
    
    def hex_to_rgb(self, hex_color: str):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))
    
    def generate(self, resume_data: Dict[str, Any]) -> BytesIO:
        """Generate PDF resume"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=6,
            alignment=TA_CENTER
        )
        
        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor(self.theme_color),
            spaceAfter=6,
            spaceBefore=12,
            borderWidth=1,
            borderColor=colors.gray,
            borderPadding=2,
            borderRadius=0,
            leftIndent=0,
            rightIndent=0,
        )
        
        subheading_style = ParagraphStyle(
            'Subheading',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Times-Bold',
            spaceAfter=2,
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Times-Roman',
            spaceAfter=4,
        )
        
        date_style = ParagraphStyle(
            'Date',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Times-Italic',
            textColor=colors.gray,
            alignment=TA_RIGHT,
        )
        
        # Personal Info - Header with underline
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], title_style))
            # Add underline using a table
            underline = Table([['']], colWidths=[6*inch])
            underline.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor(self.theme_color)),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(underline)
        
        # Contact information
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        
        if contact_parts:
            elements.append(Paragraph(' | '.join(contact_parts), contact_style))
        
        # Links
        links = []
        if personal_info.get('linkedin'):
            links.append(f"LinkedIn: {personal_info['linkedin']}")
        if personal_info.get('github'):
            links.append(f"GitHub: {personal_info['github']}")
        if personal_info.get('website'):
            links.append(f"Website: {personal_info['website']}")
        
        if links:
            link_style = ParagraphStyle(
                'Links',
                parent=contact_style,
                textColor=colors.HexColor(self.theme_color)
            )
            elements.append(Paragraph(' | '.join(links), link_style))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary/Objective
        if resume_data.get('summary'):
            elements.append(Paragraph('CAREER OBJECTIVE / PROFESSIONAL SUMMARY', heading_style))
            elements.append(Paragraph(resume_data['summary'], body_style))
            elements.append(Spacer(1, 0.1*inch))
        elif resume_data.get('objective'):
            elements.append(Paragraph('OBJECTIVE', heading_style))
            elements.append(Paragraph(resume_data['objective'], body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Skills - MOVED UP
        if resume_data.get('skills'):
            elements.append(Paragraph('TECHNICAL SKILLS', heading_style))
            skills = resume_data['skills']
            
            # Handle both formats: List[str] or List[{category, items}]
            if skills and isinstance(skills[0], dict):
                # New format with categories
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skills_text = f"<b>{category}:</b> {', '.join(items)}"
                        elements.append(Paragraph(skills_text, body_style))
            else:
                # Old format: simple list
                skills_text = ', '.join(skills)
                elements.append(Paragraph(skills_text, body_style))
            
            elements.append(Spacer(1, 0.1*inch))
        
        # Projects - MOVED UP
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', heading_style))
            for proj in resume_data['projects']:
                proj_title = f"<b>{proj.get('name', 'Project')}</b>"
                elements.append(Paragraph(proj_title, subheading_style))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], body_style))
                
                if proj.get('technologies'):
                    tech_text = f"<b>Technologies:</b> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, body_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Experience / Internship Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('INTERNSHIP / WORK EXPERIENCE', heading_style))
            for exp in resume_data['experience']:
                # Create a table for position (left) and dates (right)
                date_range = f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                position_cell = Paragraph(f"<b>{exp.get('position', 'Position')}</b>", subheading_style)
                date_cell = Paragraph(f"<i>{date_range}</i>", date_style)
                
                exp_table = Table([[position_cell, date_cell]], colWidths=[4.5*inch, 1.5*inch])
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_table)
                
                # Company
                elements.append(Paragraph(exp.get('company', 'Company'), body_style))
                
                # Description (can be string or list)
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:  # Skip empty strings
                                elements.append(Paragraph(f"• {item}", body_style))
                    else:
                        elements.append(Paragraph(description, body_style))
                
                # Achievements
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", body_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', heading_style))
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b> - {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                elements.append(Paragraph(cert_text, body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Education - MOVED TO END
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', heading_style))
            for edu in resume_data['education']:
                # Handle both field_of_study and field
                field = edu.get('field_of_study') or edu.get('field', '')
                edu_title = f"<b>{edu.get('degree', 'Degree')}</b>"
                if field:
                    edu_title += f" in {field}"
                
                # Create table for degree (left) and dates (right)
                degree_cell = Paragraph(edu_title, subheading_style)
                
                # Handle graduation_date or start_date/end_date
                date_text = ''
                if edu.get('graduation_date'):
                    date_text = edu['graduation_date']
                else:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                if date_text:
                    date_cell = Paragraph(f"<i>{date_text}</i>", date_style)
                    edu_table = Table([[degree_cell, date_cell]], colWidths=[4.5*inch, 1.5*inch])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_table)
                else:
                    elements.append(degree_cell)
                
                # Institution
                elements.append(Paragraph(edu.get('institution', 'Institution'), body_style))
                
                # Handle GPA
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", body_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def _generate_google(self, resume_data: Dict[str, Any]) -> BytesIO:
        """Generate Google-style PDF resume - Clean, minimalist, technical focus"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Google style: Simple, clean, Helvetica-like fonts
        name_style = ParagraphStyle(
            'GoogleName',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=3,
            alignment=TA_LEFT
        )
        
        contact_style = ParagraphStyle(
            'GoogleContact',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.grey,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        section_style = ParagraphStyle(
            'GoogleSection',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=4,
            spaceBefore=10,
            leftIndent=0
        )
        
        item_title_style = ParagraphStyle(
            'GoogleItemTitle',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=2,
        )
        
        item_subtitle_style = ParagraphStyle(
            'GoogleItemSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.grey,
            spaceAfter=2,
        )
        
        body_style = ParagraphStyle(
            'GoogleBody',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            spaceAfter=3,
            leading=11,
        )
        
        # Personal Info - Google minimalist style
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'].upper(), name_style))
        
        # Contact - all on one line
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('linkedin'):
            contact_parts.append(personal_info['linkedin'].replace('https://linkedin.com/in/', ''))
        if personal_info.get('github'):
            contact_parts.append(personal_info['github'].replace('https://github.com/', 'github.com/'))
        
        if contact_parts:
            elements.append(Paragraph(' • '.join(contact_parts), contact_style))
        
        # Thin horizontal line
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceAfter=8))
        
        # Education First (Google style)
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_style))
            for edu in resume_data['education']:
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = f"{edu.get('degree', 'Degree')}"
                if field:
                    degree_text += f", {field}"
                
                # Create table for institution (left) and dates (right)
                inst_cell = Paragraph(f"<b>{edu.get('institution', 'Institution')}</b>", item_title_style)
                
                date_text = ''
                if edu.get('graduation_date'):
                    date_text = edu['graduation_date']
                else:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                if date_text:
                    date_cell = Paragraph(date_text, item_subtitle_style)
                    edu_table = Table([[inst_cell, date_cell]], colWidths=[5.5*inch, 2*inch])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_table)
                else:
                    elements.append(inst_cell)
                
                elements.append(Paragraph(degree_text, body_style))
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Technical Skills
        if resume_data.get('skills'):
            elements.append(Paragraph('TECHNICAL SKILLS', section_style))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skills_text = f"<b>{category}:</b> {', '.join(items)}"
                        elements.append(Paragraph(skills_text, body_style))
            else:
                skills_text = ', '.join(skills)
                elements.append(Paragraph(skills_text, body_style))
            
            elements.append(Spacer(1, 0.05*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('EXPERIENCE', section_style))
            for exp in resume_data['experience']:
                date_range = f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                position_cell = Paragraph(f"<b>{exp.get('position', 'Position')}</b>", item_title_style)
                date_cell = Paragraph(date_range, item_subtitle_style)
                
                exp_table = Table([[position_cell, date_cell]], colWidths=[5.5*inch, 2*inch])
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_table)
                
                elements.append(Paragraph(f"<i>{exp.get('company', 'Company')}</i>", item_subtitle_style))
                
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"• {item}", body_style))
                    else:
                        elements.append(Paragraph(description, body_style))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', section_style))
            for proj in resume_data['projects']:
                proj_title = f"<b>{proj.get('name', 'Project')}</b>"
                elements.append(Paragraph(proj_title, item_title_style))
                
                if proj.get('description'):
                    elements.append(Paragraph(proj['description'], body_style))
                
                if proj.get('technologies'):
                    tech_text = f"<i>Technologies:</i> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', section_style))
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b> - {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                elements.append(Paragraph(cert_text, body_style))
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _generate_amazon(self, resume_data: Dict[str, Any]) -> BytesIO:
        """Generate Amazon-style PDF resume - Leadership principles, metrics-driven"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Amazon style: Professional, emphasis on impact metrics
        name_style = ParagraphStyle(
            'AmazonName',
            parent=styles['Normal'],
            fontSize=20,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=4,
            alignment=TA_CENTER
        )
        
        contact_style = ParagraphStyle(
            'AmazonContact',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            spaceAfter=14,
            alignment=TA_CENTER
        )
        
        section_style = ParagraphStyle(
            'AmazonSection',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=6,
            spaceBefore=12,
            borderWidth=0,
            borderPadding=0,
        )
        
        item_title_style = ParagraphStyle(
            'AmazonItemTitle',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=1,
        )
        
        item_subtitle_style = ParagraphStyle(
            'AmazonItemSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Oblique',
            spaceAfter=3,
        )
        
        body_style = ParagraphStyle(
            'AmazonBody',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=4,
            leading=12,
            leftIndent=15,
        )
        
        # Personal Info - Amazon centered style
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], name_style))
        
        # Contact
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        
        if contact_parts:
            elements.append(Paragraph(' | '.join(contact_parts), contact_style))
        
        # Links
        links = []
        if personal_info.get('linkedin'):
            links.append(personal_info['linkedin'])
        if personal_info.get('github'):
            links.append(personal_info['github'])
        
        if links:
            link_style = ParagraphStyle('AmazonLinks', parent=contact_style, fontSize=8)
            elements.append(Paragraph(' | '.join(links), link_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Professional Summary
        if resume_data.get('summary') or resume_data.get('objective'):
            elements.append(Paragraph('PROFESSIONAL SUMMARY', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            summary_text = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary_text, body_style))
            elements.append(Spacer(1, 0.05*inch))
        
        # Core Competencies / Skills
        if resume_data.get('skills'):
            elements.append(Paragraph('CORE COMPETENCIES', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skills_text = f"<b>{category}:</b> {', '.join(items)}"
                        elements.append(Paragraph(skills_text, body_style))
            else:
                skills_text = ', '.join(skills)
                elements.append(Paragraph(skills_text, body_style))
            
            elements.append(Spacer(1, 0.05*inch))
        
        # Professional Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('PROFESSIONAL EXPERIENCE', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            
            for exp in resume_data['experience']:
                date_range = f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                # Company and Position
                position_cell = Paragraph(f"<b>{exp.get('company', 'Company')}</b> - {exp.get('position', 'Position')}", item_title_style)
                date_cell = Paragraph(date_range, item_subtitle_style)
                
                exp_table = Table([[position_cell, date_cell]], colWidths=[5*inch, 1.5*inch])
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(exp_table)
                
                # Impact-focused descriptions (Amazon loves metrics!)
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"• {item}", body_style))
                    else:
                        elements.append(Paragraph(f"• {description}", body_style))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", body_style))
                
                elements.append(Spacer(1, 0.08*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('KEY PROJECTS', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            
            for proj in resume_data['projects']:
                proj_title = f"<b>{proj.get('name', 'Project')}</b>"
                elements.append(Paragraph(proj_title, item_title_style))
                
                if proj.get('description'):
                    elements.append(Paragraph(f"• {proj['description']}", body_style))
                
                if proj.get('technologies'):
                    tech_text = f"• <b>Technologies Used:</b> {', '.join(proj['technologies'])}"
                    elements.append(Paragraph(tech_text, body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            
            for edu in resume_data['education']:
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = f"{edu.get('degree', 'Degree')}"
                if field:
                    degree_text += f" in {field}"
                
                inst_cell = Paragraph(f"<b>{edu.get('institution', 'Institution')}</b> - {degree_text}", item_title_style)
                
                date_text = ''
                if edu.get('graduation_date'):
                    date_text = edu['graduation_date']
                else:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                if date_text:
                    date_cell = Paragraph(date_text, item_subtitle_style)
                    edu_table = Table([[inst_cell, date_cell]], colWidths=[5*inch, 1.5*inch])
                    edu_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ]))
                    elements.append(edu_table)
                else:
                    elements.append(inst_cell)
                
                if edu.get('gpa') or edu.get('grade'):
                    gpa = edu.get('gpa') or edu.get('grade')
                    elements.append(Paragraph(f"GPA: {gpa}", body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS & AWARDS', section_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))
            
            for cert in resume_data['certifications']:
                cert_text = f"<b>{cert.get('name', 'Certification')}</b> - {cert.get('issuer', 'Issuer')}"
                if cert.get('date'):
                    cert_text += f" ({cert['date']})"
                elements.append(Paragraph(f"• {cert_text}", body_style))
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _generate_meta(self, resume_data: Dict[str, Any]) -> BytesIO:
        """Generate Meta/Facebook-style PDF resume - Bold, impact-first, modern"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Meta style: Bold headers, clean layout, impact metrics
        meta_blue = colors.HexColor('#0668E1')  # Meta brand blue
        
        name_style = ParagraphStyle(
            'MetaName',
            parent=styles['Normal'],
            fontSize=22,
            fontName='Helvetica-Bold',
            textColor=meta_blue,
            spaceAfter=2,
            alignment=TA_LEFT
        )
        
        contact_style = ParagraphStyle(
            'MetaContact',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.grey,
            spaceAfter=10,
            alignment=TA_LEFT
        )
        
        section_style = ParagraphStyle(
            'MetaSection',
            parent=styles['Normal'],
            fontSize=13,
            fontName='Helvetica-Bold',
            textColor=meta_blue,
            spaceAfter=5,
            spaceBefore=10,
            borderWidth=0,
        )
        
        item_title_style = ParagraphStyle(
            'MetaItemTitle',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            spaceAfter=1,
        )
        
        item_subtitle_style = ParagraphStyle(
            'MetaItemSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=colors.grey,
            spaceAfter=2,
        )
        
        body_style = ParagraphStyle(
            'MetaBody',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            spaceAfter=3,
            leading=11,
        )
        
        impact_style = ParagraphStyle(
            'MetaImpact',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            spaceAfter=3,
            leading=11,
            leftIndent=12,
        )
        
        # Personal Info - Meta bold style
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], name_style))
        
        # Contact - compact format
        contact_parts = []
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            linkedin_clean = personal_info['linkedin'].replace('https://', '').replace('http://', '')
            contact_parts.append(linkedin_clean)
        if personal_info.get('github'):
            github_clean = personal_info['github'].replace('https://', '').replace('http://', '')
            contact_parts.append(github_clean)
        
        if contact_parts:
            elements.append(Paragraph(' • '.join(contact_parts), contact_style))
        
        # Summary (if available)
        if resume_data.get('summary') or resume_data.get('objective'):
            summary_style = ParagraphStyle(
                'MetaSummary',
                parent=body_style,
                fontSize=10,
                spaceAfter=8,
            )
            summary_text = resume_data.get('summary') or resume_data.get('objective')
            elements.append(Paragraph(summary_text, summary_style))
        
        # Technical Skills - Compact format
        if resume_data.get('skills'):
            elements.append(Paragraph('TECHNICAL SKILLS', section_style))
            skills = resume_data['skills']
            
            if skills and isinstance(skills[0], dict):
                skill_lines = []
                for skill_cat in skills:
                    category = skill_cat.get('category', '')
                    items = skill_cat.get('items', [])
                    if category and items:
                        skill_lines.append(f"<b>{category}:</b> {', '.join(items)}")
                elements.append(Paragraph(' | '.join(skill_lines), body_style))
            else:
                skills_text = ', '.join(skills)
                elements.append(Paragraph(skills_text, body_style))
            
            elements.append(Spacer(1, 0.05*inch))
        
        # Experience - Impact first
        if resume_data.get('experience'):
            elements.append(Paragraph('EXPERIENCE', section_style))
            
            for exp in resume_data['experience']:
                # Title row
                position_text = f"<b>{exp.get('position', 'Position')}</b> | {exp.get('company', 'Company')}"
                date_range = f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'Present') if not exp.get('current') else 'Present'}"
                
                title_cell = Paragraph(position_text, item_title_style)
                date_cell = Paragraph(date_range, item_subtitle_style)
                
                title_table = Table([[title_cell, date_cell]], colWidths=[5.5*inch, 2*inch])
                title_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(title_table)
                
                # Impact bullets
                description = exp.get('description')
                if description:
                    if isinstance(description, list):
                        for item in description:
                            if item:
                                elements.append(Paragraph(f"• {item}", impact_style))
                    else:
                        elements.append(Paragraph(f"• {description}", impact_style))
                
                if exp.get('achievements'):
                    for achievement in exp['achievements']:
                        elements.append(Paragraph(f"• {achievement}", impact_style))
                
                elements.append(Spacer(1, 0.06*inch))
        
        # Projects
        if resume_data.get('projects'):
            elements.append(Paragraph('PROJECTS', section_style))
            
            for proj in resume_data['projects']:
                proj_title = f"<b>{proj.get('name', 'Project')}</b>"
                
                if proj.get('technologies'):
                    tech_list = ', '.join(proj['technologies'])
                    proj_title += f" | <i>{tech_list}</i>"
                
                elements.append(Paragraph(proj_title, item_title_style))
                
                if proj.get('description'):
                    elements.append(Paragraph(f"• {proj['description']}", impact_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_style))
            
            for edu in resume_data['education']:
                field = edu.get('field_of_study') or edu.get('field', '')
                degree_text = f"<b>{edu.get('degree', 'Degree')}</b>"
                if field:
                    degree_text += f" in {field}"
                degree_text += f" | {edu.get('institution', 'Institution')}"
                
                degree_cell = Paragraph(degree_text, item_title_style)
                
                date_text = ''
                if edu.get('graduation_date'):
                    date_text = edu['graduation_date']
                else:
                    date_range = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
                    if date_range.strip() != '-':
                        date_text = date_range
                
                if date_text:
                    date_cell = Paragraph(date_text, item_subtitle_style)
                    edu_table = Table([[degree_cell, date_cell]], colWidths=[5.5*inch, 2*inch])
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
                    elements.append(Paragraph(f"GPA: {gpa}", body_style))
                
                elements.append(Spacer(1, 0.05*inch))
        
        # Certifications
        if resume_data.get('certifications'):
            elements.append(Paragraph('CERTIFICATIONS', section_style))
            
            cert_items = []
            for cert in resume_data['certifications']:
                cert_text = f"{cert.get('name', 'Certification')}"
                if cert.get('issuer'):
                    cert_text += f" ({cert['issuer']})"
                if cert.get('date'):
                    cert_text += f" - {cert['date']}"
                cert_items.append(cert_text)
            
            elements.append(Paragraph(' | '.join(cert_items), body_style))
            elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer


def generate_pdf_resume(resume_data: Dict[str, Any], template: str = "modern", theme_color: str = "#3B82F6") -> BytesIO:
    """Main function to generate PDF resume"""
    generator = PDFGenerator(template, theme_color)
    return generator.generate(resume_data)
