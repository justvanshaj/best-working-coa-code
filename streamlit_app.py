import streamlit as st
import requests
from docx import Document
from io import BytesIO
import datetime

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

def download_template(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error("Failed to download template file.")
        return None

def replace_placeholders(doc, replacements):
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, str(value))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in replacements.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, str(value))

def generate_docx(cps_range, batch_no, moisture, ph_level, through_100, through_200, cps_2hr, cps_24hr, template_url):
    gum, protein, ash, air, fat = calculate_components(moisture)

    template_file = download_template(template_url)
    if template_file is None:
        return None

    doc = Document(template_file)

    today = datetime.date.today().strftime("%d-%m-%Y")

    replacements = {
        "CPS_RANGE_HERE": cps_range,
        "DATE_HERE": today,
        "BATCH_NO_HERE": batch_no,
        "MOISTURE_HERE": f"{moisture}%",
        "GUM_CONTENT_HERE": f"{gum}%",
        "PROTEIN_HERE": f"{protein}%",
        "ASH_CONTENT_HERE": f"{ash}%",
        "AIR_HERE": f"{air}%",
        "FAT_HERE": f"{fat}%",
        "PH_LEVEL_HERE": ph_level,
        "THROUGH_100_HERE": f"{through_100}%",
        "THROUGH_200_HERE": f"{through_200}%",
        "CPS_2HR_HERE": f"{cps_2hr} CPS (1% solution, W/W, Spindle No. 4, RPM-20, at 25°C, Cold - Brookfield Viscometer - RVDV)",
        "CPS_24HR_HERE": f"{cps_24hr} CPS (1% solution, W/W, Spindle No. 4, RPM-20, at 25°C, Cold - Brookfield Viscometer - RVDV)"
    }

    replace_placeholders(doc, replacements)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

# Streamlit app
st.title('Batch Quality Report Generator (Template Based)')

with st.form('input_form'):
    cps_range = st.text_input('CPS Range (e.g., 5500-6000 CPS)')
    batch_no = st.text_input('Batch Number')
    moisture = st.number_input('Moisture (%)', min_value=0.0, max_value=20.0, step=0.01)
    ph_level = st.text_input('pH Level')
    through_100 = st.number_input('Through 100 Mesh (%)', min_value=0.0, max_value=100.0, step=0.01)
    through_200 = st.number_input('Through 200 Mesh (%)', min_value=0.0, max_value=100.0, step=0.01)
    cps_2hr = st.number_input('Viscosity After 2 hours (CPS)', min_value=0, max_value=10000, step=1)
    cps_24hr = st.number_input('Viscosity After 24 hours (CPS)', min_value=0, max_value=10000, step=1)
    template_url = st.text_input('Template DOCX GitHub URL')

    submitted = st.form_submit_button('Generate Report')

if submitted:
    final_docx = generate_docx(cps_range, batch_no, moisture, ph_level, through_100, through_200, cps_2hr, cps_24hr, template_url)
    if final_docx:
        st.success('Report generated successfully!')
        st.download_button('Download Report', final_docx, file_name=f'{batch_no}_Quality_Report.docx')
