#!/usr/bin/env python3
"""Convert Markdown posts to HTML using the site template."""
import os, re, markdown

POSTS_DIR = "posts"
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - CAIO 部落格</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.8; color: #333; }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #0066cc; padding-bottom: 15px; }}
        h2 {{ color: #2c3e50; margin-top: 30px; }}
        p {{ margin: 15px 0; }}
        .back {{ display: inline-block; margin-bottom: 20px; color: #0066cc; text-decoration: none; }}
        .back:hover {{ text-decoration: underline; }}
        hr {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
    </style>
</head>
<body>
    <a href="../index.html" class="back">← 返回首頁</a>
    <h1>{title}</h1>
{content}
</body>
</html>"""

def process_file(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first H1
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(md_path)

    # Remove the H1 from content
    md_content = re.sub(r'^#\s+.+\n', '', md_content, count=1, flags=re.MULTILINE)

    # Remove footnotes or references at bottom
    md_content = re.sub(r'\*\*準備好.*sit\?\*\*.*', '', md_content, flags=re.DOTALL)
    md_content = re.sub(r'\*Eagle.*$', '', md_content, flags=re.MULTILINE)

    # Convert markdown
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # Build HTML
    html = TEMPLATE.format(title=title, content=html_content)

    # Write output
    basename = os.path.splitext(os.path.basename(md_path))[0]
    html_path = os.path.join(os.path.dirname(md_path), f"{basename}.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {html_path}")

if __name__ == "__main__":
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith('.md'):
            process_file(os.path.join(POSTS_DIR, fname))
    print("Done!")
