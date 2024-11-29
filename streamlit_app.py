import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Define the structure of the form with fields
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

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Certificate of Analysis", align="C", ln=True)
        self.ln(5)

    def add_row(self, label, value):
        self.set_font("Arial", size=12)
        self.cell(50, 10, f"{label}:", border=1)
        self.cell(0, 10, value, border=1, ln=True)

def create_pdf(data):
    pdf = CustomPDF()
    pdf.add_page()

    # Add data in rows
    for key, value in data.items():
        pdf.add_row(key, value)

    # Save to buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# Streamlit app
st.title("Food COA Form")
st.write("Fill in the required details below:")

user_inputs = {}
for field in fields:
    user_inputs[field] = st.text_input(field, placeholder=f"Enter {field}...")

if st.button("Generate PDF"):
    pdf_buffer = create_pdf(user_inputs)
    st.success("PDF generated successfully!")
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="COA_Food.pdf",
        mime="application/pdf",
    )
