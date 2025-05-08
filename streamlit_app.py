import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
import datetime
import os

TEMPLATE_FILE = "Finish_Work_FINAL_SAFE.docx"

# Guar gum component calculator
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

# Load template from file or uploaded fallback
def load_template(uploaded_template):
    if uploaded_template:
        return DocxTemplate(uploaded_template)
    elif os.path.exists(TEMPLATE_FILE):
        return DocxTemplate(TEMPLATE_FILE)
    else:
        return None

st.title("🧾 Guar Gum Batch Report Generator")

# Upload backup option
uploaded_template = st.file_uploader("⬆️ Upload Custom Template (optional)", type="docx")

# Input form
with st.form("batch_form"):
    cpsgt = st.text_input("CPSGT (2 Hour Viscosity Threshold)", "5000")
    cpslt = st.text_input("CPSLT (24 Hour Viscosity Threshold)", "5500")
    cps2 = st.text_input("Actual CPS After 2 Hours")
    cps24 = st.text_input("Actual CPS After 24 Hours")
    batch_no = st.text_input("Batch Number")
    month_year = st.text_input("Month Year (e.g. May 2025)")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=20.0, step=0.01)
    ph = st.text_input("pH Level")
    through_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, max_value=100.0)
    through_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, max_value=100.0)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    gum, protein, ash, air, fat = calculate_components(moisture)
    now = datetime.datetime.now()
    try:
        best_before = month_year.replace(str(now.year), str(now.year + 2))
    except:
        best_before = "N/A"

    context = {
        "CPSGTHERE": cpsgt,
        "CPSLTHERE": cpslt,
        "CPS2HERE": cps2,
        "CPS24HERE": cps24,
        "BATCHNUMBERHERE": batch_no,
        "MONTHYYYYHERE": month_year,
        "MONTHYYYYplus2HERE": best_before,
        "MOISTHERE": f"{moisture}%",
        "GUMCONTENTHERE": f"{gum}%",
        "PROTEINHERE": f"{protein}%",
        "ASHHERE": f"{ash}%",
        "AIRHERE": f"{air}%",
        "FATHERE": f"{fat}%",
        "PHHERE": ph,
        "100MESHHERE": f"{through_100}%",
        "200MESHHERE": f"{through_200}%",
    }

    doc = load_template(uploaded_template)
    if doc:
        try:
            doc.render(context)
            output = BytesIO()
            doc.save(output)
            output.seek(0)
            st.success("✅ Report generated successfully!")
            st.download_button("📥 Download DOCX", output, file_name=f"{batch_no}_report.docx")
        except Exception as e:
            st.error(f"⚠️ Error rendering document: {e}")
    else:
        st.error("❌ Template not found. Please upload a valid .docx file.")
