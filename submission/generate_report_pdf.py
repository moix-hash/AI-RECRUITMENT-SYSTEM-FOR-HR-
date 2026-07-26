from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
source = ROOT / "project_report.md"
output = ROOT / "project_report.pdf"
styles = getSampleStyleSheet()
font_dir = Path("C:/Windows/Fonts")
regular_font = "Helvetica"
bold_font = "Helvetica-Bold"
if (font_dir / "arial.ttf").exists() and (font_dir / "arialbd.ttf").exists():
    pdfmetrics.registerFont(TTFont("TalentOS", str(font_dir / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("TalentOS-Bold", str(font_dir / "arialbd.ttf")))
    regular_font = "TalentOS"
    bold_font = "TalentOS-Bold"

title_style = ParagraphStyle("ReportTitle", parent=styles["Title"], fontName=bold_font, alignment=TA_CENTER, spaceAfter=18)
heading_style = ParagraphStyle("ReportHeading", parent=styles["Heading2"], fontName=bold_font, textColor=colors.HexColor("#1F2937"), spaceBefore=12, spaceAfter=6)
body_style = ParagraphStyle("ReportBody", parent=styles["BodyText"], fontName=regular_font, leading=15, spaceAfter=7)

story = []
bullets: list[str] = []


def flush_bullets() -> None:
    if bullets:
        story.append(ListFlowable([ListItem(Paragraph(item, body_style)) for item in bullets], bulletType="bullet", leftIndent=18))
        bullets.clear()


for raw_line in source.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line:
        flush_bullets()
        story.append(Spacer(1, 4))
    elif line.startswith("# "):
        flush_bullets()
        story.append(Paragraph(line[2:], title_style))
    elif line.startswith("## "):
        flush_bullets()
        story.append(Paragraph(line[3:], heading_style))
    elif line.startswith("- "):
        bullets.append(line[2:])
    else:
        flush_bullets()
        story.append(Paragraph(line.replace("&", "&amp;"), body_style))
flush_bullets()

document = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
document.build(story)
print(output)
