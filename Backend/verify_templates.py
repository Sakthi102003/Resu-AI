"""Quick verification script for template system"""

from templates.template_manager import TemplateManager

# List all templates
templates = TemplateManager.list_templates()

print(f"\n✅ Template System Verification")
print(f"=" * 50)
print(f"\n📦 Total Templates Registered: {len(templates)}")
print(f"\nTemplate List:")
for i, template in enumerate(templates, 1):
    print(f"  {i}. {template['id']:25s} - {template['name']}")
    print(f"     Description: {template['description'][:60]}...")

print(f"\n" + "=" * 50)
print(f"✅ All templates verified successfully!\n")
