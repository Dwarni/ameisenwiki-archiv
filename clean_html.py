import sys
import re
from pathlib import Path

def clean_html(path):
    file = Path(path)
    
    # Tiefe relativ zum Arbeitsverzeichnis berechnen
    depth = len(file.parent.parts)
    css_path = "../" * depth + "style.css"
    
    content = file.read_text(encoding="utf-8", errors="ignore")
    
    # Scripts entfernen
    content = re.sub(r'\s*<script[^>]*>.*?</script>\s*', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Beide stylesheet-Links durch einen einzigen ersetzen
    content = re.sub(r'<link[^>]*load\.php[^>]*skins\.vector\.styles\.legacy[^>]*/>', f'<link rel="stylesheet" href="{css_path}"/>', content)
    content = re.sub(r'\s*<link[^>]*load\.php[^>]*site\.styles[^>]*/>\s*', '', content)
    
    file.write_text(content, encoding="utf-8")
    print(f"Cleaned: {file} (css: {css_path})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_html.py <datei.html>")
        print("       python clean_html.py all")
        sys.exit(1)
    
    if sys.argv[1] == "all":
        files = list(Path(".").rglob("*.html"))
        print(f"Gefunden: {len(files)} HTML-Dateien")
        for f in files:
            clean_html(f)
        print("Fertig!")
    else:
        clean_html(sys.argv[1])