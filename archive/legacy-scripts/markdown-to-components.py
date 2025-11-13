#!/usr/bin/env python3
"""
Markdown zu HTML-Komponenten Konverter für Robo4you Präsentationen

Verwendung:
    python markdown-to-components.py input.md [output-dir]
    
Beispiel:
    python markdown-to-components.py ../pitch/02_Validierte_Statistiken_Quellen.md output/
"""

import sys
import re
import os
from pathlib import Path
from typing import List, Dict, Tuple

class Component:
    def __init__(self, title: str = "", component_type: str = "section"):
        self.title = title
        self.type = component_type
        self.content = []
    
    def add_stat(self, text: str):
        self.content.append(("stat", text))
    
    def add_bullet(self, text: str):
        self.content.append(("bullet", text))
    
    def add_text(self, text: str):
        self.content.append(("text", text))
    
    def add_quote(self, text: str):
        self.content.append(("quote", text))
    
    def add_h3(self, text: str):
        self.content.append(("h3", text))

class Slide:
    def __init__(self, title: str):
        self.title = title
        self.components: List[Component] = []
    
    def add_component(self, component: Component):
        self.components.append(component)

def parse_markdown(markdown_text: str) -> List[Slide]:
    """Parst Markdown und gibt Liste von Slides zurück"""
    lines = markdown_text.split('\n')
    slides = []
    current_slide = None
    current_component = None
    
    for line in lines:
        stripped = line.strip()
        
        # Folie-Trenner
        if stripped == '---':
            if current_slide and current_component:
                current_slide.add_component(current_component)
                current_component = None
            continue
        
        # H1 = Neue Folie
        if line.startswith('# '):
            if current_slide and current_component:
                current_slide.add_component(current_component)
            if current_slide:
                slides.append(current_slide)
            
            title = line[2:].strip()
            current_slide = Slide(title)
            current_component = None
        
        # H2 = Neue Komponente
        elif line.startswith('## '):
            if current_component and current_slide:
                current_slide.add_component(current_component)
            
            title = line[3:].strip()
            current_component = Component(title)
        
        # H3 = Sub-Überschrift
        elif line.startswith('### '):
            if not current_component:
                current_component = Component()
            title = line[4:].strip()
            current_component.add_h3(title)
        
        # Aufzählung
        elif line.startswith('- '):
            if not current_component:
                current_component = Component()
            
            text = line[2:].strip()
            
            # Erkenne Statistiken (Zahl am Anfang)
            if re.match(r'^\d+[.,\d]*\s*(Mio|Mrd|%|€|\$|USD)', text):
                current_component.add_stat(text)
            else:
                current_component.add_bullet(text)
        
        # Blockquote
        elif line.startswith('> '):
            if not current_component:
                current_component = Component()
            text = line[2:].strip()
            current_component.add_quote(text)
        
        # Normaler Text
        elif stripped and not stripped.startswith('#'):
            if not current_component:
                current_component = Component()
            current_component.add_text(stripped)
    
    # Letzte Komponente und Folie hinzufügen
    if current_component and current_slide:
        current_slide.add_component(current_component)
    if current_slide:
        slides.append(current_slide)
    
    return slides

def format_text(text: str) -> str:
    """Formatiert Markdown-Text zu HTML"""
    # **bold** → <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # `code` → <code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def render_component(component: Component, slide_num: int, comp_num: int) -> str:
    """Rendert eine einzelne Komponente zu HTML"""
    html = f'<div class="component" id="slide-{slide_num}-comp-{comp_num}">\n'
    html += f'  <div class="component-label">Komponente {slide_num}.{comp_num}</div>\n'
    
    if component.title:
        html += f'  <h2>{component.title}</h2>\n'
    
    # Gruppiere Inhalte nach Typ
    stats = [c for c in component.content if c[0] == 'stat']
    bullets = [c for c in component.content if c[0] == 'bullet']
    others = [c for c in component.content if c[0] not in ['stat', 'bullet']]
    
    # Statistiken als Grid
    if stats:
        html += '  <div class="stat-grid">\n'
        for _, text in stats:
            # Versuche Zahl und Label zu trennen
            match = re.match(r'^([\d.,]+\s*(?:Mio|Mrd|%|€|\$|USD|\w+))\s+(.+)$', text)
            if match:
                number, label = match.groups()
                html += f'    <div class="stat-card">\n'
                html += f'      <span class="stat-number">{number}</span>\n'
                html += f'      <span class="stat-label">{label}</span>\n'
                html += f'    </div>\n'
            else:
                html += f'    <div class="stat-card">\n'
                html += f'      <span class="stat-label">{text}</span>\n'
                html += f'    </div>\n'
        html += '  </div>\n'
    
    # Aufzählungen
    if bullets:
        html += '  <ul class="bullet-list">\n'
        for _, text in bullets:
            formatted = format_text(text)
            html += f'    <li>{formatted}</li>\n'
        html += '  </ul>\n'
    
    # Andere Inhalte
    for content_type, text in others:
        if content_type == 'h3':
            html += f'  <h3>{text}</h3>\n'
        elif content_type == 'text':
            formatted = format_text(text)
            html += f'  <p>{formatted}</p>\n'
        elif content_type == 'quote':
            html += f'  <div class="quote">{text}</div>\n'
    
    html += '</div>\n'
    return html

def render_slides(slides: List[Slide]) -> str:
    """Rendert alle Slides zu HTML"""
    html = ''
    
    for slide_idx, slide in enumerate(slides):
        slide_num = slide_idx + 1
        html += f'<div class="slide-section">\n'
        html += f'  <div class="slide-title">Folie {slide_num}: {slide.title}</div>\n'
        
        for comp_idx, component in enumerate(slide.components):
            comp_num = comp_idx + 1
            html += render_component(component, slide_num, comp_num)
        
        html += '</div>\n\n'
    
    return html

def create_html_file(slides: List[Slide], output_path: Path):
    """Erstellt vollständige HTML-Datei"""
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robo4you Präsentations-Komponenten</title>
    <link rel="stylesheet" href="../github-presentation-template.css">
    <style>
        body {{
            background: #f6f8fa;
            padding: 40px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }}
        
        .component {{
            background: white;
            border: 2px solid #d0d7de;
            border-radius: 6px;
            padding: 32px;
            margin-bottom: 24px;
            position: relative;
        }}
        
        .component-label {{
            position: absolute;
            top: -12px;
            left: 16px;
            background: #238636;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .slide-section {{
            margin-bottom: 48px;
            padding-bottom: 24px;
            border-bottom: 2px solid #d0d7de;
        }}
        
        .slide-title {{
            font-size: 24px;
            font-weight: 700;
            color: #238636;
            margin-bottom: 24px;
            padding: 16px;
            background: #f6f8fa;
            border-radius: 6px;
            border-left: 4px solid #238636;
        }}
        
        h1 {{ font-size: 48px; font-weight: 700; margin: 0 0 16px 0; color: #24292f; }}
        h2 {{ font-size: 32px; font-weight: 600; margin: 0 0 16px 0; color: #24292f; }}
        h3 {{ font-size: 24px; font-weight: 600; margin: 0 0 12px 0; color: #24292f; }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }}
        
        .stat-card {{
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 20px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: 700;
            color: #238636;
            display: block;
            margin-bottom: 8px;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #57606a;
        }}
        
        .bullet-list {{
            list-style: none;
            padding: 0;
        }}
        
        .bullet-list li {{
            padding: 12px;
            margin: 8px 0;
            background: #f6f8fa;
            border-left: 4px solid #238636;
            border-radius: 4px;
        }}
        
        .bullet-list li strong {{
            color: #238636;
        }}
        
        .quote {{
            border-left: 4px solid #238636;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #57606a;
        }}
        
        code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1 style="color: #238636; margin-bottom: 32px;">📊 Robo4you Präsentations-Komponenten</h1>
    <p style="margin-bottom: 32px; color: #57606a;">
        Automatisch generiert aus Markdown. Jede Komponente kann einzeln gescreenshottet werden.
    </p>
    
{render_slides(slides)}
    
    <div style="margin-top: 48px; padding: 24px; background: #dff6e8; border: 1px solid #238636; border-radius: 6px;">
        <strong>💡 Screenshot-Tipp:</strong><br>
        Chrome: DevTools → Element untersuchen → Screenshot des Elements<br>
        Firefox: Rechtsklick → "Screenshot des Knotens erstellen"
    </div>
</body>
</html>
'''
    
    output_path.write_text(html, encoding='utf-8')

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python markdown-to-components.py <input.md> [output-dir]")
        print("\nBeispiel:")
        print("  python markdown-to-components.py pitch.md output/")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"❌ Datei nicht gefunden: {input_file}")
        sys.exit(1)
    
    # Output-Verzeichnis
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    else:
        output_dir = Path("output")
    
    output_dir.mkdir(exist_ok=True)
    
    # Markdown lesen
    print(f"📖 Lese Markdown: {input_file}")
    markdown_text = input_file.read_text(encoding='utf-8')
    
    # Parsen
    print("⚙️  Parse Markdown...")
    slides = parse_markdown(markdown_text)
    
    print(f"✅ {len(slides)} Folien gefunden")
    for idx, slide in enumerate(slides):
        print(f"   Folie {idx + 1}: {slide.title} ({len(slide.components)} Komponenten)")
    
    # HTML generieren
    output_file = output_dir / f"{input_file.stem}-components.html"
    print(f"💾 Generiere HTML: {output_file}")
    create_html_file(slides, output_file)
    
    print(f"\n✨ Fertig! Öffnen Sie {output_file} im Browser.")
    print(f"   Screenshots können dann einzeln erstellt werden.")

if __name__ == "__main__":
    main()

