import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path

pdf_path = 'No Links Clarkville Super Fund - Workpaper 2019.pdf'
words_to_find = ['Employer', 'Government Co-Contributions', 'Interest', 'Other Income',
                 'Actuarial Fee', 'ASIC Fee', 'Financial Planning Fees', 'Fund Administration Fee',
                 'Investment Expenses', 'SMSF Supervisory Levy', 'Receivables' , 'Member', 'Accountancy Fee']

start_account = "Liability for Accrued Benefits"
end_account = "Total Liability for Accrued Benefits"

matched_values = {}
matched_client_values = {}

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
            print(page)
            # print(f"page:{page}")
            # Get the text content of the page
            # text_content = page.get_text()

            # Search for a specific word and retrieve its coordinates
            keyword = matched_values[word]['value']
            # print(f"keyword_static:{keyword}")
            word_instances = page.search_for(keyword)
            if len(word_instances) > 0:
                for instance in word_instances:
                    x, y, x1, y1 = instance
                    print(f'Coordinates: x={x}, y={y}, width={x1-x}, height={y1-y}')
                    # Get the height of the page
                    try:
                        page_height = page.rect.height

                        # Calculate the new y-coordinate for the bottom placement
                        new_y = page_height - y1

                        # Add a link to the new PDF using the updated coordinates
                        sentence_to_find = "Transactions: "
                        to_find = sentence_to_find + word
                        
                        second_sentence = 'Total '
                        total_word_toFind = second_sentence + word

                        matched_goto_pagenumber = None
                        for page_num, page in enumerate(pdf.pages):
                            lines = page.extract_text().split('\n')
                            for line in lines:
                                if to_find in line:
                                    # matched_goto_pagenumber = page_num
                                    for subsequent_line in lines[lines.index(line) + 1:]:
                                        if total_word_toFind in subsequent_line:
                                            matched_goto_pagenumber = page_num
                                            print(matched_goto_pagenumber)
                                            break
                                    # print(matched_goto_pagenumber)
                                    # print(to_find)
                                    break
                        pdf_writer.addLink(
                            page_no_to_place_link,
                            matched_goto_pagenumber,
                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                            border=[1, 1, 1]
                        )
                        
                        # with pdfplumber.open(pdf_path) as pdf:
                        page = pdf.pages[matched_goto_pagenumber]

                        texts = page.extract_text().split('\n')
                        for text in texts:
                            if total_word_toFind in text:
                                data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)
                                if data:
                                    matched_data = data[-1]
                                    doc = fitz.open(pdf_path)
                                    matched_page = doc[matched_goto_pagenumber]
                                  
                                    # print('-------------',matched_data)
                                    keyword = matched_data
                                    word_instances = matched_page.search_for(keyword)
                                    if len(word_instances) > 0:
                                        # for instance in word_instances:
                                            # print(word_instances[-1])
                                            # print('Instance:',instance)
                                            # print('Word - Instance:',word_instances)
                                            x, y, x1, y1 = word_instances[-1]
                                            # print(f'Coordinates_11: x={x}, y={y}, width={x1-x}, height={y1-y}')
                                    
                                            page_height = matched_page.rect.height

                                            # Calculate the new y-coordinate for the bottom placement
                                            new_y = page_height - y1
                                            pdf_writer.addLink(
                                                matched_goto_pagenumber,
                                                page_no_to_place_link,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border=[1, 1, 1]
                                            )
                                            print("end")
                                            break                           
                    except:
                        pass
            else:
                print('Word not found in the PDF.')
    

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
                        matched_client_values[start_account] = (data_lines[:-1], matched_page_number)
                        break  # Exit the loop if end_account is found
                break  # Exit the loop if start_account is found
            
    # pdf_writer = PdfFileWriter()

    # # Copy the existing pages to the new PDF
    # for page_num in range(pdf_reader.getNumPages()):
    #     current_page = pdf_reader.getPage(page_num)
    #     pdf_writer.addPage(current_page)
        
    # Print all matched data and their respective page numbers
    for start, (data, client_name_page) in matched_client_values.items():
        print("Start Account:", start)
        print("Matched Data:")
        for line_data in data:
            print(line_data)
            print("Page Number:", client_name_page)
            doc = fitz.open(pdf_path)
            matched_client_page = doc[client_name_page]
            print("*****", matched_client_page)
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
    
    # Save the modified PDF
    output_file = path.abspath('testsample_007_pdf.pdf')
    with open(output_file, 'wb') as link_pdf:
        pdf_writer.write(link_pdf)

    print(f'Link added to the PDF: {output_file}')
   