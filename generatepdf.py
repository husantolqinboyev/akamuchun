#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Generator for "عين الطالب" (Talabaning ko'zlari) Arabic Textbook
This script converts Markdown chapters to PDF format and saves them in the book/ directory.
It utilizes Microsoft Edge or Google Chrome in headless mode for zero-dependency high-fidelity PDF rendering.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Check if required libraries are available, if not, install them
try:
    from markdown import markdown
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'markdown'])
    from markdown import markdown


def find_browser():
    """Find Google Chrome or Microsoft Edge executable on Windows."""
    # 1. Try standard Windows paths
    paths = [
        # Microsoft Edge
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        # Google Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\x86\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    
    for path in paths:
        if os.path.exists(path):
            return path
            
    # 2. Try to find in PATH
    for cmd in ["msedge", "chrome", "google-chrome"]:
        path = shutil.which(cmd)
        if path:
            return path
            
    return None


def get_arabic_css():
    """Return CSS styles optimized for Arabic text rendering."""
    return """
    @page {
        margin: 2cm;
        size: A4;
    }
    
    body {
        font-family: 'Outfit', 'Amiri', 'Traditional Arabic', 'Arabic Typesetting', 'Scheherazade', serif;
        font-size: 13pt;
        line-height: 1.8;
        direction: ltr;
        color: #2d3748;
        background-color: #ffffff;
    }
    
    h1 {
        font-family: 'Outfit', 'Amiri', sans-serif;
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
        font-family: 'Outfit', 'Amiri', sans-serif;
        font-size: 18pt;
        color: #2e8b57;
        margin-top: 25px;
        border-left: 4px solid #2e8b57;
        padding-left: 10px;
    }
    
    h3 {
        font-family: 'Outfit', 'Amiri', sans-serif;
        font-size: 15pt;
        color: #4682b4;
        margin-top: 20px;
    }
    
    /* Ensure all Arabic content has proper shaping and sizing */
    .arabic-text, [dir="rtl"] {
        font-family: 'Amiri', 'Traditional Arabic', 'Scheherazade', serif;
        font-size: 18pt;
        direction: rtl;
        text-align: right;
        font-weight: bold;
        line-height: 1.6;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        page-break-inside: avoid;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    }
    
    th, td {
        border: 1px solid #e2e8f0;
        padding: 12px 15px;
        text-align: left;
    }
    
    th {
        background-color: #1a5f7a;
        color: white;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        font-size: 11pt;
    }
    
    tr:nth-child(even) {
        background-color: #f7fafc;
    }
    
    /* Table cells containing Arabic */
    td:first-child {
        font-size: 15pt;
        font-weight: bold;
    }
    
    blockquote {
        border-left: 4px solid #2e8b57;
        margin: 20px 0;
        padding: 12px 20px;
        background-color: #f7fafc;
        font-style: normal;
        border-radius: 0 8px 8px 0;
    }
    
    .note {
        border-left: 4px solid #ff6b6b;
        background-color: #fff5f5;
        padding: 12px 15px;
        margin: 20px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .qr-placeholder {
        border: 2px dashed #a0aec0;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #edf2f7;
        border-radius: 8px;
        font-family: 'Outfit', sans-serif;
    }
    
    code {
        background-color: #edf2f7;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 90%;
        color: #e53e3e;
    }
    
    pre {
        background-color: #1a202c;
        color: #f7fafc;
        padding: 15px;
        border-radius: 8px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 30px;
    }
    
    li {
        margin: 6px 0;
    }
    
    .transliteration {
        font-style: italic;
        color: #718096;
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
    
    # Create full HTML document with remote Google Fonts loaded
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>عين الطالب - Arab tili darsligi</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400;1,700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            {get_arabic_css()}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    return full_html


def generate_pdf(md_file_path, output_pdf_path):
    """Generate PDF from markdown file using headless Microsoft Edge or Chrome."""
    print(f"Converting: {md_file_path}")
    
    browser_path = find_browser()
    if not browser_path:
        print("[ERROR] Microsoft Edge or Google Chrome was not found on this system.")
        print("Please ensure you have Microsoft Edge or Google Chrome installed.")
        return False
        
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(md_file_path)
    
    # Write styled HTML content to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(html_content)
        temp_html_path = temp_file.name
        
    # Standardize path as file URL
    temp_file_url = Path(temp_html_path).absolute().as_uri()
    
    success = False
    try:
        # Print HTML to PDF using browser headless mode
        cmd = [
            browser_path,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf_path}",
            temp_file_url
        ]
        
        # Run printing subprocess
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] Created: {output_pdf_path}")
        success = True
    except subprocess.CalledProcessError:
        # Fallback to older headless syntax if browser version is older
        try:
            print("   Retrying with older headless mode...")
            cmd[1] = "--headless=old"
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[SUCCESS] Created: {output_pdf_path}")
            success = True
        except Exception as fallback_err:
            print(f"[ERROR] Generating PDF: {output_pdf_path}")
            print(f"   Browser printing failed: {fallback_err}")
    except Exception as e:
        print(f"[ERROR] Starting browser process: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_html_path):
            try:
                os.remove(temp_html_path)
            except Exception:
                pass
                
    return success


def main():
    """Main function to process all chapter files."""
    # Dynamically find the workspace directory (parent of this script)
    workspace_dir = Path(__file__).parent.absolute()
    book_dir = workspace_dir / 'book'
    
    # Ensure book directory exists
    book_dir.mkdir(exist_ok=True)
    
    # Find all markdown chapter files
    chapter_files = sorted(workspace_dir.glob('chapter_*.md'))
    
    if not chapter_files:
        print("[WARNING] No chapter files found (chapter_*.md)")
        print(f"Looked in directory: {workspace_dir}")
        print("Please create chapter files first.")
        return
    
    print(f"\nFound {len(chapter_files)} chapter(s) to process:\n")
    
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
    print(f"Summary: {success_count}/{len(chapter_files)} chapters converted successfully")
    print(f"PDF files saved to: {book_dir.absolute()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
