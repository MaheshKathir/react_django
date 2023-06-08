import pdfplumber
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path

pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
words_to_find = ['Employer', 'Government Co-Contributions']

matched_values = {}

# Open the PDF using pdfplumber
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
    pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
    for page_num in range(pdf_reader.getNumPages()):
        current_page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(current_page)

    for word in words_to_find:
        if word in matched_values:
            print(f"Matching value for '{word}':")
            print(f"Value: {matched_values[word]['value']}")
            print(f"Page number: {matched_values[word]['page_number']}")

            page_number = matched_values[word]['page_number']
            page = pdf.pages[page_number]

            sentence_to_find = 'Transactions: '
            to_find = sentence_to_find + word

            matched_goto_pagenumber = None
            for page_num, page in enumerate(pdf.pages):
                lines = page.extract_text().split('\n')
                for line in lines:
                    if to_find in line:
                        matched_goto_pagenumber = page_num
                        break

            if matched_goto_pagenumber is not None:
                # Search for a specific word and retrieve its coordinates
                keyword = matched_values[word]['value']
                print(f"Keyword: {keyword}")
                word_instances = page.search_for(keyword)

                if len(word_instances) > 0:
                    for instance in word_instances:
                        x0, y0, x1, y1 = instance['x0'], instance['top'], instance['x1'], instance['bottom']
                        print(f'Coordinates: x={x0}, y={y0}, width={x1-x0}, height={y1-y0}')

                        # Get the height of the page
                        page_height = page.height

                        # Calculate the new y-coordinate for the bottom placement
                        new_y = page_height - y1

                        # Add a link to the new PDF using the updated coordinates
                        pdf_writer.addLink(
                            page_number,
                            matched_goto_pagenumber,
                            RectangleObject([x0, new_y, x1, new_y + (y1 - y0)]),
                            border=[2, 2, 2],
                        )
                else:
                    print('Word not found in the PDF.')
            else:
                print(f"Cannot find '{to_find}' in the PDF.")

    # Save the modified PDF
    output_file = path.abspath('testsample_155555_pdf.pdf')
    with open(output_file, 'wb') as link_pdf:
        pdf_writer.write(link_pdf)

    print(f'Link added to the PDF: {output_file}')
