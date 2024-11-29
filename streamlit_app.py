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

    pdf.ln(10)  # Spacing before the Organoleptic Analysis section

    # Add Organoleptic Analysis section
    pdf.add_section_title("ORGANOLEPTIC ANALYSIS")
    organoleptic_data = [
        ("Appearance/Colour", "Cream/White Powder"),
        ("Odour", "Natural"),
        ("Taste", "Natural"),
    ]
    for parameter, value in organoleptic_data:
        pdf.add_field(parameter, value)

    pdf.ln(10)  # Spacing before the Parameters Table

    # Add Parameters Table
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
