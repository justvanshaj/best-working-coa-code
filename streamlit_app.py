import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Define fields for user input
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

# FPDF class to replicate the table structure
class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Certificate of Analysis", align="C", ln=True)
        self.ln(5)

    def add_table_row(self, parameter, specification, test_result):
        self.set_font("Arial", size=12)
        self.cell(70, 10, parameter, border=1)
        self.cell(60, 10, specification, border=1)
        self.cell(60, 10, test_result, border=1, ln=True)

    def add_section(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

def create_pdf(data):
    pdf = CustomPDF()
    pdf.add_page()

    # Static header details
    header_data = {
        "Customer": "",
        "Product": "",
        "Date": "",
        "Batch No.": "",
        "Shelf-life": "",
        "Invoice No.": "",
        "PO No.": "",
    }

    pdf.set_font("Arial", size=12)
    for key, value in header_data.items():
        pdf.cell(50, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Add sections
    pdf.add_section("PARAMETERS SPECIFICATIONS TEST RESULTS")

    # Parameters section
    table_data = [
        ("Gum Content (%)", "more than 80%", data["Gum Content (%)"]),
        ("Moisture (%)", "less than 12%", data["Moisture (%)"]),
        ("Protein (%)", "less than 5%", data["Protein (%)"]),
        ("ASH Content (%)", "less than 1%", data["ASH Content (%)"]),
        ("AIR (%)", "less than 6%", data["AIR (%)"]),
        ("Fat (%)", "less than 1%", data["Fat (%)"]),
        ("Ph Levels", "5.5 - 7.0", data["Ph Levels"]),
        ("Arsenic", "less than 3.0 mg/kg", data["Arsenic"]),
        ("Lead", "less than 2.0 mg/kg", data["Lead"]),
        ("Heavy Metals", "less than 1.0 mg/kg", data["Heavy Metals"]),
        ("Through 100 Mesh", "99%", data["Through 100 Mesh"]),
        ("Through 200 Mesh", "95%-99%", data["Through 200 Mesh"]),
        ("APC/gm", "less than 5000/gm", data["APC/gm"]),
        ("Yeast & Mould", "less than 500/gm", data["Yeast & Mould"]),
        ("Coliform", "Negative", data["Coliform"]),
        ("Ecoli", "Negative", data["Ecoli"]),
        ("Salmonella", "Negative", data["Salmonella"]),
    ]

    # Add table rows
    for row in table_data:
        pdf.add_table_row(*row)

    return pdf

# Streamlit app
st.title("Certificate of Analysis Generator")
st.write("Fill in the required details below (only fields marked 'Fill' in the original):")

# Collect user inputs for the "Fill" fields
user_inputs = {}
for field in fields_to_fill:
    user_inputs[field] = st.text_input(field, placeholder=f"Enter {field}...")

if st.button("Generate PDF"):
    pdf = create_pdf(user_inputs)

    # Save PDF to a buffer for download
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
