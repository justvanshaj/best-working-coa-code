import streamlit as st
from docx import Document
import random
import os
from io import BytesIO
import mammoth

# --- Format-preserving placeholder replacement (even across runs) ---
def replace_text_format_preserved(doc, replacements):
    def replace_in_runs(runs, replacements):
        full_text = ''.join(run.text for run in runs)
        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in full_text:
                full_text = full_text.replace(placeholder, str(value))
                for run in runs:
                    run.text = ''
                if runs:
                    runs[0].text = full_text
                break

    for para in doc.paragraphs:
        replace_in_runs(para.runs, replacements)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_runs(para.runs, replacements)

# --- COA DOCX Generator ---
def generate_docx(data, template_path="COA SAMPLE GPT.docx", output_path="generated_coa.docx"):
    doc = Document(template_path)
    replace_text_format_preserved(doc, data)
    doc.save(output_path)
    return output_path

# --- Optional preview using mammoth (HTML conversion of .docx) ---
def docx_to_html(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

# --- Calculation logic ---
def calculate_components(moisture):
    remaining = 100 - moisture
    gum = round(random.uniform(81, min(85, remaining - 1.5)), 2)
    remaining -= gum
    protein = round(min(5, remaining * 0.2), 2)
    remaining -= protein
    ash = round(min(1, remaining * 0.2), 2)
    remaining -= ash
    air = round(min(6, remaining * 0.5), 2)
    remaining -= air
    fat = round(remaining, 2)
    return gum, protein, ash, air, fat

# --- UI Starts ---
st.set_page_config(page_title="COA Generator", layout="wide")
st.title("🧪 COA Document Generator with Formatting & Live Preview")

with st.form("coa_form"):
    product = st.text_input("Product Name", "GUAR GUM POWDER 5500-6000 (CPS)")
    date = st.text_input("Date (e.g., July 2025)")
    batch_no = st.text_input("Batch Number")
    best_before = st.text_input("Best Before (e.g., July 2027)")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=100.0, step=0.01, value=10.0)
    ph = st.text_input("pH Level (e.g., 6.7)")
    mesh_200 = st.text_input("200 Mesh (%)")
    viscosity_2h = st.text_input("Viscosity After 2 Hours (CPS)")
    viscosity_24h = st.text_input("Viscosity After 24 Hours (CPS)")
    submitted = st.form_submit_button("Generate COA")

if submitted:
    gum, protein, ash, air, fat = calculate_components(moisture)

    data = {
        "PRODUCT": product,
        "DATE": date,
        "BATCH_NO": batch_no,
        "BEST_BEFORE": best_before,
        "MOISTURE": f"{moisture}%",
        "PH": ph,
        "MESH_200": mesh_200,
        "VISCOSITY_2H": viscosity_2h,
        "VISCOSITY_24H": viscosity_24h,
        "GUM_CONTENT": f"{gum}%",
        "PROTEIN": f"{protein}%",
        "ASH_CONTENT": f"{ash}%",
        "AIR": f"{air}%",
        "FAT": f"{fat}%"
    }

    template_path = "COA SAMPLE GPT.docx"
    output_path = "generated_coa.docx"

    generate_docx(data, template_path=template_path, output_path=output_path)

    # Preview (HTML render)
    try:
        html = docx_to_html(output_path)
        st.subheader("📄 COA Preview")
        st.components.v1.html(f"<div style='padding:15px;'>{html}</div>", height=700, scrolling=True)
    except Exception as e:
        st.error("Preview failed. You can still download the file.")

    # Download
    with open(output_path, "rb") as file:
        st.download_button("📥 Download COA (DOCX)", file, file_name="COA_Generated.docx")
