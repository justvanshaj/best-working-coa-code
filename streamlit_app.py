import streamlit as st
from docx import Document
from datetime import datetime
import io
import re

# Function to parse the CPS range
def parse_cps_range(cps_range):
    try:
        first, last = cps_range.split("-")
        return first.strip(), last.strip()
    except Exception as e:
        return "0000", "0000"  # Fallback if format is wrong

# Function to get current month and year + best-before month/year
def get_month_year_strings():
    now = datetime.now()
    current_str = now.strftime("%B %Y")  # e.g., May 2025
    best_before_str = now.replace(year=now.year + 2).strftime("%B %Y")
    return current_str, best_before_str

# Function to replace placeholders in the document
def replace_placeholders(doc, replacements):
    # Paragraphs
    for p in doc.paragraphs:
        for key, val in replacements.items():
            if key in p.text:
                inline = p.runs
                for run in inline:
                    if key in run.text:
                        run.text = run.text.replace(key, val)

    # Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for key, val in replacements.items():
                        if key in p.text:
                            inline = p.runs
                            for run in inline:
                                if key in run.text:
                                    run.text = run.text.replace(key, val)

# Function to generate the report
def generate_report(data):
    # Load the template document
    doc = Document("template.docx")
    
    # Replace all placeholders
    replace_placeholders(doc, data)
    
    # Save the document to a BytesIO object
    doc_stream = io.BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0)
    
    return doc_stream

def main():
    st.title("Final Batch Report Generator (Exact Template)")

    # Input fields
    cps_range = st.text_input("CPS Range (e.g., 5000-5500)", "5000-5500")
    cps_first, cps_last = parse_cps_range(cps_range)
    cps2 = st.text_input("Viscosity After 24 Hours (CPS2)")
    batch_no = st.text_input("Batch Number")
    moisture = st.number_input("Moisture (%)", min_value=0.0, step=0.01)
    ph_level = st.text_input("pH Level")
    through_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, step=0.01)
    through_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, step=0.01)

    # Get current month and year, and best-before date
    current_month_year, best_before = get_month_year_strings()

    # Create replacements dictionary
    replacements = {
        "CPS_RANGE_FIRST_4_DIGIT": cps_first,
        "CPS_RANGE_LAST_4_DIGIT": cps_last,
        "CPS2": cps2,
        "BATCH_NO": batch_no,
        "MOISTURE": str(moisture),
        "PH_LEVEL": ph_level,
        "THROUGH_100": str(through_100),
        "THROUGH_200": str(through_200),
        "CURRENT_MONTH_YEAR": current_month_year,
        "BEST_BEFORE": best_before,
    }

    # Generate report
    if st.button("Generate Report"):
        doc_stream = generate_report(replacements)
        
        # Provide download link for the generated report
        st.download_button("Download Report", doc_stream, "Batch_Report.docx")

if __name__ == "__main__":
    main()
