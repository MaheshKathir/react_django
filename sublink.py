# Pypdf FileReader and Writer getting  Deprecated Error means install this  -> pip install 'PyPDFpip2<3.0'
# To Resolve the fitz error , need to install this pymupdf                  -> pip install pymupdf
# for pip                                                                   -> py -m pip


#Modules or libraries for this project

import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path
import os
import time



import time
import pyautogui

#this module for mask the input text 
import pwinput


def pdf_automation():
    #For password functionality
    password_list  = ['!@#$%12345','1111','sbsl@123']
    password = pwinput.pwinput(prompt='Password: ', mask='*')

    
    if password in password_list: 

        # path_folder = 'C:\BGL_Test_Folder'
        print("\nInfo: When you open the file explorer, you'll see the path in the address bar, for example - 'C:Users\Lin\Desktop\PDF Files'")                      
        path_folder =input("\nEnter your 'PDF' folder's path here to generate link: ")
        out_path_folder = input("\nEnter the path where you want to save the 'PDF' file: ")

        for root, dirs, files in os.walk(path_folder):
            for pdf_file in files:
                pdf_path = path.join(root, pdf_file)

                #Below defined over all words are read from text file

                # opening the file in read mode 
                my_file = open("words.txt", "r") 

                # reading the file 
                data = my_file.read() 

                # replacing end splitting the text 
                # when newline ('\n') is seen. 
                words_to_find = data.split("\n") 
              
                #Below defined investment summary based words are read from text file
                my_word_file = open('investment_summary_words.txt', 'r')
                data_investment_summary_words = my_word_file.read()
                investment_summary_words = data_investment_summary_words.split('\n')

                #This below list is used to palce link based on total credits string on the pdf
                word_based_credits = ['PAYG Payable','Employer Contributions','Interest Received','Employer Contributions','Personal Non Concessional',
                                    'Personal Concessional', 'Other Contributions','Other Investment Income','Property Income','Forex Gain/Loss']

                #For matched values has to store as dictionary data structure
                matched_values = {}
                matched_investment_amount_values = {}
                Link_notGenerated = []
                gui_automation_pageNo = []
               
                #Open the PDF_file Using PyPDF2
                pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
                
                #For using pdfplumber to get the matched values like page number , matched values data
                with pdfplumber.open(pdf_path)  as pdf:
                    for word in words_to_find:
                        matched_amount = None
                        matched_page_number = None
                        matched_word = None
                        for page_num, page in enumerate(pdf.pages):
                            if page_num <= 3:
                                lines = page.extract_text().split('\n')
                                for line in lines:
                                    
                                    if word in line:
                                       
                                        data_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                    
                                        if data_values:
                                           if data_values[0] != '0' and data_values[0] != '0.00':

                                                matched_amount = data_values[0]   # Extract the first value from the line
                                              
                                                matched_page_number = page_num
                                                matched_word = word
                                              
                                                break 
                                if matched_amount:
                                    break
                        if matched_amount:
                        
                            matched_values[word] = {
                                'value': matched_amount,
                                'page_number': matched_page_number,
                                'word': matched_word
                            }

                    #Create a new PDF using PyPDF2
                    pdf_writer = PdfFileWriter()

                    #Copy the existing pages to the new PDF
                    for page_num in range(pdf_reader.getNumPages()):
                        current_page = pdf_reader.getPage(page_num)
                        pdf_writer.addPage(current_page)
                        
                        # zoom_factor = 1
                        
                        # # Get the original page size
                        # page_width, page_height = current_page.mediaBox.upperRight

                        # # Create a new page with adjusted size
                        # new_page = pdf_writer.addBlankPage(width=page_width * zoom_factor, height=page_height * zoom_factor)
                        
                        # # Scale and translate content to fit new page size
                        # new_page.mergeTranslatedPage(current_page, 0 , 0)
                        # new_page.compressContentStreams()
                        
                    for word in words_to_find:
                        if  word in matched_values and matched_values[word]['value'] != '0.00':         
                            #To find or find the word and get dimension of the word using fitz module
                            doc = fitz.open(pdf_path)
                            page = doc[matched_values[word]['page_number']]
                            #This for pdfwriter.addlink to place the link to matched word page
                            page_no_to_palce_link = matched_values[word]['page_number']

                            # Search for a specific word and retrieve its coordinates
                            keyword_matched_amount = matched_values[word]['value']
                            matched_word_string = matched_values[word]['word']

                          

                            if matched_word_string == 'Benefits accrued as a result of operations before income tax':
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'Benefits accrued as a result of operations'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                

                                            )
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)

                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[-1]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.add_link(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                [1,1,1],
                                                                '/XYZ',
                                                                0,0,1.25 
                                                                
                                                            )
                                                            break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(matched_word_string)
                                            pass    

                            elif matched_word_string == 'Income Tax Expense' or  matched_word_string == 'Income Tax Refundable':
                                
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'CURRENT TAX OR REFUND'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                
                                            )
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[-1]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.add_link(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                [1,1,1],
                                                                '/XYZ',
                                                                0,0,1.25
                                                                 
                                                                
                                                            )
                                                            break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(matched_word_string)
                                            pass    

                            elif matched_word_string == 'Trust Distributions' or matched_word_string == 'Dividends Received':
                                            
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            if matched_word_string == 'Trust Distributions':
                                                value_to_find = 'Distribution Reconciliation Report'
                                            else:
                                                value_to_find = 'Dividend Reconciliation Report'

                                            subsequent_word = 'TOTAL'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                
                                            )
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[0]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.add_link(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                [1,1,1],
                                                                '/XYZ',
                                                                0,0,1.25
                                                                 
                                                                
                                                            )
                                                            break
                                        except:
                                            Link_notGenerated.append(matched_word_string)
                                            pass 
                            
                            elif matched_word_string == 'Income Tax Payable':
                                word_instances = page.search_for(keyword_matched_amount)
                            
                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'AMOUNT DUE OR REFUNDABLE'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                
                                            )
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)

                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                 
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)
                                                  
                                                    if data:

                                                        matched_data = data[-1]
                                                       
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.add_link(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                [1,1,1],
                                                                '/XYZ',
                                                                0,0,1.25
                                                                 
                                                                
                                                            )
                                                            break
                                        except Exception as e:
                                    
                                            Link_notGenerated.append(matched_word_string)
                                            pass    
                            
                            elif matched_word_string in investment_summary_words:
                                word_instances = page.search_for(keyword_matched_amount)
                                
                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Investment Summary Report'
                                            second_word_Tofind = 'Market Value'
                                            subsequent_word = keyword_matched_amount
                                            

                                            matched_goto_pagenumber = None
                                            
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line: #1 value_to_find
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if second_word_Tofind in subsequent_line: #2 second_word_Tofind
                                                                for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                                    if subsequent_word in second_subsequent_line: #3 subsequent_word
                                                                        matched_goto_pagenumber = page_num
                                                                        break
                                                                    elif matched_goto_pagenumber is None:
                                                                        find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', second_subsequent_line)
                                                                        if find_decimal_value:
                                                                            # print(find_decimal_value)
                                                                            find_decimal_value = [value.replace(',','').strip() for value in find_decimal_value]
                                                                            for exact_decimal_value in find_decimal_value:
                                                                            
                                                                                if exact_decimal_value != 0.00:

                                                                                    convert_ToInt_subsequent_word = subsequent_word.replace(',','').strip()

                                                                                    round_value = round(float(convert_ToInt_subsequent_word))

                                                                                    decimal_value = float(exact_decimal_value)
                                                                                
                                                                                    if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                                        matched_goto_pagenumber = page_num
                                                                                        keyword_matched_amount = f"{decimal_value:,.2f}"
                                                                                    
                                                                                        break 
                                                                            
                                                if matched_goto_pagenumber is not None:
                                                    break
                                                                        
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                
                                            )

                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)
                                            
                                            # page = pdf.pages[matched_goto_pagenumber]
                                            
                                            # texts = page.extract_text().split('\n')
                                            # for text in texts:
                                            #     if subsequent_word in text:
                                            #         data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                            #         if data:

                                            #             matched_data = data[-1]
                                            doc = fitz.open(pdf_path)
                                            matched_page = doc[matched_goto_pagenumber]

                                            keyword = keyword_matched_amount
                                        
                                
                                            word_instances = matched_page.search_for(keyword)
                                            if len(word_instances) > 0:

                                                x, y, x1, y1 = word_instances[-1]

                                                page_height = matched_page.rect.height

                                                # Calculate the new y-coordinate for the bottom placement
                                                new_y = page_height - y1
                                                pdf_writer.add_link(
                                                    matched_goto_pagenumber,
                                                    page_no_to_palce_link,
                                                    RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                    [1,1,1],
                                                    '/XYZ',
                                                    0,0,1.25
                                                     
                                                    
                                                )
                                                # tentative_matched_amount = None
                                                break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(matched_word_string)
                                            pass    
                            
                            elif matched_word_string == 'ANZ - E*trade Cash Investment Account' or matched_word_string == 'CBA Direct Investment Account':
                                
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Cash transactions'
                                            subsequent_word = keyword_matched_amount

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.add_link(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                [1,1,1],
                                                 
                                                '/XYZ',
                                                0,0,1.25
                                                
                                            )
                                            
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)
                                            # page = pdf.pages[matched_goto_pagenumber]
                                            
                                            # texts = page.extract_text().split('\n')
                                            # for text in texts:
                                            #     if subsequent_word in text:
                                            #         data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                            #         if data:

                                            #             matched_data = data[-1]
                                            doc = fitz.open(pdf_path)
                                            matched_page = doc[matched_goto_pagenumber]

                                            keyword = keyword_matched_amount

                                            word_instances = matched_page.search_for(keyword)
                                            if len(word_instances) > 0:
                                                x,y,x1,y1 = word_instances[-1]
                                                page_height = matched_page.rect.height

                                                new_y = page_height - y1
                                                pdf_writer.add_link(
                                                    matched_goto_pagenumber,
                                                    page_no_to_palce_link,
                                                    RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                    [1,1,1],
                                                    '/XYZ',
                                                    0,0,1.25
                                                    
                                                )
                                                break
                                        except Exception as e:
                                    
                                            Link_notGenerated.append(matched_word_string)
                                            pass    
                            
                            else:
                                word_instances = page.search_for(keyword_matched_amount)
                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        
                                        #Get the height of the page
                                        try:
                                            page_height = page.rect.height

                                            #Calculate the new y-coordinates for the bottom placement
                                            new_y = page_height - y1

                                            #Add a link to the new PDF using the updated coordinates
                                            first_word_Tofind = 'General Ledger'

                                            if (word == 'Employer Contributions' or word == 'Personal Non Concessional' or word == 'Personal Concessional' or word == 'Other Contributions'):
                                                second_word_Tofind = 'Contributions'
                                            else:    
                                                second_word_Tofind = matched_word_string

                                            if word in word_based_credits:
                                                third_word_Tofind = 'Total Credits'
                                            else:
                                                third_word_Tofind = 'Total Debits'
                                            
                                            #To find the above mentioned data from the pdf 
                                            matched_goto_pagenumber = None
                                            for page_num , page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if first_word_Tofind in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if second_word_Tofind in subsequent_line:                                                          
                                                                for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                                    if third_word_Tofind in second_subsequent_line:
                                                                        # for end_line in lines[lines.index(subsequent_line) + 1:]:   
                                                                        #     if keyword_matched_amount in end_line:                                                           
                                                                        matched_goto_pagenumber = page_num
                                                                        break  # Exit the innermost loop once you've found the third word
                                                                    # elif third_word_Tofind not in lines:
                                                                    #     # If third word not found on the current page, continue searching on subsequent pages    
                                                                    #     i = page_num + 1
                                                                    #     while i < len(pdf.pages):
                                                                    #         next_page_lines = pdf.pages[i].extract_text().split('\n') 
                                                                    #         for next_line in next_page_lines:
                                                                    #             if third_word_Tofind in next_line:
                                                                    #                 matched_goto_pagenumber = i
                                                                    #                 break # Exit the loop once you've found the third word on a later page
                                                                    #         if matched_goto_pagenumber is not None:
                                                                    #             break # Exit the loop if you've found the third word on a later page
                                                                    #         i += 1 

                                                                if matched_goto_pagenumber is not None:
                                                                    break  # Exit the middle loop if you've found the third word
                                                        if matched_goto_pagenumber is not None:
                                                                break  # Exit the outer loop if you've found the third word

                                                if matched_goto_pagenumber is not None:
                                                    break  # Exit the loop if you've found the third word                   
                                                
                                            #to generate top link of the pdf
                                            pdf_writer.add_link(
                                                page_no_to_palce_link, #top page to palce link
                                                matched_goto_pagenumber, #Bottom page to place link
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]), #rectangel box for the matched data
                                                [1,1,1],
                                                '/XYZ',
                                                0,0,1.25
                                                 
                                                
                                            )
                                            
                                            gui_automation_pageNo.append(page_no_to_palce_link + 1)
                                            gui_automation_pageNo.append(matched_goto_pagenumber + 1)

                                            #Below code is used for generate bottom link of the pdf

                                            page = pdf.pages[matched_goto_pagenumber]

                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if third_word_Tofind in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)  
                                                    if data:
                                                        matched_data = data[0]
                                                        #this if for matching the same amount is equal to actual amount in total credits or debits
                                                        if matched_data ==  keyword_matched_amount:  
                                                        
                                                            doc = fitz.open(pdf_path)
                                                            matched_page = doc[matched_goto_pagenumber]
                                                            #
                                                            keyword = matched_data
                                                            word_instances = matched_page.search_for(keyword)
                                                            if len(word_instances) > 0:

                                                                x, y, x1, y1 = word_instances[-1]

                                                                page_height = matched_page.rect.height

                                                                #calculate the new y-coordinate for the bottom placement
                                                                new_y = page_height - y1
                                                                pdf_writer.add_link(
                                                                    matched_goto_pagenumber,
                                                                    page_no_to_palce_link,
                                                                    RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                    [1,1,1],
                                                                    '/XYZ',
                                                                     0,0,1.25
                                                                     
                                                                    
                                                                )
                                                                break

                                                       
                                                        #else if for the amount is not equal means it place the link in last index of matched amount 
                                                        else:
                                                        
                                                            doc = fitz.open(pdf_path)
                                                            matched_page = doc[matched_goto_pagenumber]

                                                            #
                                                            keyword = keyword_matched_amount
                                                        
                                                            word_instances = matched_page.search_for(keyword)

                                                            if not word_instances:
                                                                # for date in enumerate(pdf.pages):
                                                                try:
                                                                    lines = pdf.pages[matched_goto_pagenumber].extract_text().split('\n')
                                                                    for line in lines:
                                                                        find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                                                        if find_decimal_value:
                                                                            find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                                            for exact_decimal_value in find_decimal_value:
                                                                                if exact_decimal_value != 0.00:
                                                                                    convert_ToInt_subsequent_word = keyword_matched_amount.replace(',','').strip()
                                                                                    round_value = round(float(convert_ToInt_subsequent_word))
                                                                                    decimal_value = float(exact_decimal_value)

                                                                                    if (decimal_value <= round_value +1 and decimal_value >= round_value -1):
                                                                                        keyword = f"{decimal_value:,.2f}"
                                                                                        # print(keyword, 'general Ledger')
                                                                                        word_instances = matched_page.search_for(keyword)

                                                                                        break
                                                                except:
                                                                       pass



                                                            if len(word_instances) > 0:

                                                                x, y, x1, y1 = word_instances[-1]

                                                                page_height = matched_page.rect.height

                                                                #calculate the new y-coordinate for the bottom placement
                                                                new_y = page_height - y1
                                                                pdf_writer.add_link(
                                                                    matched_goto_pagenumber,
                                                                    page_no_to_palce_link,
                                                                    RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                                                                    [1,1,1],
                                                                    '/XYZ',
                                                                    0,0,1.25
                                                                     
                                                                    
                                                                )
                                                                break
                                            matched_word_string  = None                  
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(matched_word_string)
                                            pass           
                             
                    #Below code only for memeber statement - Start

                    #variable statement to find the sentence in the pdf from start account to end account variable in between member *amount
                    start_account = "Liability for accrued benefits allocated to members' accounts"
                    end_account = "Total Liability for accrued benefits allocated to members' accounts"

                    #To store the amount and page no. as a dictionary data structure
                    matched_client_values = {}

                    #Gather the inbetween amount and page no.
                    for page_num, page in enumerate(pdf.pages):
                        if page_num <=3:
                            lines = page.extract_text().split('\n')
                            for line in lines:
                                if start_account in line:
                                    # If start_account is  matched, search for end_account in subsequent lines
                                    matched_page_number = []
                                    data_lines = []
                                    for subsequent_line in lines[lines.index(line) + 1:]:
                                        # values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))', subsequent_line)
                                        values = re.findall(r' \b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))(?![0-9]{2}/[0-9]{2}/[0-9]{4})(?![0-9]{2}:[0-9]{2}:[0-9]{2})', subsequent_line)
                                    
                                        if values: 
                                            compare_val = values[0].replace(',', '').strip()
                                            if float(compare_val) > 300: 
                                                data_lines.append(values[0])
                                                matched_page_number.append(page_num)
                                        if end_account in subsequent_line:
                                            #If end_account is found, extract the data from the collected lines
                                            matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                            break #Exit the loop if end_account is found
                                        else:
                                            nextPage = page_num + 1
                                            lines = pdf.pages[nextPage].extract_text().split('\n')
                                            for line in lines:
                                                # values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))', line)
                                                values = re.findall(r' \b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))(?![0-9]{2}/[0-9]{2}/[0-9]{4})(?![0-9]{2}:[0-9]{2}:[0-9]{2})', line)
                                            
                                                if values:
                                                    compare_val = values[0].replace(',', '').strip() 
                                                    if float(compare_val) > 300:
                                                        data_lines.append(values[0])
                                                        matched_page_number.append(nextPage)
                                                if end_account in line:
                                                    matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                                    break
                                    break #Exit the loop if start_account is found
                                
                    # print all matched data and their respective page numbers - for client member' account benefits

                    #find out the above matched value with below specified member_statementSring value  and place the top link
                    for start, (data, client_name_page) in matched_client_values.items():
                        
                        for line_data, client_pageNo in zip(data, client_name_page):
                
                            doc = fitz.open(pdf_path)
                            matched_client_page = doc[client_pageNo]
                            client_nameTo_placeLink = client_pageNo
                        
                            client_data_no = line_data
                            member_statementString = 'Members Statement'
                            matched_memberPageNo = None

                            for page_num, page in enumerate(pdf.pages):
                                lines = page.extract_text().split('\n')
                                for line in lines:
                                    if member_statementString in line:
                                        for member_subsequent_line in lines[lines.index(line) + 1:]:
                                            if line_data in member_subsequent_line:
                                                matched_memberPageNo = page_num
                                                break
                                            elif matched_memberPageNo is None:
                                                find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', member_subsequent_line)
                                                if find_decimal_value:
                                                    find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                    for exact_decimal_value in find_decimal_value:
                                                        if exact_decimal_value != 0.00:
                                                            convert_ToInt_subsequent_word = line_data.replace(',', '').strip()
                                                            round_value = round(float(convert_ToInt_subsequent_word))
                                                            decimal_value = float(exact_decimal_value)

                                                            if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                matched_memberPageNo = page_num
                                                                client_data_no_decimal = f"{decimal_value:,.2f}"
                                                            
                                                                break
                                                            

                                if matched_memberPageNo is None:
                                    i = page_num + 1
                                    for date in enumerate(pdf.pages):
                                        try:
                                            next_line = pdf.pages[i].extract_text().split('\n')
                                            for end_line in next_line:
                                                if member_statementString in end_line:
                                                    for subsequent_line in next_line[next_line.index(end_line) + 1:]:
                                                        if line_data in subsequent_line:
                                                            matched_memberPageNo = i
                                                            break
                                                        elif matched_memberPageNo is None:
                                                            find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', member_subsequent_line)
                                                            if find_decimal_value:
                                                                find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                                for exact_decimal_value in find_decimal_value:
                                                                    if exact_decimal_value != 0.00:
                                                                        convert_ToInt_subsequent_word = line_data.replace(',', '').strip()
                                                                        round_value = round(float(convert_ToInt_subsequent_word))
                                                                        decimal_value = float(exact_decimal_value)

                                                                        if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                            matched_memberPageNo = i
                                                                            client_data_no_decimal = f"{decimal_value:,.2f}"

                                                                            break

                                            if matched_memberPageNo is None:
                                                i += 1
                                            else:
                                                break
                                        except:
                                           
                                            pass

                                        break

                            word_instance = matched_client_page.search_for(client_data_no)
                
                            if len(word_instance) > 0:
                                for instance in word_instance:
                                    x,y, x1,y1 = instance
                                    try:
                                        page_height = matched_client_page.rect.height

                                        new_y = page_height - y1
                                        
                                        pdf_writer.add_link(
                                            client_nameTo_placeLink,
                                            matched_memberPageNo,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            [1,1,1],
                                            '/XYZ',
                                            0,0,1.25
                                             
                                            
         
                                        )
                                        gui_automation_pageNo.append(client_nameTo_placeLink + 1)
                                        gui_automation_pageNo.append(matched_memberPageNo + 1)
                                    except Exception as e:
                                        # Link_notGenerated.append()
                                        pass
                            
                            #This for below matched amount to set bottom to top link in the pdf
                            doc = fitz.open(pdf_path)
                            if matched_memberPageNo is not None:
                            
                                matched_client_page_up = doc[matched_memberPageNo]
                                word_instance = matched_client_page_up.search_for(client_data_no)
                                if not word_instance:
                                    client_data_no_decimal = client_data_no_decimal.replace(',', '').strip()
                                    convert_to_int = int(float(client_data_no_decimal))
                                  
                                    client_data_no = f"{convert_to_int:,}"
                                  
                                word_instance = matched_client_page_up.search_for(client_data_no)
                               
                                if len(word_instance) > 0:
                                    
                                    try:
                                        x,y, x1,y1 = word_instance[-2]
                                        page_height = matched_client_page_up.rect.height

                                        new_y = page_height - y1
                                        
                                       
                                        pdf_writer.add_link(
                                            matched_memberPageNo,
                                            client_nameTo_placeLink,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            [1,1,1],
                                            '/XYZ',
                                            0,0,1.25
                                            
                                        )
                                    except Exception as e:
                                        # Link_notGenerated.append(word)
                                        pass

                                else:
                                    print('Word not found in the PDF')

                    #End memeber statement 

                    investment_code = []
                    investment_code_1 = []

                    start_investment_code_value = 'Investment Summary Report'

                    investment_words = ['Shares in Listed Companies (Australian)']


                    for page_num, page in enumerate(pdf.pages):
                        
                        lines = page.extract_text().split('\n')

                        if start_investment_code_value in lines:
                        
                            for value in investment_words:
                                for line in lines:
                    
                                    if value in line:
                    
                                        for subsequent_line in lines[lines.index(line) + 1:]:
                
                                            data = subsequent_line[0]
                                            data_1 = subsequent_line
                                            print(data, data_1)

                                    # if data:
                                    #     investment_code.append(data)
                                    #     investment_code_1.append(data)
                                    #     print(investment_code, investment_code_1 , 'axx code')







                    # #Below Sublinking code
                    # investmentBank_word_list = open('investment_code.txt', 'r')

                    # investment_data = investmentBank_word_list.read()

                    # investment_to_find = investment_data.split('\n')

                    # word_string1 = 'Investment Summary Report'
                    
                    

                    # for word_investment in investment_to_find: 
                    #     matched_investment_amount = None
                        

                    #     for page_num, page in enumerate(pdf.pages):

                    #         lines = page.extract_text().split('\n')
                    #         for line_number, line in enumerate(lines):

                    #             if word_string1  in line:
                                   
                    #                 for subsequent_line_number, subsequent_line in enumerate(lines[line_number + 1:]):
                    #                     if word_investment in subsequent_line:

                    #                         amount_investment = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', subsequent_line)
                    #                         if amount_investment[0] != '0' and amount_investment[0] != '0.00':
                                                
                    #                             matched_investment_amount = amount_investment[0]

                    #                             matched_investment_page_number = page_num

                    #                             matched_investment_word = word_investment

                    #                             matched_line_number = line_number + subsequent_line_number + 1
                    #                             print(matched_line_number)

                    #                             break
                    #                 if matched_investment_amount:
                    #                     break
                    #         if matched_investment_amount:
                    #             break
                    #     if matched_investment_amount:

                    #         matched_investment_amount_values[word_investment] = {
                    #             'value': matched_investment_amount,
                    #             'page_number': matched_investment_page_number,
                    #             'word': matched_investment_word,
                    #             'line_no': matched_line_number
                    #         }
                    #         print('1',matched_investment_amount, matched_investment_page_number, matched_investment_word, matched_line_number)

                    # for word_investment in investment_to_find:
                       
                    #     if word_investment in matched_investment_amount_values and matched_investment_amount_values[word_investment]['value'] != '0.00':
                        
                    #         #To find or find the word and get dimension of the word using fitz module
                    #         doc = fitz.open(pdf_path)
                           
                    #         page = doc[matched_investment_amount_values[word_investment]['page_number']]
                            
                    #         #This for pdfwriter.addlink to place the link to matched word page
                    #         page_no_to_place_link = matched_investment_amount_values[word_investment]['page_number']
                          
                    #         # Search for a specific word and retrieve its coordinates
                    #         keyword_matched_amount = matched_investment_amount_values[word_investment]['value']
                          
                    #         matched_word_string = matched_investment_amount_values[word_investment]['word']

                    #         line_number = matched_investment_amount_values[word_investment]['line_no']    
                           
                    #         print('2',page_no_to_place_link, keyword_matched_amount, matched_word_string, line_number)
                            
                    #         if matched_word_string:
                                
                    #             words = page.get_text('words')

                    #             try:
                    #                 word_rect = None
                    #                 for word in words:
                                        
                    #                     if keyword_matched_amount in word[4]:
                    #                         #check if the word is in the target line number
                    #                         if word[5] == line_number:
                    #                             word_rect = fitz.Rect(word[:4])
                    #                             break

                    #                 x = word_rect[0]
                    #                 y = word_rect[1]
                    #                 x1 = word_rect[2]
                    #                 y1 = word_rect[3]
                    #                 print(x,y,x1,y1)

                    #                 page_height = page.rect.height
                    #                 new_y = page_height - y1

                    #                 wordString_one = 'Investor Centre'
                    #                 wordString_two = matched_word_string

                    #                 # wordString_two = matched_word_string.split(' ')[1:]
                    #                 # wordString_two = ' '.join(wordString_two).upper()
                    #                 keyword_amount = keyword_matched_amount.replace(',','').strip()
                    #                 keyword_amount = round(float(keyword_amount))

                    #                 keyword_amount_1 = keyword_matched_amount.split('.')[0]
                    #                 print(keyword_amount_1)
                    #                 wordString_three = 'Total ' + str(keyword_amount) 
                    #                 print(wordString_three)
                    #                 investment_goto_pagenumber = None
                    #                 for page_num, page in enumerate(pdf.pages):
                    #                     lines = page.extract_text().split('\n')
                    #                     for line in lines:
                    #                         if wordString_one in line:
                                                
                    #                             for subsequent_line in lines[lines.index(line) + 1:]:
                                                    
                    #                                 if wordString_two in subsequent_line:
                                                        
                    #                                     for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                            
                    #                                         if wordString_three in second_subsequent_line:
                    #                                             print('threee')
                    #                                             investment_goto_pagenumber = page_num
                    #                                             print(investment_goto_pagenumber)
                    #                                             break
                    #                                         elif keyword_amount_1 in second_subsequent_line:
                    #                                             investment_goto_pagenumber = page_num
                    #                                             keyword_amount = keyword_amount_1
                    #                                             print(keyword_amount)
                    #                                             break
                    #                                     if investment_goto_pagenumber is not None:
                    #                                         break
                    #                             if investment_goto_pagenumber is not None:
                    #                                 break
                    #                     if investment_goto_pagenumber is not None:
                    #                         break
                                    
                    #                 pdf_writer.add_link(
                    #                     page_no_to_place_link,
                    #                     investment_goto_pagenumber,
                    #                     RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                    #                     [1,1,1], 
                    #                     "/XYZ",
                    #                     0,0,1.25
                                        

                    #                 )
                    #                 gui_automation_pageNo.append(page_no_to_place_link + 1)
                    #                 gui_automation_pageNo.append(investment_goto_pagenumber + 1)
                                    
                    #                 #Bottom Link
                    #                 page = pdf.pages[investment_goto_pagenumber]

                    #                 # texts = page.extract_text().split('\n')
                    #                 # for text in texts:
                    #                 #     if wordString_three in text:
                    #                 #         data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                    #                         # if data:
                    #                         #     print(data[0])
                    #                 matched_data = str(keyword_amount)
                    #                 print(matched_data)
                    #                 print('1',matched_data, type(matched_data))
                    #                 doc = fitz.open(pdf_path)
                    #                 matched_page = doc[investment_goto_pagenumber]

                    #                 keyword = matched_data

                    #                 word_instances = matched_page.search_for(keyword)

                    #                 find_investor_instances = matched_page.search_for('Investor Centre | Link Market Services')
                                    
                    #                 if len(word_instances) > 0:
                    #                     if len(find_investor_instances) == 0:
                    #                         x,y,x1,y1 = word_instances[0]
                    #                     else:
                    #                         x,y,x1,y1 = word_instances[-1]


                    #                     print(word_instances)
                    #                     page_height = matched_page.rect.height

                    #                     new_y = page_height - y1
                    #                     pdf_writer.addLink(
                    #                         investment_goto_pagenumber,
                    #                         page_no_to_place_link,
                    #                         RectangleObject([x-20, new_y, x1+20, (new_y + (y1 - y))]),
                    #                         [1,1,1],
                    #                         '/XYZ',
                    #                         0,0,1.25
                                            
                    #                     )
                    #                 # break         
                                        
                
                    #             except Exception as e:
                    #                 print(e)
                    #                 Link_notGenerated.append(matched_word_string)
                    #                 pass 

                                
                    # # save the modified PDF and error log text file
                    # filename = os.path.splitext(pdf_file)[0] #Extract the filename without extension
                    # output_file = path.join(out_path_folder, f'Automated_link_{filename}.pdf')

                    # # #for error log code
                    # output_file_error_log = path.join(out_path_folder, f'Error_log_File_{filename}.txt')
                    # with open(output_file_error_log, 'w') as file:
                    #     file.write("Filename:  "+filename+ ""+'\n')
                    #     file.write('\n')
                    #     file.write("_______________ Failing to generate link for this below Word's _______________"+'\n')
                    #     file.write('\n')
                    #     for item in list(set(Link_notGenerated)):
                    #         if item is not None:
                    #             file.write(item + '\n')
                    #             file.write('\n')
                    # print(f'Data has been written to {output_file_error_log}')


                    # #gui Automation
      
                    # output_file_pageNumber = (f'pageNumber.txt')
                    # with open(output_file_pageNumber, 'w') as file:
                    #     for item in list(set(gui_automation_pageNo)):
                    #         if item is not None:
                    #             file.write(str(item)+ '\n')
                                
                    # print(f'Data has been written to {output_file_pageNumber}')

                    # #for pdf code
                    # with open(output_file, 'wb') as link_pdf:
                    #     pdf_writer.write(link_pdf)
                    # print(f'Link added to the PDF: {output_file}')      

                    
                    # # time.sleep(8)   
                    
                    # # # Open Adobe Acrobat (Assuming it is already installed)
                    # # pyautogui.hotkey('win', 's')  # Open Windows Search
                    # # pyautogui.write('Adobe Acrobat')  # Type Adobe Acrobat
                    # # pyautogui.press('enter')  # Press Enter to open Acrobat

                    # # # Wait for Acrobat to open
                    # # time.sleep(3)
                    # # # print(output_file)
                    
                    # # # Open the PDF file
                    # # pyautogui.hotkey('ctrl', 'o')
                    # # time.sleep(5)
                    # # pyautogui.write(output_file)
                    # # pyautogui.press('enter')

                    # # # Wait for the PDF to open
                    # # time.sleep(3) 

                    # # current_window = pyautogui.getActiveWindowTitle()
                    # # if "Adobe Acrobat" in current_window:

                    # #     # # Get the total number of pages in the PDF using PyMuPDF
                    # #     # num_pages = get_total_pages(file_path)

                    # #     text_file = open('pageNumber.txt', 'r')
                    # #     text_file_data = text_file.read()

                    # #     page_Num_pdf = text_file_data.split('\n')

                    # #     # Iterate through each page and perform the actions
                    # #     for Number_data in page_Num_pdf:
                    # #         # Go to the specific page
                            
                    # #         pyautogui.hotkey('ctrl', 'shift', 'n')
                    # #         pyautogui.write(Number_data)
                    # #         pyautogui.press('enter')
                    # #         time.sleep(1)  # Add a delay to allow the page to load

                            
                    # #         pyautogui.press('l')
                    # #         pyautogui.hotkey('ctrl', 'a')

                    # #         # Right-click to open the context menu for link properties
                    # #         pyautogui.press('enter')
                        
                    # #         pyautogui.keyDown('ctrl')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.keyUp('ctrl')

                    # #         time.sleep(1)
                    # #         # pyautogui.press('tab')
                    # #         # pyautogui.press('tab')
                    # #         # pyautogui.press('tab')
                    # #         pyautogui.hotkey('alt' , 'e')
                    # #         # pyautogui.press('enter')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('i')
                    # #         time.sleep(1)
                    # #         pyautogui.press('enter')


                    # #         # time.sleep(2)

                    # #         pyautogui.keyDown('ctrl')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.keyUp('ctrl')
                    # #         time.sleep(1)

                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('enter')
                    # #         time.sleep(1)

                    # #         pyautogui.hotkey('alt', 'down')
                    # #         pyautogui.hotkey('alt', 'down')
                    # #         time.sleep(1)

                    # #         pyautogui.hotkey('alt', 'right')
                    # #         pyautogui.hotkey('alt', 'right')
                    # #         pyautogui.hotkey('alt', 'right')
                    # #         pyautogui.hotkey('alt', 'right')
                    # #         pyautogui.hotkey('alt', 'right')
                        
                    # #         time.sleep(1)
        

                    # #         pyautogui.press('enter')
                    # #         pyautogui.press('tab')
                    # #         pyautogui.press('enter')
                        
                    # #         pyautogui.hotkey('ctrl', 'down')


                    # #         # Save changes and close Adobe Acrobat
                    # #         pyautogui.hotkey('ctrl', 's')


                    # #     # Close Adobe Acrobat
                    # #     pyautogui.hotkey('alt', 'f4')

                    # # else:
                    # #     exit()
                    
                       
             
    else:
        print('Password is Incorrect!')
        pdf_automation()

    

pdf_automation()








