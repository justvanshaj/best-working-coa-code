import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Define the fields for user input
fields_to_fill = {
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

# Custom PDF Class
class COAPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Certificate of Analysis", align="C", ln=True)
        self.ln(10)

    def add_field(self, label, value):
        self.set_font("Arial", size=12)
        self.cell(40, 10, f"{label}:", border=0)
        self.cell(0, 10, value, border=0, ln=True)

    def add_table_row(self, col1, col2, col3):
        self.set_font("Arial", size=12)
        self.cell(70, 10, col1, border=1)
        self.cell(60, 10, col2, border=1)
        self.cell(60, 10, col3, border=1, ln=True)

    def add_section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

def create_pdf(data):
    pdf = COAPDF()
    pdf.add_page()

    # Add header fields
    header_data = {
        "Customer": data["Customer"],
        "Product": data["Product"],
        "Date": data["Date"],
        "Batch No.": data["Batch No."],
        "Shelf-life": data["Shelf-life"],
        "Invoice No.": data["Invoice No."],
        "PO No.": data["PO No."],
    }
    for key, value in header_data.items():
        pdf.add_field(key, value)

    pdf.ln(10)  # Spacing before the table

    # Add table section
    pdf.add_section_title("PARAMETERS SPECIFICATIONS TEST RESULTS")
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
    for row in table_data:
        pdf.add_table_row(*row)

    return pdf

# Streamlit App
st.title("Certificate of Analysis Generator")
st.write("Fill in the fields below to generate a COA PDF:")

# Collect user inputs
user_inputs = {field: st.text_input(field, placeholder=f"Enter {field}...") for field in fields_to_fill}

if st.button("Generate PDF"):
    pdf = create_pdf(user_inputs)

    # Save PDF to buffer
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
