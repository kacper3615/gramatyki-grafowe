import os
import sys
from pathlib import Path
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from PIL import Image
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "Pillow"])
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from PIL import Image


def get_sorted_images(output_dir):
    """Get all PNG files sorted by iteration order."""
    images = []
    
    # Add starting graph first
    starting_graph = os.path.join(output_dir, "starting-graph.png")
    if os.path.exists(starting_graph):
        images.append(("Starting Graph", starting_graph))
    
    # Get all iteration images
    iteration_files = []
    for file in os.listdir(output_dir):
        if file.endswith('.png') and file != 'starting-graph.png':
            iteration_files.append(file)
    
    # Sort by iteration number
    iteration_files.sort()
    
    for file in iteration_files:
        # Extract production name from filename (e.g., "00-P9.png" -> "P9")
        name = file.replace('.png', '').split('-', 1)[-1] if '-' in file else file.replace('.png', '')
        images.append((name, os.path.join(output_dir, file)))
    
    return images


def create_pdf_report(output_dir, pdf_filename, authors, group_number):
    """Create PDF report with all iteration images.
    
    Args:
        output_dir: Directory containing output PNG files
        pdf_filename: Output PDF filename
        authors: List of author names
        group_number: Group number
    """
    images = get_sorted_images(output_dir)
    
    if not images:
        print(f"No images found in {output_dir}")
        return
    
    # Register fonts that support Polish characters
    try:
        # Try to use system fonts that support Polish characters
        pdfmetrics.registerFont(TTFont('DejaVuSans', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
        font_regular = 'DejaVuSans'
        font_bold = 'DejaVuSans-Bold'
    except:
        # Fallback to Helvetica (limited Polish support)
        font_regular = 'Helvetica'
        font_bold = 'Helvetica-Bold'
    
    # Create PDF
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    
    # Title page
    c.setFont(font_bold, 32)
    c.drawCentredString(width / 2, height - 5*cm, "Gramatyki grafowe – zadanie 2")
    
    c.setFont(font_regular, 16)
    y_position = height - 8*cm
    c.drawCentredString(width / 2, y_position, "Autorzy:")
    
    c.setFont(font_regular, 14)
    y_position -= 1.5*cm
    for author in authors:
        c.drawCentredString(width / 2, y_position, author)
        y_position -= 1*cm
    
    # Add group number
    y_position -= 1*cm
    c.setFont(font_regular, 14)
    c.drawCentredString(width / 2, y_position, f"Grupa: {group_number}")
    
    # Add date
    c.setFont(font_regular, 12)
    c.drawCentredString(width / 2, 3*cm, datetime.now().strftime("%d.%m.%Y"))
    
    c.showPage()
    
    # Add images
    for idx, (name, img_path) in enumerate(images):
        print(f"Adding image {idx+1}/{len(images)}: {name}")
        
        # Add image title
        c.setFont(font_bold, 14)
        c.drawCentredString(width / 2, height - 2*cm, f"{idx}. {name}")
        
        # Load and scale image
        img = Image.open(img_path)
        img_width, img_height = img.size
        
        # Calculate scaling to fit on page (leaving margins)
        max_width = width - 4*cm
        max_height = height - 6*cm
        
        scale = min(max_width / img_width, max_height / img_height)
        scaled_width = img_width * scale
        scaled_height = img_height * scale
        
        # Center image on page
        x = (width - scaled_width) / 2
        y = (height - scaled_height) / 2 - 1*cm
        
        # Draw image
        c.drawImage(img_path, x, y, width=scaled_width, height=scaled_height)
        
        c.showPage()
    
    c.save()
    print(f"\nPDF report saved to: {pdf_filename}")
    print(f"Total pages: {len(images) + 1} (1 title page + {len(images)} images)")


if __name__ == "__main__":
    output_dir = "./loops/outputs"
    
    # Prompt for authors
    print("=== PDF Report Generator ===")
    print("Enter author names (one per line, empty line to finish):")
    
    authors = []
    while True:
        author = input(f"Author {len(authors)+1}: ").strip()
        if not author:
            break
        authors.append(author)
    
    if not authors:
        print("No authors provided. Using default.")
        authors = ["Author Name"]

    group_number = input("Group number: ").strip()
    if not group_number:
        group_number = "N/A"
    
    # Create PDF
    pdf_filename = "./loops/raport_zadanie2.pdf"
    create_pdf_report(output_dir, pdf_filename, authors, group_number)