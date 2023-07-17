# Pypdf FileReader and Writer  Deprecated Error -> pip install 'PyPDF2<3.0'

import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path
import os

list = ['!@#$%12345','1111']
password = input("Password: ")
if password in list:
    
    path_folder = 'c:\Test_Folder\smsf_link_automation'

    for root, dirs, files in os.walk(path_folder):
        for pdf_file in files:
            pdf_path = path.join(root, pdf_file)
            words_to_find = ['Cash At Bank', 'Foreign At Bank', 'Employer', 'Government Co-Contributions', 'Interest', 'Other Income',
                            'Actuarial Fee', 'ASIC Fee', 'Financial Planning Fees', 'Fund Administration Fee',
                            'Investment Expenses', 'SMSF Supervisory Levy', 'Receivables' , 'Member', 'Accountancy Fee','Rent']
            
            bank_list = ['Cash At Bank', 'Foreign At Bank']

            start_account = "Liability for Accrued Benefits"
            end_account = "Total Liability for Accrued Benefits"
            
            start_investment = 'Investments'
            end_investment = "Other Assets"
            
            investment_summary = 'Investment Summary'
            

            matched_values = {}
            matched_client_values = {}
            matched_investment_values = {}

            # Open the PDF using PyPDF2
            pdf_reader = PdfFileReader(open(pdf_path, 'rb'))

            with pdfplumber.open(pdf_path) as pdf:
                for word in words_to_find:
                    matched_value = None
                    matched_page_number = None
                    matched_word = None
                    for page_num, page in enumerate(pdf.pages):
                        lines = page.extract_text().split('\n')
                        for line in lines:
                            if word in line:
                                values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                if values:
                                    matched_value = values[0]  # Extract the first value from the line
                                    matched_page_number = page_num
                                    matched_word = word
                                    break
                        if matched_value:
                            break

                    if matched_value:
                        matched_values[word] = {
                            'value': matched_value,
                            'page_number': matched_page_number,
                            'word': matched_word
                        }

                # Create a new PDF using PyPDF2
                pdf_writer = PdfFileWriter()

                # Copy the existing pages to the new PDF
                for page_num in range(pdf_reader.getNumPages()):
                    current_page = pdf_reader.getPage(page_num)
                    pdf_writer.addPage(current_page)

                for word in words_to_find:
                    if word in matched_values:
                      
                        doc = fitz.open(pdf_path)
                        page = doc[matched_values[word]['page_number']]
                        page_no_to_place_link = matched_values[word]['page_number']
                        print(page)
                       

                        # Search for a specific word and retrieve its coordinates
                        keyword = matched_values[word]['value']
                        matched_word_string = matched_values[word]['word']
                        if matched_word_string not in bank_list:
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
                                                    print("to_find:", to_find)
                                                    print('total_word_toFind:',total_word_toFind)
                                                    # matched_goto_pagenumber = page_num
                                                    for subsequent_line in lines[lines.index(line) + 1:]:
                                                        if total_word_toFind in subsequent_line:
                                                            print('total_word_toFind:',total_word_toFind)
                                                            matched_goto_pagenumber = page_num
                                                            print(matched_goto_pagenumber)
                                                            break
                                            if matched_goto_pagenumber is None:
                                                i = page_num + 1
                                                for date in enumerate(pdf.pages):
                                                    next_line = pdf.pages[i].extract_text().split('\n')
                                                    for end_line in next_line:
                                                        if total_word_toFind in end_line:
                                                            matched_goto_pagenumber = i
                                                            print('valueeee:', matched_goto_pagenumber)
                                                            break
                                                    if matched_goto_pagenumber is None:
                                                        i += 1
                                                    else:
                                                        break
                                                    
                                                    break
                                        pdf_writer.addLink(
                                            page_no_to_place_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border=[1, 1, 1]
                                        )

                                    
                                        page = pdf.pages[matched_goto_pagenumber]

                                        texts = page.extract_text().split('\n')
                                        for text in texts:
                                            if total_word_toFind in text:
                                                data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)
                                                if data:
                                                    matched_data = data[-1]
                                                    doc = fitz.open(pdf_path)
                                                    matched_page = doc[matched_goto_pagenumber]

                                                
                                                    keyword = matched_data
                                                    word_instances = matched_page.search_for(keyword)
                                                    if len(word_instances) > 0:
                                                    
                                                            x, y, x1, y1 = word_instances[-1]
                                                        
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
                                        # sentence_to_find = "Transactions: "
                                        # to_find = sentence_to_find + word

                                        # second_sentence = 'Total '
                                        # total_word_toFind = second_sentence + word

                                        matched_goto_pagenumber = None
                                        for page_num, page in enumerate(pdf.pages):
                                            lines = page.extract_text().split('\n')
                                            for line in lines:
                                                if investment_summary in line:
                                                    matched_goto_pagenumber = page_num - 1
                                                    print(matched_goto_pagenumber)
                                                    break
                                            
                                        pdf_writer.addLink(
                                            page_no_to_place_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border=[1, 1, 1]
                                        )
                                            
                                    except:
                                        pass

                for page_num, page in enumerate(pdf.pages):
                    lines = page.extract_text().split('\n')
                    for line in lines:
                        if start_account in line:
                            # If start_account is matched, search for end_account in subsequent lines
                            matched_page_number = page_num
                            data_lines = []
                            for subsequent_line in lines[lines.index(line) + 1:]:
                                values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', subsequent_line)
                                print('client_name:', subsequent_line)
                                if values:
                                    data_lines.append(values[0]) 
                                if end_account in subsequent_line:
                                    # If end_account is found, extract the data from the collected lines
                                    matched_client_values[start_account] = (data_lines[:-1], matched_page_number)
                                    break  # Exit the loop if end_account is found
                            break  # Exit the loop if start_account is found
                    for line in lines:
                        if start_investment in line:
                            investments_page_no = page_num
                            data_investment = []
                            for subsequent_investment_line in lines[lines.index(line) + 1:]:
                                values_investment = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', subsequent_investment_line)
                                if values_investment:
                                    data_investment.append(values_investment[0])
                                if end_investment in subsequent_investment_line:
                                    matched_investment_values[start_investment] = (data_investment[:-1], investments_page_no)
                                    break
                            break
                    
                    
                # Print all matched data and their respective page numbers
                for start, (data, client_name_page) in matched_client_values.items():
                    
                    for line_data in data:
                        print(line_data)
                        print("Page Number:", client_name_page)
                        doc = fitz.open(pdf_path)
                        matched_client_page = doc[client_name_page]
                        print("*****", matched_client_page)
                        client_nameTo_placeLink = client_name_page
                        
                        client_data_no = line_data
                        consolidated_memberString= 'Consolidated Member Benefit Totals'
                        matched_consolidatedPageNo = None

                        for page_num, page in enumerate(pdf.pages):
                            lines = page.extract_text().split('\n')
                            for line in lines:
                                 if consolidated_memberString in line:
                                     for consolidated_subsequent_line in lines[lines.index(line) + 1:]:
                                         if line_data in consolidated_subsequent_line:
                                             matched_consolidatedPageNo = page_num
                                             break
                            if matched_consolidatedPageNo is None:
                                i = page_num + 1
                                for date in enumerate(pdf.pages):
                                    try:
                                        next_line = pdf.pages[i].extract_text().split('\n')
                                        for end_line in next_line:
                                            if consolidated_memberString in end_line:
                                                for subsequent_line in next_line[next_line.index(end_line) + 1:]:
                                                    if line_data in subsequent_line:
                                                        matched_consolidatedPageNo = i
                                                        print('consolidated_value:', matched_consolidatedPageNo)
                                                        break
                                        if matched_consolidatedPageNo is None:
                                            i += 1
                                        else:
                                            break
                                    except:
                                        pass
                                    
                                    break
                                
                        
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
                                        matched_consolidatedPageNo,
                                        RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                        border=[1,1,1]
                                    )
                                except:
                                    pass
                                
                        doc = fitz.open(pdf_path)
                        matched_client_page_up = doc[matched_consolidatedPageNo]        
                        word_intances = matched_client_page_up.search_for(client_data_no)
                      
                        if len(word_intances) > 0:
                           
                            x,y, x1,y1 = word_intances[-2]
                            print(f'coordinates: x={x}, y={y}, width={x1-x}, height= {y1-y}')
                            try:
                                page_height = matched_client_page_up.rect.height
                                    
                                new_y = page_height - y1
                                    
                                pdf_writer.addLink(
                                    matched_consolidatedPageNo,
                                    client_nameTo_placeLink,
                                    RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                    border=[1,1,1]
                                )
                            except:
                                pass
                                
                        else:
                            print('Word not found in the PDF.')
                            
                for start,(data, investment_page) in matched_investment_values.items():
                    print('start investment:', start)
                    print('matched Investment data:')
                    for line_data in data:
                        print(line_data)
                        print('Investment_page_no:', investment_page)
                        doc = fitz.open(pdf_path)
                        matched_investment_page = doc[investment_page]
                        print("******", matched_investment_page)
                        investment_subline_placeLink = investment_page
                        
                        investment_data_no = line_data
                        
                        #To find the investment summary page number
                        investment_summary = 'Investment Summary'
                        matched_investment_pageNo = None
                        
                        for page_num, page in enumerate(pdf.pages):
                            lines = page.extract_text().split('\n')
                            for line in lines:
                                if investment_summary in line:
                                    for subsequent_line in lines[lines.index(line) + 1:]:
                                        if line_data in subsequent_line:
                                            matched_investment_pageNo = page_num
                                            break
                            if matched_investment_pageNo is None:
                                i = page_num + 1
                                for date in enumerate(pdf.pages):
                                    try:
                                        next_line = pdf.pages[i].extract_text().split('\n')
                                        for end_line in next_line:
                                            if investment_summary in end_line:
                                                for investment_subsequent_line in next_line[next_line.index(end_line) + 1:]:
                                                    if line_data in investment_subsequent_line:
                                                        matched_investment_pageNo = i
                                                        print('investment_value:', matched_investment_pageNo)
                                                        break
                                        if matched_investment_pageNo is None:
                                            i += 1
                                        else:
                                            break
                                    except:
                                       pass
                                  
                                    break
                                        
                                                                    
                        word_instances = matched_investment_page.search_for(investment_data_no)
                        if len(word_instances) > 0:
                            for instance in word_instances:
                                x,y ,x1,y1 = instance
                                print(f'Investment_coordinates: x={x}, y={y}, width={x1-x}, height= {y1-y}')
                                try:
                                    page_height = matched_investment_page.rect.height
                                    
                                    new_y = page_height - y1
                                    pdf_writer.addLink(
                                        investment_subline_placeLink,
                                        matched_investment_pageNo,
                                        RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                        border=[1,1,1]    
                                    )
                                except: 
                                    pass
                        else:
                            print('Investment word not found in the pdf')
                                
                                                
                # Save the modified PDF
                filename = os.path.splitext(pdf_file)[0]  # Extract the filename without extension
                output_file = path.join(path_folder, f"Auto_link_{filename}.pdf")
                with open(output_file, 'wb') as link_pdf:
                    pdf_writer.write(link_pdf)
                print(f'Link added to the PDF: {output_file}')
else:
    print('Password is Incorrrect')
