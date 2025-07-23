import streamlit as st
from docx import Document
import datetime
import os
import base64
import pandas as pd
from io import BytesIO
from docx2pdf import convert

# --- Replace placeholders preserving formatting ---
def replace_placeholders(doc, replacements):
    for p in doc.paragraphs:
        for key, val in replacements.items():
            if f"{{{{{key}}}}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if f"{{{{{key}}}}}" in inline[i].text:
                        inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(val))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for key, val in replacements.items():
                        if f"{{{{{key}}}}}" in p.text:
                            inline = p.runs
                            for i in range(len(inline)):
                                if f"{{{{{key}}}}}" in inline[i].text:
                                    inline[i].text = inline[i].text.replace(f"{{{{{key}}}}}", str(val))

# --- Generate DOCX ---
def generate_docx(data, template_path="SALARY SLIP FORMAT.docx"):
    doc = Document(template_path)
    replace_placeholders(doc, data)
    output_path = f"generated_slip_{data['Name'].replace(' ', '_')}.docx"
    doc.save(output_path)
    return output_path

# --- Convert DOCX to PDF ---
def convert_to_pdf(docx_path):
    pdf_path = docx_path.replace(".docx", ".pdf")
    convert(docx_path, pdf_path)
    return pdf_path

# --- Streamlit App ---
st.set_page_config(page_title="Salary Slip Generator", layout="wide")
st.title("🧾 Salary Slip Generator")

with st.expander("📤 Bulk COA Generator from Excel"):
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ Uploaded {len(df)} row(s)")
        generated_files = []

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

            out_path = generate_docx(data)
            st.success(f"✅ Generated: {os.path.basename(out_path)}")
            with open(out_path, "rb") as f:
                st.download_button(
                    label=f"📄 Download {os.path.basename(out_path)}",
                    data=f,
                    file_name=os.path.basename(out_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            # PDF version
            pdf_path = convert_to_pdf(out_path)
            with open(pdf_path, "rb") as pdf:
                st.download_button(
                    label=f"🧾 Download PDF for {name}",
                    data=pdf,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

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

        out_path = generate_docx(data)
        st.success(f"✅ Generated: {os.path.basename(out_path)}")
        with open(out_path, "rb") as f:
            st.download_button(
                label="📄 Download Salary Slip (DOCX)",
                data=f,
                file_name=os.path.basename(out_path),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # Optional PDF
        pdf_path = convert_to_pdf(out_path)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="🧾 Download Salary Slip (PDF)",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
