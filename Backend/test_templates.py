"""
Test script for resume templates
Generates sample PDFs for all templates
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templates.template_manager import TemplateManager
from templates.sample_data import get_sample_resume


def test_all_templates():
    """Generate PDFs for all templates with sample data"""
    
    # Create output directory
    output_dir = "template_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get sample data
    resume_data = get_sample_resume('full')
    
    # Get all templates
    templates = TemplateManager.list_templates()
    
    print("🎨 Generating sample resumes for all templates...\n")
    
    for template in templates:
        template_id = template['id']
        template_name = template['name']
        
        try:
            print(f"Generating: {template_name} ({template_id})...")
            
            # Generate PDF
            pdf_buffer = TemplateManager.generate_resume(
                resume_data=resume_data,
                template_name=template_id,
                theme_color="#3B82F6"
            )
            
            # Save to file
            output_file = os.path.join(output_dir, f"{template_id}.pdf")
            with open(output_file, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            print(f"✅ Generated: {output_file}")
            
        except Exception as e:
            print(f"❌ Error generating {template_name}: {str(e)}")
    
    print(f"\n✨ Done! Check the '{output_dir}' directory for generated PDFs.")


def test_single_template(template_id, resume_type='full', theme_color='#3B82F6'):
    """Generate PDF for a single template"""
    
    resume_data = get_sample_resume(resume_type)
    
    print(f"Generating {template_id} with {resume_type} resume data...")
    
    try:
        pdf_buffer = TemplateManager.generate_resume(
            resume_data=resume_data,
            template_name=template_id,
            theme_color=theme_color
        )
        
        output_file = f"test_{template_id}_{resume_type}.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print(f"✅ Generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def list_available_templates():
    """List all available templates"""
    templates = TemplateManager.list_templates()
    
    print("\n📋 Available Resume Templates:\n")
    print("-" * 80)
    
    for template in templates:
        print(f"ID: {template['id']}")
        print(f"Name: {template['name']}")
        print(f"Description: {template['description']}")
        print(f"Best For: {template['best_for']}")
        print("-" * 80)


def test_theme_colors():
    """Test templates with different theme colors"""
    
    template_id = 'auto_cv'
    resume_data = get_sample_resume('full')
    
    colors = {
        'blue': '#3B82F6',
        'green': '#10B981',
        'purple': '#8B5CF6',
        'red': '#EF4444',
        'orange': '#F59E0B'
    }
    
    output_dir = "color_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎨 Testing {template_id} with different colors...\n")
    
    for color_name, color_hex in colors.items():
        try:
            pdf_buffer = TemplateManager.generate_resume(
                resume_data=resume_data,
                template_name=template_id,
                theme_color=color_hex
            )
            
            output_file = os.path.join(output_dir, f"{template_id}_{color_name}.pdf")
            with open(output_file, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            print(f"✅ Generated {color_name} variant: {output_file}")
            
        except Exception as e:
            print(f"❌ Error with {color_name}: {str(e)}")
    
    print(f"\n✨ Done! Check the '{output_dir}' directory.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test resume templates')
    parser.add_argument('--template', '-t', help='Specific template to test')
    parser.add_argument('--resume', '-r', default='full', 
                       choices=['full', 'minimal', 'creative', 'academic'],
                       help='Type of resume data to use')
    parser.add_argument('--color', '-c', default='#3B82F6', 
                       help='Theme color (hex format)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available templates')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Generate all templates')
    parser.add_argument('--colors', action='store_true',
                       help='Test different color themes')
    
    args = parser.parse_args()
    
    if args.list:
        list_available_templates()
    elif args.all:
        test_all_templates()
    elif args.colors:
        test_theme_colors()
    elif args.template:
        test_single_template(args.template, args.resume, args.color)
    else:
        print("Resume Template Tester")
        print("=" * 50)
        print("\nUsage:")
        print("  python test_templates.py --all              # Generate all templates")
        print("  python test_templates.py --list             # List templates")
        print("  python test_templates.py -t auto_cv         # Test single template")
        print("  python test_templates.py -t yuan -r minimal # Test with minimal data")
        print("  python test_templates.py --colors           # Test color themes")
        print("\nOptions:")
        print("  -t, --template    Template ID to test")
        print("  -r, --resume      Resume type (full, minimal, creative, academic)")
        print("  -c, --color       Theme color in hex format")
        print("  -l, --list        List all available templates")
        print("  -a, --all         Generate all templates")
        print("  --colors          Test different color themes")
