import streamlit as st
from docx import Document
from datetime import datetime
import re
import os

st.set_page_config(page_title="Final Batch Report Generator (Exact Template)", layout="centered")
st.title("Final Batch Report Generator (Exact Template)")

# Input fields
cps_range = st.text_input("CPS Range (e.g., 5000-5500)", value="5000-5500")
cps2 = st.text_input("Viscosity After 24 Hours (CPS2)")
batch_number = st.text_input("Batch Number")
moisture = st.number_input("Moisture (%)", min_value=0.0, format="%.2f")
ph = st.text_input("pH Level")
mesh_100 = st.number_input("Through 100 Mesh (%)", min_value=0.0, format="%.2f")
mesh_200 = st.number_input("Through 200 Mesh (%)", min_value=0.0, format="%.2f")

# Date info
now = datetime.now()
current_display = now.strftime("%B %Y")  # e.g., May 2025
future_display = datetime(now.year + 2, now.month, 1).strftime("%B %Y")  # e.g., May 2027

st.markdown(f"**Current Month-Year:** {current_display}")
st.markdown(f"**Same Month with Year +2:** {future_display}")

# Button
if st.button("Generate Report"):
    try:
        # Handle CPS range
        cps_match = re.match(r"(\d{4})-(\d{4})", cps_range)
        if not cps_match:
            st.error("Invalid CPS range format. Please enter like 5000-5500.")
            st.stop()
        cps_first, cps_last = cps_match.groups()

        # Load template
        template_path = "Sample Piece Final.docx"
        if not os.path.exists(template_path):
            st.error("Template file not found.")
            st.stop()

        doc = Document(template_path)

        # Replacement mapping
        replacements = {
            "CPS1_here": cps_range,
            "CPS_RANGE_FIRST_4_DIGIT": cps_first,
            "CPS_RANGE_LAST_4_DIGIT": cps_last,
            "CPS2_here": cps2,
            "BATCH_NUMBER_HERE": batch_number,
            "MOISTURE_HERE": f"{moisture:.2f}",
            "PH_HERE": ph,
            "THROUGH_100_MESH_HERE": f"{mesh_100:.2f}",
            "THROUGH_200_MESH_HERE": f"{mesh_200:.2f}",
            "CURRENT_MONTH_YEAR": current_display,
            "FUTURE_MONTH_YEAR": future_display,
        }

        # Replace text in paragraphs and tables
        def replace_text_in_paragraphs(paragraphs):
            for p in paragraphs:
                for key, val in replacements.items():
                    if key in p.text:
                        inline = p.runs
                        for i in range(len(inline)):
                            if key in inline[i].text:
                                inline[i].text = inline[i].text.replace(key, val)

        def replace_text_in_tables(tables):
            for table in tables:
                for row in table.rows:
                    for cell in row.cells:
                        replace_text_in_paragraphs(cell.paragraphs)

        replace_text_in_paragraphs(doc.paragraphs)
        replace_text_in_tables(doc.tables)

        # Save to BytesIO
        from io import BytesIO
        output = BytesIO()
        doc.save(output)
        output.seek(0)

        filename = f"{batch_number.replace(' ', '_')}_Report.docx"
        st.success("Report generated successfully!")
        st.download_button("Download Final Report", output, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    except Exception as e:
        st.error(f"Error: {str(e)}")
