import streamlit as st
from docx import Document
from docx.shared import Inches
from docx2pdf import convert
from io import BytesIO
import random
import os
from PIL import Image
import mammoth  # optional for cleaner previews

# --- Format-preserving text replacement ---
def replace_text_format_preserved(doc, replacements):
    for p in doc.paragraphs:
        for run in p.runs:
            for key, value in replacements.items():
                if f"{{{{{key}}}}}" in run.text:
                    run.text = run.text.replace(f"{{{{{key}}}}}", str(value))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        for key, value in replacements.items():
                            if f"{{{{{key}}}}}" in run.text:
                                run.text = run.text.replace(f"{{{{{key}}}}}", str(value))

# --- Document Generation ---
def generate_docx(data, template_path="COA SAMPLE GPT.docx", output_path="generated_coa.docx"):
    doc = Document(template_path)
    replace_text_format_preserved(doc, data)
    doc.save(output_path)
    return output_path

# --- Component calculation logic ---
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

# --- DOCX to preview image (using Word/LibreOffice not possible here; use simplified HTML preview) ---
def docx_to_html(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

# --- Streamlit UI ---
st.title("🧪 COA Document Generator with Preview")

with st.form("coa_form"):
    product = st.text_input("Product Name")
    date = st.text_input("Date (e.g., July 2025)")
    batch_no = st.text_input("Batch Number")
    best_before = st.text_input("Best Before (e.g., July 2027)")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=100.0, step=0.01)
    ph = st.text_input("pH Level (5.5 - 7.0)")
    mesh_200 = st.text_input("200 Mesh (%)")
    viscosity_2h = st.text_input("Viscosity After 2 Hours (CPS)")
    viscosity_24h = st.text_input("Viscosity After 24 Hours (CPS)")
    submitted = st.form_submit_button("Generate and Preview")

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

    output_path = "generated_coa.docx"
    generate_docx(data, template_path="COA SAMPLE GPT.docx", output_path=output_path)

    # Show preview using HTML view
    st.subheader("📄 Preview:")
    try:
        html_content = docx_to_html(output_path)
        st.components.v1.html(f"<div style='padding:20px;'>{html_content}</div>", height=700, scrolling=True)
    except Exception as e:
        st.warning("Preview failed. Download is still available.")

    with open(output_path, "rb") as file:
        st.download_button("📥 Download COA (DOCX)", file, file_name="COA_Generated.docx")
