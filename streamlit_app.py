import streamlit as st
from docx import Document
import random
import os

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

def generate_docx(data, template_path="gpt sample for coa.docx", output_path="generated_coa.docx"):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, value in data.items():
            if f"{{{{{key}}}}}" in p.text:
                p.text = p.text.replace(f"{{{{{key}}}}}", str(value))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    if f"{{{{{key}}}}}" in cell.text:
                        cell.text = cell.text.replace(f"{{{{{key}}}}}", str(value))
    doc.save(output_path)
    return output_path

# Streamlit App
st.title("COA Document Generator")

st.subheader("Enter COA Details:")

product = st.text_input("Product Name")
date = st.text_input("Date")
batch_no = st.text_input("Batch Number")
best_before = st.text_input("Best Before")
moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=100.0, step=0.01)
ph = st.text_input("pH Level (5.5 - 7.0)")
mesh_200 = st.text_input("200 Mesh (%)")
viscosity_2h = st.text_input("Viscosity After 2 Hours (CPS)")
viscosity_24h = st.text_input("Viscosity After 24 Hours (CPS)")

if st.button("Generate COA Document"):
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
    template_path = "template_coa.docx"  # Ensure this is in the same folder
    generate_docx(data, template_path, output_path)

    with open(output_path, "rb") as f:
        st.download_button("📄 Download COA", f, file_name=output_path)
