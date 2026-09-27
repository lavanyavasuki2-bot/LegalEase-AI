import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors

def generate_project_report():
    pdf_filename = "LegalEase_AI_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor('#1E3A8A'), alignment=1, spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=colors.HexColor('#1D4ED8'), spaceBefore=12, spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14, spaceAfter=8
    )

    caption_style = ParagraphStyle(
        'Caption_Custom', parent=styles['Italic'],
        fontName='Helvetica-Oblique', fontSize=9, leading=12,
        alignment=1, textColor=colors.gray, spaceAfter=10
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("PROJECT REPORT: LegalEase AI", title_style))
    story.append(Paragraph("<b>Student Name:</b> Lavanya", body_style))
    story.append(Paragraph("<b>Project Title:</b> LegalEase AI - Legal Document Generator", body_style))
    story.append(Paragraph("<b>Technology Stack:</b> Python, FastAPI, Streamlit, Google Gemini API, ReportLab", body_style))
    story.append(Spacer(1, 10))

    # Project Overview
    story.append(Paragraph("1. Project Overview", h2_style))
    story.append(Paragraph(
        "LegalEase AI is an AI-powered legal document generation system designed to simplify the creation "
        "of legal agreements such as House Rental Agreements and NDAs. By combining a FastAPI backend "
        "powered by the Gemini API with a clean Streamlit interface, users can generate structured legal text "
        "and seamlessly export it into professional PDF files using ReportLab.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Screenshots Section
    story.append(Paragraph("2. System Implementation & Execution", h2_style))

    # Image 1
    if os.path.exists("img1.png"):
        story.append(Image("img1.png", width=420, height=210))
        story.append(Paragraph("Figure 1: Streamlit User Interface & Input Form", caption_style))
        story.append(Spacer(1, 8))

    # Image 2
    if os.path.exists("img2.png"):
        story.append(Image("img2.png", width=420, height=210))
        story.append(Paragraph("Figure 2: AI Document Generation & Download PDF Option", caption_style))
        story.append(Spacer(1, 8))

    # Image 3
    if os.path.exists("img3.png"):
        story.append(Image("img3.png", width=420, height=210))
        story.append(Paragraph("Figure 3: Downloaded House Rental Agreement PDF Output", caption_style))
        story.append(Spacer(1, 8))

    # Conclusion
    story.append(Paragraph("3. Conclusion", h2_style))
    story.append(Paragraph(
        "The application successfully automates legal document drafting and exports clean, downloadable "
        "PDFs with appropriate structure and formatting.",
        body_style
    ))

    doc.build(story)
    print("Project Report PDF successfully created as LegalEase_AI_Project_Report.pdf")

if __name__ == "__main__":
    generate_project_report()