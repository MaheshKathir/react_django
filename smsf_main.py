import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path


pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
words_to_find = ['Benefits Accrued during the period', 'Liability for Accrued Benefits at beginning of period',  'Benefits Paid during the period', 'Vested Benefits at end of period']

matched_values = {}

# Open the PDF using PyPDF2
pdf_reader = PdfFileReader(open(pdf_path, 'rb'))

with pdfplumber.open(pdf_path) as pdf:
    for word in words_to_find:
        matched_value = None
        matched_page_number = None
        for page_num, page in enumerate(pdf.pages):
            lines = page.extract_text().split('\n')
            for line in lines:
                if word in line:
                    values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                    if values:
                        matched_value = values[0]  # Extract the first value from the line
                        matched_page_number = page_num 
                        break
            if matched_value:
                break

        if matched_value:
            matched_values[word] = {
                'value': matched_value,
                'page_number': matched_page_number
            }

    # Create a new PDF using PyPDF2
    pdf_writer = PdfFileWriter()

    # Copy the existing pages to the new PDF
    for page_num in range(pdf_reader.getNumPages()):
        current_page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(current_page)

    for word in words_to_find:
        if word in matched_values:
            print(f"Matching value for '{word}':")
            print(f"Value: {matched_values[word]['value']}")
            print(f"Page number: {matched_values[word]['page_number']}")
            doc = fitz.open(pdf_path)
            page = doc[matched_values[word]['page_number']]
            page_no_to_place_link = matched_values[word]['page_number']
            print(f"page:{page}")
            # Get the text content of the page
            text_content = page.get_text()

            # Search for a specific word and retrieve its coordinates
            keyword = matched_values[word]['value']
            print(f"keyword_static:{keyword}")
            word_instances = page.search_for(keyword)
            if len(word_instances) > 0:
                for instance in word_instances:
                    x, y, x1, y1 = instance
                    print(f'Coordinates: x={x}, y={y}, width={x1-x}, height={y1-y}')
                    # Get the height of the page
                    page_height = page.rect.height

                    # Calculate the new y-coordinate for the bottom placement
                    new_y = page_height - y1

                    # Add a link to the new PDF using the updated coordinates
                    pdf_writer.addLink(
                        page_no_to_place_link,
                        0,
                        RectangleObject([x, new_y, x1, new_y + (y1 - y)]),
                        border=[2, 2, 2],
                    )
            else:
                print('Word not found in the PDF.')

    # Save the modified PDF
    output_file = path.abspath('testsample_112_pdf.pdf')
    with open(output_file, 'wb') as link_pdf:
        pdf_writer.write(link_pdf)

    print(f'Link added to the PDF: {output_file}')
