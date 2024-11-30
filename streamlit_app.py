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
    "Viscosity After 2 Hours": "",
    "Viscosity After 24 Hours": "",
}

# Custom PDF Class
class COAPDF(FPDF):
    def add_table_row(self, col1, col2, col3=None):
        """Add a row to the table."""
        self.set_font("Arial", size=12)
        self.cell(70, 10, col1, border=1)
        self.cell(70, 10, col2, border=1)
        if col3 is not None:
            self.cell(50, 10, col3, border=1)
        self.ln()

    def add_section_title(self, title):
        """Add a section title with a centered header in the table."""
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, border=1, align="C", ln=True)

def create_pdf(data):
    pdf = COAPDF()
    pdf.add_page()

    # Header Section
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Customer: {data['Customer']}", border=1, ln=True)

    pdf.cell(70, 10, f"Product: {data['Product']}", border=1)
    pdf.cell(70, 10, f"Date: {data['Date']}", border=1, ln=True)

    pdf.cell(70, 10, f"Batch No.: {data['Batch No.']}", border=1)
    pdf.cell(70, 10, f"Shelf-life: {data['Shelf-life']}", border=1, ln=True)

    pdf.cell(70, 10, f"Invoice No.: {data['Invoice No.']}", border=1)
    pdf.cell(70, 10, f"PO No.: {data['PO No.']}", border=1, ln=True)

    pdf.ln(5)  # Spacing before the next section

    # Parameters Specifications and Results Table
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
    ]
    for row in table_data:
        pdf.add_table_row(*row)

    pdf.ln(5)

    # Organoleptic Analysis Section
    pdf.add_section_title("ORGANOLEPTIC ANALYSIS")
    organoleptic_data = [
        ("Appearance/Colour", "Cream/White Powder"),
        ("Odour", "Natural"),
        ("Taste", "Natural"),
    ]
    for parameter, value in organoleptic_data:
        pdf.add_table_row(parameter, value)

    pdf.ln(5)

    # Particle Size and Granulation Section
    pdf.add_section_title("PARTICLE SIZE AND GRANULATION")
    granulation_data = [
        ("Through 100 Mesh", "99%", data["Through 100 Mesh"]),
        ("Through 200 Mesh", "95%-99%", data["Through 200 Mesh"]),
    ]
    for row in granulation_data:
        pdf.add_table_row(*row)

    pdf.ln(5)

    # Viscosity Section
    pdf.add_section_title("VISCOSITY")
    pdf.add_table_row("After 2 hours", "≥ BLANK cps", data["Viscosity After 2 Hours"])
    pdf.add_table_row("After 24 hours", "≤ BLANK cps", data["Viscosity After 24 Hours"])

    pdf.ln(5)

    # Microbiological Analysis Section
    pdf.add_section_title("MICROBIOLOGICAL ANALYSIS")
    microbiological_data = [
        ("APC/gm", "less than 5000/gm", data["APC/gm"]),
        ("Yeast & Mould", "less than 500/gm", data["Yeast & Mould"]),
        ("Coliform", "Negative", data["Coliform"]),
        ("Ecoli", "Negative", data["Ecoli"]),
        ("Salmonella", "Negative", data["Salmonella"]),
    ]
    for row in microbiological_data:
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
