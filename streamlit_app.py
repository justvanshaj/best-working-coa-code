import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Define the fields to be filled by the user
fields_to_fill = {
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

# FPDF class to format the PDF exactly like the original
class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Certificate of Analysis", align="C", ln=True)
        self.ln(10)

    def add_static_row(self, label, value=""):
        self.set_font("Arial", size=12)
        self.cell(50, 10, f"{label}:", border=0)
        self.cell(0, 10, value, border=0, ln=True)

    def add_fillable_row(self, label, value):
        self.set_font("Arial", size=12)
        self.cell(50, 10, f"{label}:", border=0)
        self.cell(0, 10, value, border=0, ln=True)

    def add_section(self, section_title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, section_title, border=0, ln=True)
        self.ln(5)

def create_pdf(data):
    pdf = CustomPDF()
    pdf.add_page()

    # Static fields (unchanged)
    static_fields = {
        "Customer": "",
        "Product": "",
        "Date": "",
        "Batch No.": "",
        "Shelf-life": "",
        "Invoice No.": "",
        "PO No.": "",
    }

    # Add static fields
    for key, value in static_fields.items():
        pdf.add_static_row(key, value)

    pdf.ln(5)  # Add some spacing before dynamic fields

    # Fillable fields (user input replaces "Fill")
    for key, value in data.items():
        pdf.add_fillable_row(key, value if value else "Fill")

    return pdf

# Streamlit app
st.title("Certificate of Analysis Form")
st.write("Fill in the required fields below:")

# Collect user inputs for the fillable fields
user_inputs = {}
for field in fields_to_fill:
    user_inputs[field] = st.text_input(field, placeholder=f"Enter {field}...")

if st.button("Generate PDF"):
    pdf = create_pdf(user_inputs)

    # Save the PDF to a buffer for download
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.success("PDF generated successfully!")
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="COA_Food_Filled.pdf",
        mime="application/pdf",
    )
