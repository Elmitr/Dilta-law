import os
from fpdf import FPDF
from pypdf import PdfReader
import pdfplumber
from typing import Optional

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber (best for Arabic/legal docs)."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"Error extracting text with pdfplumber: {e}")
        # Fallback to pypdf
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
    return text.strip()

def create_judgment_pdf(case_number: str, court: str, judgment_date: str, 
                        ruling: str, summary: str = "", tags: str = "") -> str:
    """Create a professional PDF report for a judgment."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    
    pdf.cell(0, 10, "تقرير حكم قضائي - Dilta-law", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"رقم القضية: {case_number}", ln=True)
    pdf.cell(0, 8, f"المحكمة: {court}", ln=True)
    pdf.cell(0, 8, f"تاريخ الحكم: {judgment_date}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"ملخص الحكم:\n{summary}")
    pdf.ln(5)
    
    pdf.multi_cell(0, 8, f"نص الحكم:\n{ruling[:2000]}...")
    
    if tags:
        pdf.ln(5)
        pdf.cell(0, 8, f"التصنيفات: {tags}", ln=True)
    
    output_path = f"/tmp/judgment_{case_number.replace('/', '_')}.pdf"
    pdf.output(output_path)
    return output_path
