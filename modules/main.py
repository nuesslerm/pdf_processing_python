import PyPDF2

# if file conversion is complaining about file not being in binary mode,
# then use rb so read file to binary, b = "binary"
with open("./pdf_assets/dummy.pdf", "rb") as dummy:
    reader = PyPDF2.PdfFileReader(dummy)

    first_page = reader.getPage(0)
    first_page.rotateCounterClockwise(90)

    writer = PyPDF2.PdfFileWriter()
    writer.addPage(first_page)

    with open("./pdf_assets/tilt.pdf", "wb") as edited_dummy:
        writer.write(edited_dummy)
