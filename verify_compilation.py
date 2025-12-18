import subprocess
import os

def compile_latex(file_path):
    print(f"Compiling {file_path}...")
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', file_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(file_path)
        )
        if result.returncode == 0:
            print(f"SUCCESS: {file_path} compiled successfully.")
            return True
        else:
            print(f"FAILURE: {file_path} failed to compile.")
            print("Stdout:", result.stdout[:500])
            print("Stderr:", result.stderr[:500])
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

templates_dir = r's:\ResuAI\Templates'
templates = [
    'autocv.tex',
    'anticv.tex',
    'ethan.tex',
    'rendercv_classic.tex',
    'rendercv_engineering.tex',
    'rendercv_sb2nov.tex'
]

for template in templates:
    compile_latex(os.path.join(templates_dir, template))
