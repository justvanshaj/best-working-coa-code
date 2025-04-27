import streamlit as st
from docx import Document
from io import BytesIO
import datetime

def calculate_components(moisture):
    # Based on your sample document:
    # Moisture + Gum + Protein + Ash + AIR + Fat = 100
    gum = 81.61
    protein = 3.15
    ash = 0.64
    air = 3.0
    fat = 0.70

    total_others = gum + protein + ash + air + fat
    adjustment = 100 - (moisture + total_others)

    gum += adjustment  # Distribute entire adjustment to Gum Content

    return round(gum, 2), protein, ash, air, fat

def generate_docx(cps_range, batch_no, moisture, ph_level, through_100, through_200, cps_2hr, cps_24hr):
    gum, protein, ash, air, fat = calculate_components(moisture)

    doc = Document()

    doc.add_heading(f'PRODUCT:{cps_range}', level=1)
    doc.add_paragraph(f'Date: {datetime.date.today().strftime("%d-%m-%Y")}')
    doc.add_paragraph(f'BATCH NO.: {batch_no}')
    doc.add_paragraph('Shelf-life: 2 Years')
    doc.add_paragraph('')
    doc.add_heading('PARAMETERS', level=2)

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'PARAMETERS'
    hdr_cells[1].text = 'SPECIFICATIONS'
    hdr_cells[2].text = 'TEST RESULTS'

    # Organolectic
    organo = [
        ('Appearance/Colour', 'Cream/White Powder', 'Cream/White Powder'),
        ('Odour', 'Natural', 'Natural'),
        ('Taste', 'Natural', 'Natural')
    ]

    # Technical Specs
    technical = [
        ('Gum Content (%)', 'more than 80%', f'{gum}%'),
        ('Moisture (%)', 'less than 12%', f'{moisture}%'),
        ('Protein (%)', 'less than 5%', f'{protein}%'),
        ('ASH Content (%)', 'less than 1%', f'{ash}%'),
        ('AIR (%)', 'less than 6%', f'{air}%'),
        ('Fat (%)', 'less than 1%', f'{fat}%'),
        ('Ph Levels', '5.5 - 7.0', f'{ph_level}'),
        ('Arsenic', 'less than 3.0 mg/kg', '0.25 mg/kg'),
        ('Lead', 'less than 2.0 mg/kg', '0.025 mg/kg'),
        ('Heavy Metals', 'less than 1.0 mg/kg', '0.025 mg/kg')
    ]

    # Granulation
    granulation = [
        ('Through 100 Mesh', '99%', f'{through_100}%'),
        ('Through 200 Mesh', '95%-99%', f'{through_200}%')
    ]

    # Viscosity
    viscosity = [
        ('After 2 hours', '≥5500CPS', f'{cps_2hr} CPS (1% solution, W/W, Spindle No. 4, RPM-20, at 25°C, Cold - Brookfield Viscometer - RVDV)'),
        ('After 24 hours', '≤6000CPS', f'{cps_24hr} CPS (1% solution, W/W, Spindle No. 4, RPM-20, at 25°C, Cold - Brookfield Viscometer - RVDV)')
    ]

    # Microbiological
    micro = [
        ('APC/gm', 'less than 5000 cfu/g', '<100'),
        ('Yeast & Mould', 'less than 500 cfu/g', 'Absent'),
        ('Coliform', 'Negative', 'Absent'),
        ('Ecoli', 'Negative', 'Absent'),
        ('Salmonella', 'Negative', 'Absent')
    ]

    sections = [organo, technical, granulation, viscosity, micro]

    for section in sections:
        for param, spec, result in section:
            row_cells = table.add_row().cells
            row_cells[0].text = param
            row_cells[1].text = spec
            row_cells[2].text = result

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit App
st.title('Batch Quality Report Generator')

with st.form('input_form'):
    cps_range = st.text_input('CPS Range (e.g., 5500-6000 CPS)')
    batch_no = st.text_input('Batch Number')
    moisture = st.number_input('Moisture (%)', min_value=0.0, max_value=20.0, step=0.01)
    ph_level = st.number_input('pH Level', min_value=0.0, max_value=14.0, step=0.01)
    through_100 = st.number_input('Through 100 Mesh (%)', min_value=0.0, max_value=100.0, step=0.01)
    through_200 = st.number_input('Through 200 Mesh (%)', min_value=0.0, max_value=100.0, step=0.01)
    cps_2hr = st.number_input('Viscosity After 2 hours (CPS)', min_value=0, max_value=10000, step=1)
    cps_24hr = st.number_input('Viscosity After 24 hours (CPS)', min_value=0, max_value=10000, step=1)
    
    submitted = st.form_submit_button('Generate PDF')

if submitted:
    pdf_file = generate_docx(cps_range, batch_no, moisture, ph_level, through_100, through_200, cps_2hr, cps_24hr)
    st.success('PDF generated successfully!')
    st.download_button('Download PDF', pdf_file, file_name=f'{batch_no}_Quality_Report.docx')
