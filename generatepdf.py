#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Generator for "عين الطالب" (Talabaning ko'zlari) Arabic Textbook
This script converts Markdown chapters to PDF format and saves them in the book/ directory.
"""

import os
from pathlib import Path

# Check if required libraries are available, if not, install them
try:
    from markdown import markdown
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'markdown'])
    from markdown import markdown

try:
    from weasyprint import HTML, CSS
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'weasyprint'])
    from weasyprint import HTML, CSS


def get_arabic_css():
    """Return CSS styles optimized for Arabic text rendering."""
    return """
    @page {
        margin: 2cm;
        size: A4;
    }
    
    body {
        font-family: 'Traditional Arabic', 'Arabic Typesetting', 'Scheherazade', serif;
        font-size: 14pt;
        line-height: 1.8;
        direction: ltr;
    }
    
    h1 {
        font-size: 24pt;
        color: #1a5f7a;
        border-bottom: 3px solid #1a5f7a;
        padding-bottom: 10px;
        margin-top: 30px;
        page-break-before: always;
    }
    
    h1:first-of-type {
        page-break-before: avoid;
    }
    
    h2 {
        font-size: 20pt;
        color: #2e8b57;
        margin-top: 25px;
    }
    
    h3 {
        font-size: 16pt;
        color: #4682b4;
        margin-top: 20px;
    }
    
    .arabic-text {
        font-size: 18pt;
        direction: rtl;
        text-align: right;
        font-weight: bold;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    th {
        background-color: #1a5f7a;
        color: white;
        font-weight: bold;
    }
    
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    blockquote {
        border-left: 4px solid #2e8b57;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #f9f9f9;
        font-style: italic;
    }
    
    .note {
        border-left: 4px solid #ff6b6b;
        background-color: #fff5f5;
        padding: 10px 15px;
        margin: 15px 0;
    }
    
    .qr-placeholder {
        border: 2px dashed #666;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #f0f0f0;
    }
    
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    pre {
        background-color: #2d2d2d;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 5px 0;
    }
    
    .transliteration {
        font-style: italic;
        color: #666;
    }
    
    strong {
        color: #1a5f7a;
    }
    
    em {
        color: #2e8b57;
    }
    """


def convert_markdown_to_html(md_file_path):
    """Convert markdown file to HTML with proper styling."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_body = markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
    
    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>عين الطالب - Arab tili darsligi</title>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    return full_html


def generate_pdf(md_file_path, output_pdf_path):
    """Generate PDF from markdown file using WeasyPrint."""
    print(f"📖 Converting: {md_file_path}")
    
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(md_file_path)
    
    # Generate PDF using WeasyPrint
    try:
        html_doc = HTML(string=html_content)
        css = CSS(string=get_arabic_css())
        html_doc.write_pdf(output_pdf_path, stylesheets=[css])
        print(f"✅ Successfully created: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating PDF: {output_pdf_path}")
        print(f"   Error details: {str(e)}")
        return False


def main():
    """Main function to process all chapter files."""
    workspace_dir = Path('/workspace')
    book_dir = workspace_dir / 'book'
    
    # Ensure book directory exists
    book_dir.mkdir(exist_ok=True)
    
    # Find all markdown chapter files
    chapter_files = sorted(workspace_dir.glob('chapter_*.md'))
    
    if not chapter_files:
        print("⚠️  No chapter files found (chapter_*.md)")
        print("Please create chapter files first.")
        return
    
    print(f"\n📚 Found {len(chapter_files)} chapter(s) to process:\n")
    
    success_count = 0
    for chapter_file in chapter_files:
        # Create output filename
        output_filename = chapter_file.stem.replace('_', '-').replace('chapter', 'Chapter') + '.pdf'
        output_path = book_dir / output_filename
        
        # Generate PDF
        if generate_pdf(str(chapter_file), str(output_path)):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 Summary: {success_count}/{len(chapter_files)} chapters converted successfully")
    print(f"📁 PDF files saved to: {book_dir.absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()