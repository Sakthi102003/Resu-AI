from templates.template_manager import TemplateManager
from templates.sample_data import SAMPLE_RESUME

print("Generating rendercv_classic template...")
pdf = TemplateManager.generate_resume(SAMPLE_RESUME, 'rendercv_classic', '#1e40af')

with open('test_debug.pdf', 'wb') as f:
    f.write(pdf.getvalue())

print("Created test_debug.pdf")
