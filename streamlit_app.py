import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
import datetime

TEMPLATE_FILE = "Finish Work.docx"  # Must exist in repo

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

def get_date_fields():
    today = datetime.date.today()
    month_year = today.strftime("%B %Y")         # e.g. May 2025
    month_year_plus2 = today.replace(year=today.year + 2).strftime("%B %Y")
    return month_year, month_year_plus2

def generate_docx(context):
    doc = DocxTemplate(TEMPLATE_FILE)
    doc.render(context)
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

st.title("🧾 Final Batch Report Generator")

with st.form("batch_form"):
    cps_gt = st.text_input("CPS Range First (e.g. 5000)", "5000")
    cps_lt = st.text_input("CPS Range Last (e.g. 5500)", "5500")
    cps2 = st.text_input("Viscosity After 2 Hours")
    cps24 = st.text_input("Viscosity After 24 Hours")
    batch_no = st.text_input("Batch Number")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=20.0, step=0.01)
    ph = st.text_input("pH Level")
    through_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, max_value=100.0)
    through_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, max_value=100.0)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    gum, protein, ash, air, fat = calculate_components(moisture)
    month_yyyy, month_yyyy_plus2 = get_date_fields()

    context = {
        "CPSGT_HERE": cps_gt,
        "CPSLT_HERE": cps_lt,
        "CPS2_HERE": cps2,
        "CPS24_HERE": cps24,
        "BATCH_NUMBER_HERE": batch_no,
        "MOIST_HERE": f"{moisture}%",
        "GUM_CONTENT_HERE": f"{gum}%",
        "PROTEIN_HERE": f"{protein}%",
        "ASH_HERE": f"{ash}%",
        "AIR_HERE": f"{air}%",
        "FAT_HERE": f"{fat}%",
        "PH_HERE": ph,
        "100#_HERE": f"{through_100}%",
        "200#_HERE": f"{through_200}%",
        "MONTH_YYYY_HERE": month_yyyy,
        "MONTH_YYYY+2_HERE": month_yyyy_plus2,
    }

    doc_file = generate_docx(context)
    st.success("✅ Report generated successfully!")
    st.download_button("📥 Download DOCX", doc_file, file_name=f"{batch_no}_Report.docx")
