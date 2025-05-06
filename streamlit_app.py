import streamlit as st
from docx import Document
from io import BytesIO
import datetime

TEMPLATE_FILE = "Sample Piece Final.docx"  # Ensure this is in the same folder as this script

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

def generate_docx(cps1, cps2, batch_no, moisture, ph_level, through_100, through_200, cps_range_input):
    gum, protein, ash, air, fat = calculate_components(moisture)

    try:
        first_part, last_part = cps_range_input.strip().split('-')
        cps_range_full = cps_range_input.strip()
    except Exception:
        first_part, last_part, cps_range_full = "N/A", "N/A", "Invalid Range"

    try:
        doc = Document(TEMPLATE_FILE)
    except Exception as e:
        st.error(f"Error opening template file: {e}")
        return None

    today = datetime.date.today()
    current_month_year = today.strftime("%m-%Y")
    best_before = f"{today.strftime('%m')}-{today.year + 2}"

    replacements = {
        "CPS_2hr_here": cps1,
        "CPS_24hr_here": cps2,
        "BATCH_NO_HERE": batch_no,
        "MOISTURE_HERE": f"{moisture}%",
        "GUM_CONTENT_HERE": f"{gum}%",
        "PROTEIN_HERE": f"{protein}%",
        "ASH_CONTENT_HERE": f"{ash}%",
        "AIR_HERE": f"{air}%",
        "FAT_HERE": f"{fat}%",
        "PH_LEVEL_HERE": str(ph_level),
        "THROUGH_100_HERE": f"{through_100}%",
        "THROUGH_200_HERE": f"{through_200}%",
        "CURRENT_MONTH_YEAR_here": current_month_year,
        "CURRENT_Month_Year+2_here": best_before,
        "CPS_RANGE_here": cps_range_full,
        "CPS_RANGE_FIRST_4_DIGIT": first_part,
        "CPS_RANGE_LAST_4_DIGIT": last_part,
    }

    replace_placeholders(doc, replacements)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

# --- Streamlit UI ---
st.title("📄 Final Batch Report Generator")

with st.form("input_form"):
    cps1 = st.text_input("Viscosity After 2 Hours (CPS1)", max_chars=10)
    cps2 = st.text_input("Viscosity After 24 Hours (CPS2)", max_chars=10)
    batch_no = st.text_input("Batch Number")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=20.0, step=0.01)
    ph_level = st.text_input("pH Level", max_chars=10)
    through_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)
    through_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)
    cps_range_input = st.text_input("CPS Range (e.g. 5000-5500)")

    submitted = st.form_submit_button("Generate DOCX")

if submitted:
    if not (cps1 and cps2 and batch_no and ph_level and cps_range_input):
        st.error("Please fill all required fields.")
    else:
        result = generate_docx(cps1, cps2, batch_no, moisture, ph_level, through_100, through_200, cps_range_input)
        if result:
            st.success("✅ Document generated successfully!")
            st.download_button("📥 Download DOCX", result, file_name=f"{batch_no}_Report.docx")
