import streamlit as st
from fpdf import FPDF

# Define the structure of the form
fields = {
    "Customer": "",
    "Product": "",
    "Date": "",
    "Batch No.": "",
    "Shelf-life": "",
    "Invoice No.": "",
    "PO No.": "",
    "Gum Content (%)": "",
    "Moisture (%)": "",
    "Protein (%)": "",
    "ASH Content (%)": "",
    "AIR (%)": "",
    "Fat (%)": "",
    "Ph Levels": "",
    "Arsenic": "",
    "Lead": "",
    "Heavy Metals": "",
    "Through 100 Mesh": "",
    "Through 200 Mesh": "",
    "APC/gm": "",
    "Yeast & Mould": "",
    "Coliform": "",
    "Ecoli": "",
    "Salmonella": "",
}

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Certificate of Analysis", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    return pdf

# Streamlit form for user input
st.title("Food COA Form")
st.write("Fill in the required details below:")

user_inputs = {}
for field in fields:
    user_inputs[field] = st.text_input(field, placeholder=f"Enter {field}...")

if st.button("Generate PDF"):
    pdf = create_pdf(user_inputs)
    pdf_output_path = "/mnt/data/COA_Food.pdf"
    pdf.output(pdf_output_path)
    st.success("PDF generated successfully!")
    st.download_button(
        label="Download PDF",
        data=open(pdf_output_path, "rb").read(),
        file_name="COA_Food.pdf",
        mime="application/pdf",
    )
