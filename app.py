import streamlit as st
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import re

st.set_page_config(page_title="LegalEase AI", page_icon="⚖️", layout="centered")

st.title("LegalEase AI - Legal Document Generator")

doc_type = st.selectbox(
    "Select Document Type",
    ["House Rental Agreement", "Non-Disclosure Agreement (NDA)", "Employment Contract", "Commercial Lease Agreement"]
)

parties = st.text_input("Parties Involved (e.g., Mr. Kumar & Mr. Suresh)", "Kumar (Landlord), Suresh (Tenant)")
effective_date = st.text_input("Effective Date (e.g., 1st Oct 2026)", "October 1 2026")
key_terms = st.text_area("Key Terms & Conditions", "Rent is Rs. 10,000 per month; Security Deposit is Rs. 50,000; Notice period is 2 months; Minor repairs up to Rs. 1,000 borne by Tenant.")

def create_pdf(doc_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'LegalBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=8
    )

    story = []
    # Clean text
    cleaned_text = re.sub(r'<br\s*/?>', '\n', doc_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'<para>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'</para>', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\\(.?)\\*', r'<b>\1</b>', cleaned_text)

    paragraphs = cleaned_text.split('\n')
    for para in paragraphs:
        para_trimmed = para.strip()
        if not para_trimmed:
            story.append(Spacer(1, 6))
            continue
        story.append(Paragraph(para_trimmed, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("Generate Document"):
    with st.spinner("Generating legal document..."):
        payload = {
            "doc_type": doc_type,
            "parties": parties,
            "effective_date": effective_date,
            "key_terms": key_terms
        }
        try:
            res = requests.post("http://127.0.0.1:8000/generate", json=payload)
            if res.status_code == 200:
                doc_text = res.json().get("document_text", "")
                st.success("Document Generated Successfully!")
                st.text_area("Preview", doc_text, height=300)

                # PDF Download
                pdf_data = create_pdf(doc_text)
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_data,
                    file_name=f"{doc_type.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"Error from Backend: {res.text}")
        except Exception as e:
            st.error(f"Backend Connection Error: {str(e)}")