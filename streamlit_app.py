import streamlit as st
from docx import Document
from io import BytesIO
import datetime

TEMPLATE_FILE = "Sample Piece Final.docx"

def calculate_components(moisture):
    gum = 81.61
    protein = 3.15
    ash = 0.64
    air = 3.0
    fat = 0.70
    total_fixed = gum + protein + ash + air + fat
    adjustment = 100 - (moisture + total_fixed)
    gum += adjustment
    return round(gum, 2), protein, ash, air, fat

def replace_text_in_runs(runs, replacements):
    for run in runs:
        for key, value in replacements.items():
            if key in run.text:
                run.text = run.text.replace(key, str(value))

def replace_placeholders(doc, replacements):
    for paragraph in doc.paragraphs:
        replace_text_in_runs(paragraph.runs, replacements)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_text_in_runs(paragraph.runs, replacements)

def generate_docx(cps1, cps2, cps_range, batch_no, moisture, ph_level, through_100, through_200):
    gum, protein, ash, air, fat = calculate_components(moisture)

    try:
        doc = Document(TEMPLATE_FILE)
    except Exception as e:
        st.error(f"Error opening template file: {e}")
        return None

    # Parse CPS Range
    try:
        cps_first, cps_last = cps_range.split('-')
        cps_first = cps_first
