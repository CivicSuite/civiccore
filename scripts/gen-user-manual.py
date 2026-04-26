"""Generate USER-MANUAL.docx and USER-MANUAL.pdf from USER-MANUAL.md.

Pandoc-free; uses python-docx + reportlab. Minimal markdown subset:
H1/H2/H3 headings, paragraphs, bullet lists, fenced code blocks.
"""
from __future__ import annotations
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Image as RLImage

IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "USER-MANUAL.md"
OUT_DOCX = ROOT / "USER-MANUAL.docx"
OUT_PDF = ROOT / "USER-MANUAL.pdf"


def parse_blocks(md: str):
    """Yield (kind, text) blocks. kind in {'h1','h2','h3','p','code','bullet'}."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            yield "h1", line[2:].strip()
            i += 1
        elif line.startswith("## "):
            yield "h2", line[3:].strip()
            i += 1
        elif line.startswith("### "):
            yield "h3", line[4:].strip()
            i += 1
        elif line.startswith("```"):
            # fenced code block
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            yield "code", "\n".join(buf)
        elif IMAGE_RE.match(line):
            m = IMAGE_RE.match(line)
            yield "image", f"{m.group(1)}|{m.group(2)}"
            i += 1
        elif line.lstrip().startswith(("- ", "* ")):
            yield "bullet", line.lstrip()[2:].strip()
            i += 1
        elif line.strip() == "":
            i += 1
        else:
            yield "p", line.strip()
            i += 1


def gen_docx(md: str, dest: Path) -> None:
    doc = Document()
    for kind, text in parse_blocks(md):
        if kind == "h1":
            doc.add_heading(text, level=1)
        elif kind == "h2":
            doc.add_heading(text, level=2)
        elif kind == "h3":
            doc.add_heading(text, level=3)
        elif kind == "code":
            p = doc.add_paragraph()
            run = p.add_run(text)
            run.font.name = "Courier New"
            run.font.size = Pt(9)
        elif kind == "bullet":
            doc.add_paragraph(text, style="List Bullet")
        elif kind == "image":
            alt, path = text.split("|", 1)
            # Prefer .png variant for python-docx (no SVG support)
            png_path = ROOT / path.replace(".svg", ".png")
            if png_path.exists():
                doc.add_picture(str(png_path), width=Inches(6))
            else:
                doc.add_paragraph(f"[image: {alt} ({path})]")
        else:
            doc.add_paragraph(text)
    doc.save(str(dest))


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def gen_pdf(md: str, dest: Path) -> None:
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle(
        "Code", parent=styles["Code"], fontName="Courier", fontSize=8,
        leftIndent=12, leading=10,
    )
    story = []
    for kind, text in parse_blocks(md):
        if kind == "h1":
            story.append(Paragraph(_escape(text), styles["Heading1"]))
        elif kind == "h2":
            story.append(Paragraph(_escape(text), styles["Heading2"]))
        elif kind == "h3":
            story.append(Paragraph(_escape(text), styles["Heading3"]))
        elif kind == "code":
            story.append(Preformatted(text, code_style))
        elif kind == "bullet":
            story.append(Paragraph("• " + _escape(text), styles["BodyText"]))
        elif kind == "image":
            alt, path = text.split("|", 1)
            png_path = ROOT / path.replace(".svg", ".png")
            if png_path.exists():
                from PIL import Image as PILImage
                with PILImage.open(str(png_path)) as im:
                    iw, ih = im.size
                target_w = 6.0 * inch
                target_h = target_w * (ih / iw)
                story.append(RLImage(str(png_path), width=target_w, height=target_h))
            else:
                story.append(Paragraph(f"[image: {_escape(alt)} ({_escape(path)})]", styles["BodyText"]))
        else:
            story.append(Paragraph(_escape(text), styles["BodyText"]))
        story.append(Spacer(1, 4))
    doc = SimpleDocTemplate(str(dest), pagesize=LETTER, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    doc.build(story)


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    gen_docx(md, OUT_DOCX)
    gen_pdf(md, OUT_PDF)
    print(f"wrote {OUT_DOCX.relative_to(ROOT)} ({OUT_DOCX.stat().st_size} bytes)")
    print(f"wrote {OUT_PDF.relative_to(ROOT)} ({OUT_PDF.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
