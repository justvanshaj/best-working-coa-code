import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
import datetime

TEMPLATE_FILE = "Sample Sample.docx"  # Template file with Jinja2-style placeholders

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

def generate_docx(cps1, cps2, batch_no, moisture, ph_level, through_100, through_200):
    gum, protein, ash, air, fat = calculate_components(moisture)

    try:
        doc = DocxTemplate(TEMPLATE_FILE)
    except Exception as e:
        st.error(f"Error opening template file: {e}")
        return None

    today = datetime.date.today()
    current_month_year = today.strftime("%m-%Y")
    best_before_year = today.year + 2
    best_before = f"{today.strftime('%m')}-{best_before_year}"

    context = {
        "CPS1": cps1,
        "CPS2": cps2,
        "BATCH_NO": batch_no,
        "MOISTURE": f"{moisture}%",
        "GUM": f"{gum}%",
        "PROTEIN": f"{protein}%",
        "ASH": f"{ash}%",
        "AIR": f"{air}%",
        "FAT": f"{fat}%",
        "PH_LEVEL": str(ph_level),
        "THROUGH_100": f"{through_100}%",
        "THROUGH_200": f"{through_200}%",
        "MONTH_YYYY": current_month_year,
        "MONTH_YYYY_2": best_before,
    }

    doc.render(context)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

# Streamlit UI
st.title('Final Batch Report Generator (DocxTPL Template)')

with st.form("form"):
    cps1 = st.text_input("Viscosity After 2 Hours (CPS1)")
    cps2 = st.text_input("Viscosity After 24 Hours (CPS2)")
    batch_no = st.text_input("Batch Number")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=20.0, step=0.01)
    ph_level = st.text_input("pH Level")
    through_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)
    through_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    result = generate_docx(cps1, cps2, batch_no, moisture, ph_level, through_100, through_200)
    if result:
        st.success("Document ready!")
        st.download_button("Download DOCX", result, file_name=f"{batch_no}_Report.docx")
