import streamlit as st
from docx import Document
from docx.shared import RGBColor
from datetime import datetime
import mammoth
import io

# --- Placeholder replacement preserving style ---
def replace_style(doc, mapping):
    def proc_para(para):
        runs = para.runs
        text = ''.join(r.text for r in runs)
        for key, val in mapping.items():
            placeholder = f"{{{{ {key} }}}}"
            if placeholder in text:
                new_runs = []; acc = ""
                for r in runs:
                    acc += r.text; new_runs.append(r)
                    if placeholder in acc:
                        style_run = next((x for x in new_runs if placeholder in x.text), new_runs[0])
                        font = style_run.font
                        acc = acc.replace(placeholder, str(val))
                        for x in new_runs: x.text = ""
                        nr = new_runs[0]
                        nr.text = acc
                        nr.font.name = font.name; nr.font.size = font.size
                        nr.font.bold = font.bold; nr.font.italic = font.italic
                        nr.font.underline = font.underline
                        nr.font.color.rgb = font.color.rgb
                        break

    for p in doc.paragraphs: proc_para(p)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    proc_para(p)

# --- Generate docx from template ---
def gen_doc(data, tpl, out):
    doc = Document(tpl)
    replace_style(doc, data)
    doc.save(out)

# --- Preview converter ---
def docx_to_html(path):
    with open(path, "rb") as f:
        return mammoth.convert_to_html(f).value

# --- Streamlit UI ---
st.set_page_config("Salary Slip Generator", layout="wide")
st.title("💼 Salary Slip Generator")

with st.form("slip"):
    name = st.text_input("Name")
    desig = st.text_input("Designation")
    dept = st.text_input("Department")

    total_days = st.number_input("Total Days", min_value=0, value=30)
    working = st.number_input("Working Days", min_value=0, value=30)
    weekly_off = st.number_input("Weekly Off", min_value=0, value=4)
    fest_off = st.number_input("Festival Off", min_value=0, value=1)
    paid_days = st.number_input("Paid Days", min_value=0, value=total_days)

    base = st.number_input("Base Salary", min_value=0.0, value=0.0)
    month = st.text_input("Month & Year (e.g., July 2025)")
    salary = st.number_input("Salary", min_value=0.0, value=0.0)
    bonus = st.number_input("Bonus", min_value=0.0, value=0.0)
    other = st.number_input("Other Allowance", min_value=0.0, value=0.0)

    esi = st.number_input("ESI Deducted", min_value=0.0, value=0.0)
    adv_ded = st.number_input("Advance Deducted", min_value=0.0, value=0.0)
    adv_till = st.number_input("Advance Till Date", min_value=0.0, value=0.0)
    misc = st.number_input("Misc Deduction", min_value=0.0, value=0.0)

    submitted = st.form_submit_button("Generate Salary Slip")

if submitted:
    total = salary + bonus + other
    net_adv = adv_till - adv_ded
    payable = total - (esi + adv_ded + misc)
    pay_date = datetime.now().strftime("%B %Y")

    data = {
        "Name": name, "Designation": desig, "Department": dept,
        "Total_Days": total_days, "Working_Days": working,
        "Weekly_Off": weekly_off, "Festival_Off": fest_off,
        "Paid_Days": paid_days,
        "Base": base, "Month": month,
        "Salary": salary, "Bonus": bonus, "Other": other,
        "Total": total, "Net_Advance": net_adv,
        "Payment_Date": pay_date,
        "ESI": esi, "Advance_Deduct": adv_ded,
        "Advance_Till_Date": adv_till, "MISC": misc,
        "Payable": payable
    }

    tpl = "SALARY SLIP FORMAT.docx"
    out = "SALARY_SLIP_Generated.docx"
    gen_doc(data, tpl, out)

    try:
        html = docx_to_html(out)
        st.subheader("📄 Preview")
        st.components.v1.html(html, height=600, scrolling=True)
    except:
        st.warning("No preview available")

    with open(out, "rb") as f:
        buf = io.BytesIO(f.read())
        st.download_button("📥 Download Salary Slip", data=buf,
                           file_name=f"SalarySlip-{name}-{month}.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
