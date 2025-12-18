"""LaTeX Template Processor - Uses actual .tex files from Templates folder"""

import os
import re
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Dict, Any


class LaTeXTemplateProcessor:
    """Process LaTeX templates from the Templates folder"""
    
    # Path to templates folder (one level up from Backend)
    TEMPLATES_DIR = Path(__file__).parent.parent.parent / "Templates"
    
    TEMPLATE_FILES = {
        'auto_cv': 'autocv.tex',
        'anti_cv': 'anticv.tex',
        'ethan': 'ethan.tex',
        'rendercv_classic': 'rendercv_classic.tex',
        # Yuan template requires custom style file - skip for now
        # 'yuan': 'yuanresume.tex',
    }
    
    # Templates that require XeLaTeX instead of pdfLaTeX
    XELATEX_TEMPLATES = ['yuan']
    
    @classmethod
    def get_template_path(cls, template_name: str) -> Path:
        """Get the full path to a template file"""
        filename = cls.TEMPLATE_FILES.get(template_name, 'autocv.tex')
        return cls.TEMPLATES_DIR / filename
    
    @classmethod
    def _escape_latex(cls, text: str) -> str:
        """Escape special LaTeX characters"""
        if not text:
            return ""
        
        chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        
        return "".join(chars.get(c, c) for c in str(text))

    @classmethod
    def _generate_rendercv_classic_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for RenderCV Classic template - Academic/Traditional style"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header
        content.append(r"\begin{header}")
        content.append(rf"    \fontsize{{25 pt}}{{25 pt}}\selectfont {cls._escape_latex(info.get('name', 'Your Name'))}")
        content.append(r"    \vspace{5 pt}")
        content.append(r"    \normalsize")
        
        header_items = []
        if info.get('location'):
            header_items.append(rf"\mbox{{{cls._escape_latex(info['location'])}}}")
        if info.get('email'):
            email = cls._escape_latex(info['email'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{mailto:{email}}}{{{email}}}}}")
        if info.get('phone'):
            phone = cls._escape_latex(info['phone'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{tel:{phone}}}{{{phone}}}}}")
        if info.get('website'):
            website = cls._escape_latex(info['website'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://{website}}}{{{website}}}}}")
        if info.get('linkedin'):
            linkedin = cls._escape_latex(info['linkedin'])
            username = linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://linkedin.com/in/{username}}}{{linkedin.com/in/{username}}}}}")
        if info.get('github'):
            github = cls._escape_latex(info['github'])
            username = github.replace('github.com/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://github.com/{username}}}{{github.com/{username}}}}}")
            
        content.append(r"    " + r"%    \kern 5.0 pt%    \AND%    \kern 5.0 pt%".join(header_items))
        content.append(r"\end{header}")
        content.append(r"\vspace{5 pt - 0.3 cm}")

        # Summary
        if resume_data.get('summary'):
            content.append(r"\section{Summary}")
            content.append(r"\begin{onecolentry}")
            content.append(cls._escape_latex(resume_data['summary']))
            content.append(r"\end{onecolentry}")
            content.append(r"\vspace{0.2 cm}")

        # Experience
        if resume_data.get('experience'):
            content.append(r"\section{Experience}")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} -- {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                location = cls._escape_latex(exp.get('location', ''))
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                content.append(rf"    \textbf{{{position}}}, {company} -- {location}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.10 cm}")
                
                if exp.get('description'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    for item in exp['description']:
                        content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.2 cm}")

        # Education
        if resume_data.get('education'):
            content.append(r"\section{Education}")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} -- {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                full_degree = f"{degree} in {field}" if field else degree
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                content.append(rf"    \textbf{{{institution}}}, {full_degree}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.10 cm}")
                
                if edu.get('gpa') or edu.get('coursework'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    if edu.get('gpa'):
                        content.append(rf"        \item GPA: {cls._escape_latex(edu['gpa'])}")
                    if edu.get('coursework'):
                        content.append(rf"        \item \textbf{{Coursework:}} {cls._escape_latex(edu['coursework'])}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.2 cm}")

        # Projects
        if resume_data.get('projects'):
            content.append(r"\section{Projects}")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                url = cls._escape_latex(proj.get('url', ''))
                
                content.append(r"\begin{twocolentry}{")
                if url:
                    content.append(rf"    \href{{{url}}}{{{url}}}")
                else:
                    content.append(r"    ")
                content.append(r"}")
                content.append(rf"    \textbf{{{name}}}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.10 cm}")
                
                content.append(r"\begin{onecolentry}")
                content.append(r"    \begin{highlights}")
                if proj.get('description'):
                    content.append(rf"        \item {cls._escape_latex(proj['description'])}")
                if proj.get('technologies'):
                    techs = ", ".join(proj['technologies'])
                    content.append(rf"        \item Tools Used: {cls._escape_latex(techs)}")
                if proj.get('highlights'):
                    # Assuming highlights is a string in the JSON structure based on frontend code
                    # But frontend code shows highlights as a string in the example: "• Handles 10K+..."
                    # Let's handle both string and list
                    highlights = proj.get('highlights')
                    if isinstance(highlights, list):
                        for h in highlights:
                            content.append(rf"        \item {cls._escape_latex(h)}")
                    elif isinstance(highlights, str):
                         # Split by bullet point if present
                         items = [h.strip() for h in highlights.split('•') if h.strip()]
                         for item in items:
                             content.append(rf"        \item {cls._escape_latex(item)}")
                content.append(r"    \end{highlights}")
                content.append(r"\end{onecolentry}")
                content.append(r"\vspace{0.2 cm}")

        # Skills
        if resume_data.get('skills'):
            content.append(r"\section{Technologies}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(r"\begin{onecolentry}")
                    content.append(rf"    \textbf{{{category}:}} {cls._escape_latex(items)}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.2 cm}")
                elif isinstance(skill, str):
                    content.append(r"\begin{onecolentry}")
                    content.append(cls._escape_latex(skill))
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.2 cm}")

        return "\n".join(content)

    @classmethod
    def _generate_rendercv_engineering_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for RenderCV Engineering template - Skills-first, technical focus"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header (same style as classic but engineering focused)
        content.append(r"\begin{header}")
        content.append(rf"    \fontsize{{25 pt}}{{25 pt}}\selectfont {cls._escape_latex(info.get('name', 'Your Name'))}")
        content.append(r"    \vspace{5 pt}")
        content.append(r"    \normalsize")
        
        header_items = []
        if info.get('location'):
            header_items.append(rf"\mbox{{{cls._escape_latex(info['location'])}}}")
        if info.get('email'):
            email = cls._escape_latex(info['email'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{mailto:{email}}}{{{email}}}}}")
        if info.get('phone'):
            phone = cls._escape_latex(info['phone'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{tel:{phone}}}{{{phone}}}}}")
        if info.get('github'):
            github = cls._escape_latex(info['github'])
            username = github.replace('github.com/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://github.com/{username}}}{{GitHub: {username}}}}}")
        if info.get('linkedin'):
            linkedin = cls._escape_latex(info['linkedin'])
            username = linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://linkedin.com/in/{username}}}{{LinkedIn: {username}}}}}")
            
        content.append(r"    " + r"%    \kern 5.0 pt%    \AND%    \kern 5.0 pt%".join(header_items))
        content.append(r"\end{header}")
        content.append(r"\vspace{5 pt - 0.3 cm}")

        # Summary (optional but recommended for engineering roles)
        if resume_data.get('summary'):
            content.append(r"\section{Summary}")
            content.append(r"\begin{onecolentry}")
            content.append(cls._escape_latex(resume_data['summary']))
            content.append(r"\end{onecolentry}")
            content.append(r"\vspace{0.2 cm}")

        # ENGINEERING: Skills FIRST (key differentiator)
        if resume_data.get('skills'):
            content.append(r"\section{Technical Skills}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(r"\begin{onecolentry}")
                    content.append(rf"    \textbf{{{category}:}} {cls._escape_latex(items)}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.15 cm}")
                elif isinstance(skill, str):
                    content.append(r"\begin{onecolentry}")
                    content.append(cls._escape_latex(skill))
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.15 cm}")
            content.append(r"\vspace{0.1 cm}")

        # Experience (with engineering emphasis - metrics highlighted)
        if resume_data.get('experience'):
            content.append(r"\section{Professional Experience}")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} -- {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                location = cls._escape_latex(exp.get('location', ''))
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                content.append(rf"    \textbf{{{company}}} \textbar{{}} {position}")
                if location:
                    content.append(rf"    \\ {location}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.10 cm}")
                
                if exp.get('description'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    for item in exp['description']:
                        content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.2 cm}")

        # Education
        if resume_data.get('education'):
            content.append(r"\section{Education}")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} -- {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                if field:
                    content.append(rf"    \textbf{{{degree} in {field}}}")
                else:
                    content.append(rf"    \textbf{{{degree}}}")
                content.append(rf"    \\ {institution}")
                if edu.get('gpa'):
                    content.append(rf"    \\ GPA: {cls._escape_latex(edu['gpa'])}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.2 cm}")

        # Projects (engineering emphasis)
        if resume_data.get('projects'):
            content.append(r"\section{Projects}")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                
                content.append(r"\begin{onecolentry}")
                content.append(rf"    \textbf{{{name}}}")
                if proj.get('technologies'):
                    techs = ", ".join(proj['technologies'])
                    content.append(rf"    \\ \textit{{Technologies:}} {cls._escape_latex(techs)}")
                content.append(r"\end{onecolentry}")
                content.append(r"\vspace{0.10 cm}")
                
                if proj.get('description') or proj.get('highlights'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    if proj.get('description'):
                        content.append(rf"        \item {cls._escape_latex(proj['description'])}")
                    if proj.get('highlights'):
                        highlights = proj.get('highlights')
                        if isinstance(highlights, list):
                            for h in highlights:
                                content.append(rf"        \item {cls._escape_latex(h)}")
                        elif isinstance(highlights, str):
                            items = [h.strip() for h in highlights.split('•') if h.strip()]
                            for item in items:
                                content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.15 cm}")

        return "\n".join(content)

    @classmethod
    def _generate_rendercv_sb2nov_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for RenderCV sb2nov template - Compact, GitHub-style"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header - Compact style
        content.append(r"\begin{header}")
        content.append(rf"    \fontsize{{25 pt}}{{25 pt}}\selectfont {cls._escape_latex(info.get('name', 'Your Name'))}")
        content.append(r"    \vspace{5 pt}")
        content.append(r"    \normalsize")
        
        header_items = []
        if info.get('email'):
            email = cls._escape_latex(info['email'])
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{mailto:{email}}}{{{email}}}}}")
        if info.get('phone'):
            phone = cls._escape_latex(info['phone'])
            header_items.append(rf"\mbox{{{phone}}}")
        if info.get('github'):
            github = cls._escape_latex(info['github'])
            username = github.replace('github.com/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://github.com/{username}}}{{{username}}}}}")
        if info.get('linkedin'):
            linkedin = cls._escape_latex(info['linkedin'])
            username = linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
            header_items.append(rf"\mbox{{\hrefWithoutArrow{{https://linkedin.com/in/{username}}}{{LinkedIn}}}}")
        if info.get('location'):
            header_items.append(rf"\mbox{{{cls._escape_latex(info['location'])}}}")
            
        content.append(r"    " + r"%    \kern 5.0 pt%    \AND%    \kern 5.0 pt%".join(header_items))
        content.append(r"\end{header}")
        content.append(r"\vspace{5 pt - 0.3 cm}")

        # Summary (compact for sb2nov style)
        if resume_data.get('summary'):
            content.append(r"\section{Summary}")
            content.append(r"\begin{onecolentry}")
            content.append(cls._escape_latex(resume_data['summary']))
            content.append(r"\end{onecolentry}")
            content.append(r"\vspace{0.15 cm}")

        # SB2NOV: Education FIRST (GitHub resume style)
        if resume_data.get('education'):
            content.append(r"\section{Education}")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} -- {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                content.append(rf"    \textbf{{{institution}}}")
                if field:
                    degree_line = rf"    \\ {degree} in {field}"
                else:
                    degree_line = rf"    \\ {degree}"
                if edu.get('gpa'):
                    degree_line += rf" \textbar{{}} GPA: {cls._escape_latex(edu['gpa'])}"
                content.append(degree_line)
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.15 cm}")

        # Experience - Compact format
        if resume_data.get('experience'):
            content.append(r"\section{Experience}")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} -- {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                location = cls._escape_latex(exp.get('location', ''))
                
                content.append(r"\begin{twocolentry}{")
                content.append(f"    {dates}")
                content.append(r"}")
                content.append(rf"    \textbf{{{position}}} \textbar{{}} {company}")
                if location:
                    content.append(rf"    \\ \textit{{{location}}}")
                content.append(r"\end{twocolentry}")
                content.append(r"\vspace{0.05 cm}")
                
                if exp.get('description'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    for item in exp['description']:
                        content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.15 cm}")

        # Projects - Compact
        if resume_data.get('projects'):
            content.append(r"\section{Projects}")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                url = proj.get('url', '')
                
                project_title = rf"\textbf{{{name}}}"
                if url:
                    project_title = rf"\href{{{cls._escape_latex(url)}}}{{\textbf{{{name}}}}}"
                
                content.append(r"\begin{onecolentry}")
                content.append(f"    {project_title}")
                if proj.get('technologies'):
                    techs = ", ".join(proj['technologies'])
                    content.append(rf"    \textbar{{}} \textit{{{cls._escape_latex(techs)}}}")
                content.append(r"\end{onecolentry}")
                content.append(r"\vspace{0.05 cm}")
                
                if proj.get('description') or proj.get('highlights'):
                    content.append(r"\begin{onecolentry}")
                    content.append(r"    \begin{highlights}")
                    if proj.get('description'):
                        content.append(rf"        \item {cls._escape_latex(proj['description'])}")
                    if proj.get('highlights'):
                        highlights = proj.get('highlights')
                        if isinstance(highlights, list):
                            for h in highlights:
                                content.append(rf"        \item {cls._escape_latex(h)}")
                        elif isinstance(highlights, str):
                            items = [h.strip() for h in highlights.split('•') if h.strip()]
                            for item in items:
                                content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{highlights}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.1 cm}")

        # Skills - Last in sb2nov
        if resume_data.get('skills'):
            content.append(r"\section{Technical Skills}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(r"\begin{onecolentry}")
                    content.append(rf"    \textbf{{{category}:}} {cls._escape_latex(items)}")
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.1 cm}")
                elif isinstance(skill, str):
                    content.append(r"\begin{onecolentry}")
                    content.append(cls._escape_latex(skill))
                    content.append(r"\end{onecolentry}")
                    content.append(r"\vspace{0.1 cm}")

        return "\n".join(content)

    @classmethod
    def _generate_ethan_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for Ethan template"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header
        content.append(r"\begin{center}")
        content.append(rf"  \textbf{{\LARGE\scshape {cls._escape_latex(info.get('name', 'Your Name'))}}} \\")
        content.append(r"  \vspace{1pt}\small")
        
        contact_items = []
        if info.get('location'):
            contact_items.append(cls._escape_latex(info['location']))
        if info.get('email'):
            email = cls._escape_latex(info['email'])
            contact_items.append(rf"\href{{mailto:{email}}}{{{email}}}")
        if info.get('phone'):
            contact_items.append(cls._escape_latex(info['phone']))
        if info.get('website'):
            website = cls._escape_latex(info['website'])
            contact_items.append(rf"\href{{https://{website}}}{{{website}}}")
        if info.get('github'):
            github = cls._escape_latex(info['github'])
            username = github.replace('github.com/', '').replace('https://', '').replace('www.', '')
            contact_items.append(rf"\href{{https://github.com/{username}}}{{GitHub}}")
        if info.get('linkedin'):
            linkedin = cls._escape_latex(info['linkedin'])
            username = linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
            contact_items.append(rf"\href{{https://linkedin.com/in/{username}}}{{LinkedIn}}")
            
        content.append(r"  $\ \diamond\ $ ".join(contact_items))
        content.append(r"\end{center}")

        # Summary (Ethan template doesn't have a standard summary section, but we can add one)
        if resume_data.get('summary'):
            content.append(r"\section{Summary}")
            content.append(cls._escape_latex(resume_data['summary']))

        # Experience
        if resume_data.get('experience'):
            content.append(r"\section{Professional Experience}")
            content.append(r"\cvheadingstart")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} - {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                location = cls._escape_latex(exp.get('location', ''))
                
                content.append(r"  \cvheading")
                content.append(rf"    {{{company}}}{{{location}}}")
                content.append(rf"    {{{position}}}{{{dates}}}")
                
                if exp.get('description'):
                    content.append(r"  \cvitemstart")
                    for item in exp['description']:
                        content.append(rf"    \cvitem{{{cls._escape_latex(item)}}}")
                    content.append(r"  \cvitemend")
            content.append(r"\cvheadingend")

        # Education
        if resume_data.get('education'):
            content.append(r"\section{Education}")
            content.append(r"\cvheadingstart")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} - {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                full_degree = f"{degree} in {field}" if field else degree
                location = cls._escape_latex(edu.get('location', ''))
                
                content.append(r"  \cvheading")
                content.append(rf"    {{{institution}}}{{{location}}}")
                content.append(rf"    {{{full_degree}}}{{{dates}}}")
            content.append(r"\cvheadingend")

        # Skills
        if resume_data.get('skills'):
            content.append(r"\section{Technical Skills}")
            content.append(r"\begin{itemize}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(rf"\item \textbf{{{category}:}} {cls._escape_latex(items)}")
                elif isinstance(skill, str):
                    content.append(rf"\item {cls._escape_latex(skill)}")
            content.append(r"\end{itemize}")

        # Projects
        if resume_data.get('projects'):
            content.append(r"\section{Projects}")
            content.append(r"\cvheadingstart")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                
                content.append(r"  \item")
                content.append(rf"    \textbf{{{name}}}")
                
                if proj.get('description') or proj.get('highlights'):
                    content.append(r"  \cvitemstart")
                    if proj.get('description'):
                        content.append(rf"    \cvitem{{{cls._escape_latex(proj['description'])}}}")
                    
                    highlights = proj.get('highlights')
                    if isinstance(highlights, list):
                        for h in highlights:
                            content.append(rf"    \cvitem{{{cls._escape_latex(h)}}}")
                    elif isinstance(highlights, str):
                         items = [h.strip() for h in highlights.split('•') if h.strip()]
                         for item in items:
                             content.append(rf"    \cvitem{{{cls._escape_latex(item)}}}")
                    content.append(r"  \cvitemend")
            content.append(r"\cvheadingend")

        return "\n".join(content)

    @classmethod
    def _generate_autocv_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for AutoCV template"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header
        content.append(r"\begin{tabularx}{\linewidth}{@{} C @{}}")
        content.append(rf"\Huge{{{cls._escape_latex(info.get('name', 'Your Name'))}}} \\[7.5pt]")
        
        contact_items = []
        if info.get('location'):
            location = cls._escape_latex(info['location'])
            contact_items.append(rf"{location}")
        if info.get('github'):
            github = cls._escape_latex(info['github'])
            username = github.replace('github.com/', '').replace('https://', '').replace('www.', '')
            contact_items.append(rf"\href{{https://github.com/{username}}}{{\raisebox{{-0.05\height}}\faGithub\ {username}}}")
        if info.get('linkedin'):
            linkedin = cls._escape_latex(info['linkedin'])
            username = linkedin.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
            contact_items.append(rf"\href{{https://linkedin.com/in/{username}}}{{\raisebox{{-0.05\height}}\faLinkedin\ {username}}}")
        if info.get('website'):
            website = cls._escape_latex(info['website'])
            contact_items.append(rf"\href{{https://{website}}}{{\raisebox{{-0.05\height}}\faGlobe \ {website}}}")
        if info.get('email'):
            email = cls._escape_latex(info['email'])
            contact_items.append(rf"\href{{mailto:{email}}}{{\raisebox{{-0.05\height}}\faEnvelope \ {email}}}")
        if info.get('phone'):
            phone = cls._escape_latex(info['phone'])
            contact_items.append(rf"\href{{tel:{phone}}}{{\raisebox{{-0.05\height}}\faMobile \ {phone}}}")
            
        content.append(r" \ $|$ \ ".join(contact_items) + r" \\")
        content.append(r"\end{tabularx}")

        # Summary
        if resume_data.get('summary'):
            content.append(r"\section{Summary}")
            content.append(cls._escape_latex(resume_data['summary']))

        # Experience
        if resume_data.get('experience'):
            content.append(r"\section{Work Experience}")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} - {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                
                if exp.get('description'):
                    content.append(rf"\begin{{joblong}}{{{position} at {company}}}{{{dates}}}")
                    for item in exp['description']:
                        content.append(rf"\item {cls._escape_latex(item)}")
                    content.append(r"\end{joblong}")
                else:
                    content.append(rf"\begin{{jobshort}}{{{position} at {company}}}{{{dates}}}")
                    content.append(r"\end{jobshort}")

        # Projects
        if resume_data.get('projects'):
            content.append(r"\section{Projects}")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                url = cls._escape_latex(proj.get('url', ''))
                desc = cls._escape_latex(proj.get('description', ''))
                
                content.append(r"\begin{tabularx}{\linewidth}{ @{}l r@{} }")
                if url:
                    content.append(rf"\textbf{{{name}}} & \hfill \href{{{url}}}{{Link}} \\[3.75pt]")
                else:
                    content.append(rf"\textbf{{{name}}} & \hfill \\[3.75pt]")
                content.append(rf"\multicolumn{{2}}{{@{{}}X@{{}}}}{{{desc}}}  \\")
                content.append(r"\end{tabularx}")

        # Education
        if resume_data.get('education'):
            content.append(r"\section{Education}")
            content.append(r"\begin{tabularx}{\linewidth}{@{}l X@{}}")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} - {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                full_degree = f"{degree} in {field}" if field else degree
                gpa = f"(GPA: {cls._escape_latex(edu['gpa'])})" if edu.get('gpa') else ""
                
                content.append(rf"{dates} & {full_degree} at \textbf{{{institution}}} \hfill \normalsize {gpa} \\")
            content.append(r"\end{tabularx}")

        # Skills
        if resume_data.get('skills'):
            content.append(r"\section{Skills}")
            content.append(r"\begin{tabularx}{\linewidth}{@{}l X@{}}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(rf"{category} & \normalsize{{{cls._escape_latex(items)}}}\\\\")
                elif isinstance(skill, str):
                    content.append(rf"Skill & \normalsize{{{cls._escape_latex(skill)}}}\\\\")
            content.append(r"\end{tabularx}")

        content.append(r"\vfill")
        content.append(r"\center{\footnotesize Last updated: \today}")
        
        return "\n".join(content)

    @classmethod
    def _generate_anticv_body(cls, resume_data: Dict[str, Any]) -> str:
        """Generate body content for Anti-CV template"""
        content = []
        info = resume_data.get('personal_info', {})
        
        # Header
        name = cls._escape_latex(info.get('name', 'Your Name'))
        phone = cls._escape_latex(info.get('phone', ''))
        email = cls._escape_latex(info.get('email', ''))
        location = cls._escape_latex(info.get('location', ''))
        
        website_url = info.get('website', '')
        website_display = website_url.replace('https://', '').replace('www.', '')
        website_tex = rf"\href{{{website_url}}}{{{cls._escape_latex(website_display)}}}" if website_url else ""
        
        github_url = info.get('github', '')
        github_display = github_url.replace('https://', '').replace('www.', '')
        github_tex = rf"\href{{{github_url}}}{{{cls._escape_latex(github_display)}}}" if github_url else ""

        linkedin_url = info.get('linkedin', '')
        linkedin_display = linkedin_url.replace('linkedin.com/in/', '').replace('https://', '').replace('www.', '')
        linkedin_tex = rf"\href{{{linkedin_url}}}{{{cls._escape_latex(linkedin_display)}}}" if linkedin_url else ""
        
        # Manually construct header to include all fields and replace "Anti Curriculum Vitae" text
        content.append(r"{\Huge \usefont{OT1}{phv}{m}{n} \textbf{" + name + r"}}")
        content.append(r"{\large \usefont{OT1}{phv}{m}{n} \hfill " + phone + r"\hspace{25pt}" + email + r"}")
        
        content.append(r"\par \vspace{5pt}")
        
        second_line_items = []
        if location:
            second_line_items.append(rf"\textit{{{location}}}")
        else:
            second_line_items.append(r"\textit{Curriculum Vitae}")
            
        links = []
        if website_tex: links.append(rf"\textit{{website }} {website_tex}")
        if github_tex: links.append(rf"\textit{{github }} {github_tex}")
        if linkedin_tex: links.append(rf"\textit{{linkedin }} {linkedin_tex}")
        
        if links:
            content.append(second_line_items[0] + r"\hfill " + r"\hspace{25pt}".join(links))
        else:
            content.append(second_line_items[0])
            
        content.append(r"\par \normalsize \normalfont")
        content.append(r"\sepspace")

        # Summary
        if resume_data.get('summary'):
            content.append(r"\NewPart{Summary}{}")
            content.append(r"\begin{itemize}")
            content.append(rf"    \item {cls._escape_latex(resume_data['summary'])}")
            content.append(r"\end{itemize}")
            content.append(r"\sepspace")

        # Experience
        if resume_data.get('experience'):
            content.append(r"\NewPart{Work Experience}{}")
            content.append(r"\begin{itemize}")
            for exp in resume_data['experience']:
                dates = f"{cls._escape_latex(exp.get('start_date', ''))} -- {cls._escape_latex(exp.get('end_date', 'Present'))}"
                company = cls._escape_latex(exp.get('company', ''))
                position = cls._escape_latex(exp.get('position', ''))
                location = cls._escape_latex(exp.get('location', ''))
                
                content.append(rf"    \item \textbf{{{position}}} at \textbf{{{company}}}, {location} ({dates})")
                
                if exp.get('description'):
                    content.append(r"    \begin{itemize}")
                    for item in exp['description']:
                        content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{itemize}")
            content.append(r"\end{itemize}")
            content.append(r"\sepspace")

        # Education
        if resume_data.get('education'):
            content.append(r"\NewPart{Education}{}")
            content.append(r"\begin{itemize}")
            for edu in resume_data['education']:
                dates = f"{cls._escape_latex(edu.get('start_date', ''))} -- {cls._escape_latex(edu.get('end_date', 'Present'))}"
                institution = cls._escape_latex(edu.get('institution', ''))
                degree = cls._escape_latex(edu.get('degree', ''))
                field = cls._escape_latex(edu.get('field_of_study', ''))
                full_degree = f"{degree} in {field}" if field else degree
                
                content.append(rf"    \item \textbf{{{institution}}}, {full_degree} ({dates})")
                if edu.get('gpa'):
                    content.append(rf"    \item GPA: {cls._escape_latex(edu['gpa'])}")
            content.append(r"\end{itemize}")
            content.append(r"\sepspace")

        # Projects
        if resume_data.get('projects'):
            content.append(r"\NewPart{Projects}{}")
            content.append(r"\begin{itemize}")
            for proj in resume_data['projects']:
                name = cls._escape_latex(proj.get('name', ''))
                content.append(rf"    \item \textbf{{{name}}}")
                
                if proj.get('description'):
                    content.append(rf"    -- {cls._escape_latex(proj['description'])}")
                
                if proj.get('highlights'):
                    content.append(r"    \begin{itemize}")
                    highlights = proj.get('highlights')
                    if isinstance(highlights, list):
                        for h in highlights:
                            content.append(rf"        \item {cls._escape_latex(h)}")
                    elif isinstance(highlights, str):
                         items = [h.strip() for h in highlights.split('•') if h.strip()]
                         for item in items:
                             content.append(rf"        \item {cls._escape_latex(item)}")
                    content.append(r"    \end{itemize}")
            content.append(r"\end{itemize}")
            content.append(r"\sepspace")

        # Skills
        if resume_data.get('skills'):
            content.append(r"\NewPart{Skills}{}")
            for skill in resume_data['skills']:
                if isinstance(skill, dict) and 'category' in skill:
                    category = cls._escape_latex(skill['category'])
                    items = ", ".join(skill['items'])
                    content.append(rf"\SkillsEntry{{{category}}}{{{cls._escape_latex(items)}}}")
                elif isinstance(skill, str):
                    content.append(rf"\SkillsEntry{{Skill}}{{{cls._escape_latex(skill)}}}")
            content.append(r"\sepspace")

        return "\n".join(content)

    @classmethod
    def inject_resume_data(cls, latex_content: str, resume_data: Dict[str, Any], theme_color: str = "#3B82F6", template_name: str = "auto_cv") -> str:
        """Inject resume data into LaTeX template"""
        
        # Extract preamble
        preamble_match = re.search(r'([\s\S]*?)\\begin\{document\}', latex_content)
        if not preamble_match:
            # Fallback to old method if structure is unexpected
            return cls._old_inject_resume_data(latex_content, resume_data, theme_color)
            
        preamble = preamble_match.group(1)
        
        # Generate body based on template type
        if template_name == 'rendercv_classic':
            body = cls._generate_rendercv_classic_body(resume_data)
        elif template_name == 'ethan':
            body = cls._generate_ethan_body(resume_data)
        elif template_name == 'auto_cv':
            body = cls._generate_autocv_body(resume_data)
        elif template_name == 'anti_cv':
            body = cls._generate_anticv_body(resume_data)
        else:
            # For other templates, fallback to old method for now
            # Ideally implement generators for them too
            return cls._old_inject_resume_data(latex_content, resume_data, theme_color)
            
        # Replace theme color in preamble
        if theme_color and theme_color != "#3B82F6":
            hex_color = theme_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            preamble = re.sub(
                r'\\definecolor\{primaryColor\}\{RGB\}\{\d+,\s*\d+,\s*\d+\}',
                rf'\\definecolor{{primaryColor}}{{RGB}}{{{r}, {g}, {b}}}',
                preamble
            )
            
        return f"{preamble}\\begin{{document}}\n{body}\n\\end{{document}}"

    @classmethod
    def _old_inject_resume_data(cls, latex_content: str, resume_data: Dict[str, Any], theme_color: str = "#3B82F6") -> str:
        """Legacy injection method for non-rendercv templates"""
        
        # Personal Info
        if resume_data.get('personal_info'):
            info = resume_data['personal_info']
            
            # Replace name
            if info.get('name'):
                latex_content = re.sub(
                    r'(\\name\{|\\textbf\{\\LARGE\\scshape |\\Huge\{|Your Name|Xiao Yuan|Jane Doe|John Doe)',
                    lambda m: m.group(1) + info['name'] if '\\' in m.group(1) else info['name'],
                    latex_content,
                    count=1
                )
            
            # Replace email
            if info.get('email'):
                latex_content = re.sub(
                    r'(\\email\{|\\href\{mailto:)[^}]+',
                    lambda m: m.group(1) + info['email'],
                    latex_content
                )
            
            # Replace phone
            if info.get('phone'):
                latex_content = re.sub(
                    r'(\\phone\{|\+\d{1,3}[- ]?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4})',
                    lambda m: m.group(1) if '\\' in m.group(1) else info['phone'],
                    latex_content
                )
            
            # Replace GitHub
            if info.get('github'):
                latex_content = re.sub(
                    r'(\\href\{https://github\.com/)[^}]+',
                    lambda m: m.group(1) + info['github'].replace('github.com/', ''),
                    latex_content
                )
            
            # Replace LinkedIn
            if info.get('linkedin'):
                latex_content = re.sub(
                    r'(\\href\{https://linkedin\.com/in/)[^}]+',
                    lambda m: m.group(1) + info['linkedin'].replace('linkedin.com/in/', ''),
                    latex_content
                )
        
        # Replace theme color if template supports it
        if theme_color and theme_color != "#3B82F6":
            # Convert hex to RGB
            hex_color = theme_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            latex_content = re.sub(
                r'\\definecolor\{primaryColor\}\{RGB\}\{\d+,\s*\d+,\s*\d+\}',
                rf'\\definecolor{{primaryColor}}{{RGB}}{{{r}, {g}, {b}}}',
                latex_content
            )
        
        return latex_content
    
    @classmethod
    def compile_latex(cls, latex_content: str) -> BytesIO:
        """Compile LaTeX content to PDF"""
        import logging
        logger = logging.getLogger(__name__)
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Write LaTeX file
            tex_file = tmpdir_path / "resume.tex"
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            logger.info(f"LaTeX file written to: {tex_file}")
            
            # Copy any required style files (like myresume.sty for yuan template)
            style_files = ['myresume.sty']
            for style_file in style_files:
                source = cls.TEMPLATES_DIR / style_file
                if source.exists():
                    dest = tmpdir_path / style_file
                    dest.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
                    logger.info(f"Copied style file: {style_file}")
            
            try:
                # Check if pdflatex is available
                pdflatex_check = subprocess.run(
                    ['pdflatex', '--version'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                logger.info(f"pdflatex version check: {pdflatex_check.returncode}")
                
                # Compile LaTeX (run twice for proper references)
                for i in range(2):
                    logger.info(f"Running pdflatex compilation pass {i+1}...")
                    result = subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'resume.tex'],
                        cwd=tmpdir_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=60
                    )
                    logger.info(f"pdflatex pass {i+1} returncode: {result.returncode}")
                    if result.returncode != 0:
                        logger.error(f"pdflatex stdout: {result.stdout.decode('utf-8', errors='ignore')[:500]}")
                        logger.error(f"pdflatex stderr: {result.stderr.decode('utf-8', errors='ignore')[:500]}")
                
                # Read the generated PDF
                pdf_file = tmpdir_path / "resume.pdf"
                if pdf_file.exists():
                    logger.info(f"PDF file generated successfully: {pdf_file}")
                    pdf_buffer = BytesIO(pdf_file.read_bytes())
                    pdf_buffer.seek(0)
                    return pdf_buffer
                else:
                    logger.error(f"PDF file not found at: {pdf_file}")
                    logger.error(f"Files in temp dir: {list(tmpdir_path.iterdir())}")
                    raise Exception("PDF file was not generated - pdflatex may not be installed or compilation failed")
                    
            except subprocess.TimeoutExpired:
                logger.error("LaTeX compilation timed out")
                raise Exception("LaTeX compilation timed out")
            except FileNotFoundError as e:
                logger.error(f"pdflatex not found: {str(e)}")
                raise Exception("pdflatex is not installed or not in PATH. Please install TeX Live or MiKTeX.")
            except Exception as e:
                logger.error(f"Compilation error: {str(e)}")
                # Try to read log file for error details
                log_file = tmpdir_path / "resume.log"
                if log_file.exists():
                    log_content = log_file.read_text(encoding='utf-8', errors='ignore')
                    # Extract error message
                    error_match = re.search(r'! (.+?)(?:\n|$)', log_content)
                    if error_match:
                        logger.error(f"LaTeX error from log: {error_match.group(1)}")
                        raise Exception(f"LaTeX compilation error: {error_match.group(1)}")
                raise Exception(f"LaTeX compilation failed: {str(e)}")
    
    @classmethod
    def generate(cls, resume_data: Dict[str, Any], template_name: str = "auto_cv", 
                theme_color: str = "#3B82F6") -> BytesIO:
        """Generate PDF from template and resume data"""
        
        # Get template path
        template_path = cls.get_template_path(template_name)
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        # Read template content
        latex_content = template_path.read_text(encoding='utf-8')
        
        # Inject resume data
        latex_content = cls.inject_resume_data(latex_content, resume_data, theme_color, template_name)
        
        # Compile to PDF
        return cls.compile_latex(latex_content)
