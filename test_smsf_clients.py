import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path 

start_account = "Liability for Accrued Benefits"
end_account = "Total Liability for Accrued Benefits"

pdf_path = 'No Links Clarkville Super Fund - Workpaper 2019.pdf'
pdf_reader_plumber = pdfplumber.open(pdf_path)

matched_values = {}
pdf_reader = PdfFileReader(open(pdf_path, 'rb'))

with pdf_reader_plumber as pdf:
    for page_num, page in enumerate(pdf.pages):
        lines = page.extract_text().split('\n')
        for line in lines:
            if start_account in line:
                # If start_account is matched, search for end_account in subsequent lines
                matched_page_number = page_num
                data_lines = []
                for subsequent_line in lines[lines.index(line) + 1:]:
                    values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', subsequent_line)
                    if values:
                        data_lines.append(values[0]) 
                    if end_account in subsequent_line:
                        # If end_account is found, extract the data from the collected lines
                        matched_values[start_account] = (data_lines[:-1], matched_page_number)
                        break  # Exit the loop if end_account is found
                break  # Exit the loop if start_account is found
            
    pdf_writer = PdfFileWriter()

    # Copy the existing pages to the new PDF
    for page_num in range(pdf_reader.getNumPages()):
        current_page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(current_page)
        
    # Print all matched data and their respective page numbers
    for start, (data, client_name_page) in matched_values.items():
        print("Start Account:", start)
        print("Matched Data:")
        for line_data in data:
            print(line_data)
            print("Page Number:", client_name_page)
            doc = fitz.open(pdf_path)
            
            matched_client_page = doc[client_name_page]
            
            client_nameTo_placeLink = client_name_page
            
            client_data_no = line_data
           
            word_intances = matched_client_page.search_for(client_data_no)
            if len(word_intances) > 0:
                for instance in word_intances:
                    x,y, x1,y1 = instance
                    print(f'coordinates: x={x}, y={y}, width={x1-x}, height= {y1-y}')
                    try:
                        page_height = matched_client_page.rect.height
                        
                        new_y = page_height - y1
                        
                        pdf_writer.addLink(
                            client_nameTo_placeLink,
                            26,
                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                            border=[1,1,1]
                        )
                    except:
                        pass
                    
            else:
                print('Word not found in the PDF.')

    # # Save the modified PDF
    # output_file = path.abspath('testsample_01222222121_pdf.pdf')
    # with open(output_file, 'wb') as link_pdf:
    #     pdf_writer.write(link_pdf)

    # print(f'Link added to the PDF: {output_file}')

    
