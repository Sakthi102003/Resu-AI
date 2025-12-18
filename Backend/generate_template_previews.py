"""
Generate preview images for all resume templates
This script generates actual PDFs from each template and converts them to images
"""

import os
import sys
from pathlib import Path
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from templates.template_manager import TemplateManager
from templates.sample_data import SAMPLE_RESUME

def generate_preview_images():
    """Generate preview images for all templates"""
    
    print("🎨 Generating Template Preview Images...\n")
    
    # Get all templates
    templates = TemplateManager.list_templates()
    
    # Output directory
    output_dir = Path(__file__).parent.parent / "Frontend" / "public" / "templates"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}\n")
    
    for template in templates:
        template_id = template['id']
        template_name = template['name']
        
        try:
            print(f"🔄 Generating {template_name} ({template_id})...")
            
            # Generate PDF
            pdf_buffer = TemplateManager.generate_resume(
                resume_data=SAMPLE_RESUME,
                template_name=template_id,
                theme_color=get_default_color(template_id)
            )
            
            # Save PDF
            pdf_path = output_dir / f"{template_id}.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            print(f"   ✅ Saved PDF: {pdf_path.name}")
            
            # Try to convert to PNG using available tools
            try:
                convert_pdf_to_image(pdf_path, output_dir, template_id)
            except Exception as e:
                print(f"   ⚠️  Could not convert to image: {e}")
                print(f"   💡 You can manually convert {template_id}.pdf to PNG")
            
        except Exception as e:
            print(f"   ❌ Error generating {template_name}: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("✨ Preview generation complete!")
    print(f"\n📂 Check the output directory: {output_dir}")
    print("\n💡 If PNG conversion failed, you can manually convert PDFs:")
    print("   1. Open each PDF")
    print("   2. Take a screenshot or use a PDF-to-image tool")
    print("   3. Save as {template_id}.png (600x800px recommended)")

def get_default_color(template_id):
    """Get default color for each template"""
    colors = {
        'auto_cv': '#3B82F6',
        'anti_cv': '#8B5CF6',
        'ethan': '#3B82F6',
        'rendercv_classic': '#1e40af',
        'rendercv_engineering': '#10B981',
        'rendercv_sb2nov': '#3B82F6',
        'yuan': '#6366F1'
    }
    return colors.get(template_id, '#3B82F6')

def convert_pdf_to_image(pdf_path, output_dir, template_id):
    """
    Convert PDF to PNG image
    Tries multiple methods in order of preference
    """
    png_path = output_dir / f"{template_id}.png"
    
    # Method 1: Try pdf2image (requires poppler)
    try:
        from pdf2image import convert_from_path
        from PIL import Image
        images = convert_from_path(str(pdf_path), dpi=150, first_page=1, last_page=1)
        if images:
            # Resize to standard size
            img = images[0]
            img.thumbnail((600, 800), Image.LANCZOS)
            img.save(png_path, 'PNG')
            print(f"   ✅ Saved PNG: {png_path.name}")
            return
    except ImportError:
        pass
    except Exception as e:
        print(f"   ⚠️  pdf2image failed: {e}")
    
    # Method 2: Try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        page = doc[0]
        
        # Render at 2x resolution then scale down
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        from PIL import Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Resize to target size
        img.thumbnail((600, 800), Image.LANCZOS)
        img.save(png_path, 'PNG')
        doc.close()
        
        print(f"   ✅ Saved PNG: {png_path.name}")
        return
    except ImportError:
        pass
    except Exception as e:
        print(f"   ⚠️  PyMuPDF failed: {e}")
    
    # Method 3: Try Pillow with ReportLab (if available)
    try:
        from PIL import Image
        # This method requires additional setup
        raise NotImplementedError("Manual conversion needed")
    except:
        pass
    
    # If all methods fail
    raise Exception("No PDF-to-image converter available. Install: pip install pdf2image Pillow PyMuPDF")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║         📄 Template Preview Generator                        ║
║                                                              ║
║  This script generates preview images for all templates     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        generate_preview_images()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
