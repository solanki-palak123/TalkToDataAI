from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(summary, analysis):

    filename = "AI_Report.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>TalkToData AI Report</b>", styles["Heading1"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Dataset Summary</b>", styles["Heading2"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>AI Analysis</b>", styles["Heading2"]))
    story.append(Paragraph(str(analysis).replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    return filename