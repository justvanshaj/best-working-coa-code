import streamlit as st
from docx import Document
import random
import os
import mammoth
from docx.shared import RGBColor

# --- Replace placeholders preserving style (color, font, etc.) ---
def advanced_replace_text_preserving_style(doc, replacements):
    def replace_in_paragraph(paragraph):
        runs = paragraph.runs
        full_text = ''.join(run.text for run in runs)
        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in full_text:
                new_runs = []
                accumulated = ""
                for run in runs:
                    accumulated += run.text
                    new_runs.append(run)
                    if placeholder in accumulated:
                        style_run = next((r for r in new_runs if placeholder in r.text), new_runs[0])
                        font = style_run.font
                        accumulated = accumulated.replace(placeholder, value)
                        for r in new_runs:
                            r.text = ''
                        if new_runs:
                            new_run = new_runs[0]
                            new_run.text = accumulated
                            new_run.font.name = font.name
                            new_run.font.size = font.size
                            new_run.font.bold = font.bold
                            new_run.font.italic = font.italic
                            new_run.font.underline = font.underline
                            new_run.font.color.rgb = font.color.rgb
                        break

    for para in doc.paragraphs:
        replace_in_paragraph(para)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_paragraph(para)

# --- Generate DOCX ---
def generate_docx(data, template_path="template.docx", output_path="generated_coa.docx"):
    doc = Document(template_path)
    advanced_replace_text_preserving_style(doc, data)
    doc.save(output_path)
    return output_path

# --- Convert DOCX to HTML ---
def docx_to_html(docx_path):
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

# --- Moisture-based calculation ---
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
st.title("🧪 COA Document Generator (Code-Based Template)")

with st.form("coa_form"):
    code = st.selectbox(
        "Select Product Code Range",
        [f"{i}-{i+500}" for i in range(500, 10001, 500)]
    )
    st.info(f"📄 Using template: COA {code}.docx")

    date = st.text_input("Date (e.g., JULY 2025)")
    batch_no = st.text_input("Batch Number")
    best_before = st.text_input("Best Before (e.g., JULY 2027)")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=100.0, step=0.01, value=10.0)
    ph = st.text_input("pH Level (e.g., 6.7)")
    mesh_200 = st.text_input("200 Mesh (%)")
    viscosity_2h = st.text_input("Viscosity After 2 Hours (CPS)")
    viscosity_24h = st.text_input("Viscosity After 24 Hours (CPS)")
    submitted = st.form_submit_button("Generate COA")

if submitted:
    template_path = f"COA {code}.docx"
    output_path = "generated_coa.docx"

    if not os.path.exists(template_path):
        st.error(f"Template file 'COA {code}.docx' not found.")
    else:
        gum, protein, ash, air, fat = calculate_components(moisture)

        data = {
            "DATE": date,
            "BATCH_NO": batch_no,
            "BEST_BEFORE": best_before,
            "MOISTURE": f"{moisture}%",
            "PH": ph,
            "MESH_200": f"{mesh_200}%",
            "VISCOSITY_2H": viscosity_2h,
            "VISCOSITY_24H": viscosity_24h,
            "GUM_CONTENT": f"{gum}%",
            "PROTEIN": f"{protein}%",
            "ASH_CONTENT": f"{ash}%",
            "AIR": f"{air}%",
            "FAT": f"{fat}%"
        }

        generate_docx(data, template_path=template_path, output_path=output_path)

        try:
            html = docx_to_html(output_path)
            st.subheader("📄 Preview")
            st.components.v1.html(f"<div style='padding:15px'>{html}</div>", height=700, scrolling=True)
        except:
            st.warning("Preview failed. You can still download the file below.")

        # Final filename
        safe_batch = batch_no.replace("/", "_").replace("\\", "_").replace(" ", "_")
        final_filename = f"COA-{safe_batch}-{code}.docx"

        with open(output_path, "rb") as file:
            st.download_button("📥 Download COA (DOCX)", file, file_name=final_filename)
