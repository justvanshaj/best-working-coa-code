import streamlit as st
from docx import Document
import datetime
import os
import pandas as pd
from io import BytesIO

# --- Replace placeholders robustly even in tables ---
def replace_placeholders(doc, replacements):
    import re
    pattern = re.compile(r"{{(.*?)}}")

    def replace_in_paragraph(paragraph):
        full_text = "".join(run.text for run in paragraph.runs)
        for key, val in replacements.items():
            full_text = full_text.replace(f"{{{{{key}}}}}", str(val))
        paragraph.clear()
        paragraph.add_run(full_text)

    for p in doc.paragraphs:
        if pattern.search(p.text):
            replace_in_paragraph(p)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if pattern.search(p.text):
                        replace_in_paragraph(p)

# --- Generate DOCX ---
def generate_docx(data, template_path="SALARY SLIP FORMAT.docx"):
    doc = Document(template_path)
    replace_placeholders(doc, data)
    file_name = f"salaryslip_{data['Name'].replace(' ', '_')}_{data['Month'].replace(' ', '_')}.docx"
    doc.save(file_name)
    return file_name

# --- Streamlit App ---
st.set_page_config(page_title="Salary Slip Generator", layout="wide")
st.title("🧾 Salary Slip Generator")

if "generated_file" not in st.session_state:
    st.session_state.generated_file = None

# --- Bulk Generator ---
with st.expander("📤 Bulk Salary Slip Generator from Excel"):
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], key="bulk_excel")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ Uploaded {len(df)} row(s)")

        for index, row in df.iterrows():
            name = row["Name"]
            total = row["Salary"] + row["Bonus"] + row["Other"]
            net_advance = row["Advance_Till_Date"] - row["Advance_Deduct"]
            payable = total - (row["ESI"] + row["Advance_Deduct"] + row["MISC"])
            payment_date = datetime.datetime.now().strftime("%d %B %Y")

            data = {
                "Name": name,
                "Designation": row["Designation"],
                "Department": row["Department"],
                "Total_Days": row["Total_Days"],
                "Working_Days": row["Working_Days"],
                "Weekly_Off": row["Weekly_Off"],
                "Festival_Off": row["Festival_Off"],
                "Paid_Days": row["Paid_Days"],
                "Base": row["Base"],
                "Month": row["Month"],
                "Salary": row["Salary"],
                "Bonus": row["Bonus"],
                "Other": row["Other"],
                "Total": total,
                "ESI": row["ESI"],
                "Advance_Till_Date": row["Advance_Till_Date"],
                "Advance_Deduct": row["Advance_Deduct"],
                "Net_Advance": net_advance,
                "MISC": row["MISC"],
                "Payable": payable,
                "Payment_Date": payment_date,
            }

            docx_path = generate_docx(data)
            st.success(f"✅ Generated: {os.path.basename(docx_path)}")

            with open(docx_path, "rb") as file:
                st.download_button(
                    label=f"📄 Download DOCX - {os.path.basename(docx_path)}",
                    data=file,
                    file_name=os.path.basename(docx_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"docx_{index}"
                )

# --- Single Form Generator ---
st.markdown("---")
st.header("📥 Single Salary Slip Generator")

with st.form("salary_form"):
    name = st.text_input("Name")
    designation = st.text_input("Designation")
    department = st.text_input("Department")
    total_days = st.number_input("Total Days", min_value=0, value=30)
    working_days = st.number_input("Working Days", min_value=0, value=26)
    weekly_off = st.number_input("Weekly Off", min_value=0, value=4)
    festival_off = st.number_input("Festival Off", min_value=0, value=0)
    paid_days = st.number_input("Paid Days", min_value=0, value=26)
    base = st.number_input("Salary Per Month", value=50000)
    month = st.text_input("Month", value="July 2025")
    salary = st.number_input("Salary", value=50000)
    bonus = st.number_input("Bonus", value=5000)
    other = st.number_input("Other", value=2000)
    esi = st.number_input("ESI", value=500)
    advance_till = st.number_input("Advance Till Date", value=10000)
    advance_deduct = st.number_input("Advance Deduct", value=2000)
    misc = st.number_input("MISC", value=300)

    submitted = st.form_submit_button("Generate Salary Slip")

if submitted:
    total = salary + bonus + other
    net_advance = advance_till - advance_deduct
    payable = total - (esi + advance_deduct + misc)
    payment_date = datetime.datetime.now().strftime("%d %B %Y")

    data = {
        "Name": name,
        "Designation": designation,
        "Department": department,
        "Total_Days": total_days,
        "Working_Days": working_days,
        "Weekly_Off": weekly_off,
        "Festival_Off": festival_off,
        "Paid_Days": paid_days,
        "Base": base,
        "Month": month,
        "Salary": salary,
        "Bonus": bonus,
        "Other": other,
        "Total": total,
        "ESI": esi,
        "Advance_Till_Date": advance_till,
        "Advance_Deduct": advance_deduct,
        "Net_Advance": net_advance,
        "MISC": misc,
        "Payable": payable,
        "Payment_Date": payment_date,
    }

    generated_path = generate_docx(data)
    st.session_state.generated_file = generated_path

if st.session_state.generated_file:
    with open(st.session_state.generated_file, "rb") as f:
        st.download_button(
            label="📄 Download Salary Slip (DOCX)",
            data=f,
            file_name=os.path.basename(st.session_state.generated_file),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="single_docx"
        )
