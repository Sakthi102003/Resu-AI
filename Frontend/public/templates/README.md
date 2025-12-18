# Template Preview Images

This folder contains **real preview images** generated from actual resume templates.

## 📁 Current Files

✅ **PNG Images** (Used by the app):
- `auto_cv.png` - Auto CV template preview
- `anti_cv.png` - Anti CV template preview  
- `ethan.png` - Ethan's Resume template preview
- `rendercv_classic.png` - RenderCV Classic template preview
- `rendercv_engineering.png` - RenderCV Engineering template preview
- `rendercv_sb2nov.png` - RenderCV sb2nov template preview
- `yuan.png` - Yuan's Resume template preview

📄 **PDF Files** (Source files):
- `*.pdf` - Full-quality PDF versions of each template

## 🔄 How to Regenerate Preview Images

When you update or add templates, regenerate the preview images:

### Method 1: Automated Script (Recommended)

```bash
cd Backend
python generate_template_previews.py
```

This script will:
1. Generate PDFs from all templates using sample data
2. Convert PDFs to PNG images automatically
3. Save both PDF and PNG versions to this folder

### Method 2: Manual Generation

If the script doesn't work:

1. **Generate PDFs:**
   - Run the backend server
   - Use the `/templates/{template_id}/preview` API endpoint
   - Or run individual template classes with sample data

2. **Convert to Images:**
   - Open each PDF in a PDF viewer
   - Export/screenshot the first page
   - Resize to **600x800px** (portrait)
   - Save as `{template_id}.png`

## 🛠️ Dependencies

The automated script requires:
```bash
pip install PyMuPDF Pillow pdf2image
```

These are already in `Backend/requirements.txt`

## 📐 Image Specifications

- **Format:** PNG (24-bit RGB)
- **Recommended Size:** 600x800px (3:4 aspect ratio)
- **DPI:** 150 (for print quality)
- **Background:** White
- **Compression:** Moderate (balance quality/size)

## 🎨 Sample Data

Preview images use sample data from `Backend/templates/sample_data.py`:
- Full name: Alex Johnson
- Role: Senior Software Engineer
- Includes: Experience, Education, Skills, Projects, Certifications

## ✨ Tips

- **Keep images up-to-date:** Regenerate when template designs change
- **Consistent sizing:** All images should be same dimensions
- **Quality matters:** These are the first thing users see
- **Test fallback:** Icon emoji appears if image fails to load
- **File size:** Keep PNGs under 200KB each for fast loading

## 📝 Adding New Templates

When adding a new template:

1. Create the template class in `Backend/templates/`
2. Add it to `TemplateManager.TEMPLATES` dictionary
3. Run `generate_template_previews.py`
4. Verify the new PNG appears in this folder
5. Test in the frontend Template Selection page

---

**Last Generated:** Check file timestamps for last update date
