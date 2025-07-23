import streamlit as st
from docx import Document
import mammoth
from datetime import datetime
import os

# --- Replace placeholders while preserving format ---
def replace_placeholders(doc, replacements):
    def process_runs(runs):
        full_text = ''.join(run.text for run in runs)
        for key, val in replacements.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in full_text:
                full_text = full_text.replace(placeholder, str(val))
                for run in runs:
                    run.text = ''
                if runs:
                    runs[0].text = full_text
                break

    for para in doc.paragraphs:
        process_runs(para.runs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    process_runs(para.runs)

# --- Generate the output salary slip DOCX ---
def generate_salary_doc(data, template_path, output_path):
    doc = Document(template_path)
    replace_placeholders(doc, data)
    doc.save(output_path)
    return output_path

# --- Optional HTML preview ---
def preview_docx_as_html(docx_path):
    with open(docx_path, "rb") as file:
        result = mammoth.convert_to_html(file)
        return result.value

# --- Streamlit UI ---
st.set_page_config("Salary Slip Generator", layout="centered")
st.title("🧾 Salary Slip Generator")

with st.form("salary_form"):
    name = st.text_input("Employee Name")
    designation = st.text_input("Designation")
    department = st.text_input("Department")
    month = st.text_input("Month (e.g., July 2025)")
    total_days = st.number_input("Total Days", 0, 31, 30)
    working_days = st.number_input("Working Days", 0, 31, 26)
    weekly_off = st.number_input("Weekly Off", 0, 10, 4)
    festival_off = st.number_input("Festival Off", 0, 5, 1)
    paid_days = st.number_input("Paid Days", 0, 31, 25)

    base = st.number_input("Base Salary (Monthly)", 0.0)
    salary = st.number_input("Salary", 0.0)
    bonus = st.number_input("Bonus", 0.0)
    other = st.number_input("Other Earnings", 0.0)
    esi = st.number_input("ESI", 0.0)
    advance_till_date = st.number_input("Advance Till Date", 0.0)
    advance_deduct = st.number_input("Advance Deduct", 0.0)
    misc = st.number_input("Misc Deductions", 0.0)

    submitted = st.form_submit_button("Generate Salary Slip")

if submitted:
    try:
        total = round(salary + bonus + other, 2)
        net_advance = round(advance_till_date - advance_deduct, 2)
        payable = round(total - (esi + advance_deduct + misc), 2)
        payment_date = datetime.now().strftime("%B %d, %Y")

        replacements = {
            "Name": name,
            "Designation": designation,
            "Department": department,
            "Month": month,
            "Total_Days": total_days,
            "Working_Days": working_days,
            "Weekly_Off": weekly_off,
            "Festival_Off": festival_off,
            "Paid_Days": paid_days,
            "Base": base,
            "Salary": salary,
            "Bonus": bonus,
            "Other": other,
            "Total": total,
            "ESI": esi,
            "Advance_Till_Date": advance_till_date,
            "Advance_Deduct": advance_deduct,
            "Net_Advance": net_advance,
            "MISC": misc,
            "Payable": payable,
            "Payment_Date": payment_date
        }

        template = "SALARY SLIP FORMAT.docx"
        output_path = f"SalarySlip_{name.replace(' ', '_')}.docx"

        generate_salary_doc(replacements, template, output_path)

        # Preview
        st.subheader("📄 Preview")
        html = preview_docx_as_html(output_path)
        st.components.v1.html(f"<div style='padding:20px'>{html}</div>", height=600, scrolling=True)

        # Download
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Salary Slip (DOCX)",
                data=f,
                file_name=output_path,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")
