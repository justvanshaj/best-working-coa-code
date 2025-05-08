import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO

TEMPLATE_FILE = "Finish Work.docx"

def generate_docx(context):
    doc = DocxTemplate(TEMPLATE_FILE)
    doc.render(context)
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

st.title("📄 Final Batch Report Generator")

with st.form("batch_form"):
    cps_gt = st.text_input("CPSGT (e.g. 5000)")
    cps_lt = st.text_input("CPSLT (e.g. 5500)")
    cps2 = st.text_input("CPS2 Result (After 2 Hours)")
    cps24 = st.text_input("CPS24 Result (After 24 Hours)")
    batch_no = st.text_input("Batch Number")
    month_yyyy = st.text_input("Date (e.g. May 2025)")
    month_yyyy_plus2 = st.text_input("Best Before (e.g. May 2027)")
    moisture = st.number_input("Moisture (%)", min_value=0.0, max_value=20.0, step=0.01)
    ph = st.text_input("pH Level")
    mesh_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)
    mesh_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, max_value=100.0, step=0.01)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    context = {
        "CPSGT_HERE": cps_gt,
        "CPSLT_HERE": cps_lt,
        "CPS2_HERE": cps2,
        "CPS24_HERE": cps24,
        "BATCH_NUMBER_HERE": batch_no,
        "MONTH_YYYY_HERE": month_yyyy,
        "MONTH_YYYY+2_HERE": month_yyyy_plus2,
        "MOIST_HERE": f"{moisture}%",
        "PH_HERE": ph,
        "100#_HERE": f"{mesh_100}%",
        "200#_HERE": f"{mesh_200}%"
    }

    doc_file = generate_docx(context)
    st.success("✅ Report generated successfully!")
    st.download_button("📥 Download DOCX", doc_file, file_name=f"{batch_no}_Report.docx")
