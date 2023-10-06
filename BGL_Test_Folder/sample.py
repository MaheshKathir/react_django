# Pypdf FileReader and Writer getting  Deprecated Error means install this  -> pip install 'PyPDF2<3.0'
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

#For password functionality
password_list  = ['!@#$%12345','1111']
password = input("Password: ")

if password in password_list:

    path_folder = 'C:\BGL_Test_Folder'

    for root, dirs, files in os.walk(path_folder):
        for pdf_file in files:
            pdf_path = path.join(root, pdf_file)

            #Defined Words to search into the PDF file
            

            # words_to_find = ['Unsettle Trade', 'Dividends Receivable', 'Distributions Receivable','PAYG Payable',
            #                  'Interest Received','Employer Contributions','Personal Non Concessional','Accountancy Fees','ATO Supervisory Levy',
            #                  'Investment Expenses','Changes in Market Values','Benefits accrued as a result of operations before income tax','Income Tax Expense','Dividends Received','Trust Distributions','Income Tax Payable',
            #                  'Shares in Listed Companies', 'Units in Listed Unit Trusts', 'Managed Investments', 'ANZ - E*trade Cash Investment Account', 'CBA Direct Investment Account']
            # words_to_find = ['Benefits accrued as a result of operations before income tax', 'Income Tax Expense','Changes in Market Values']
            
            words_to_find = [

                                'Managed Investments (Australian)',
                                'Managed Investments (Overseas)',
                                'Shares in Listed Companies (Australian)',
                                'Shares in Listed Companies (Overseas)',	
                                'Shares in Unlisted Private Companies (Overseas)',
                                'Units in Listed Unit Trusts (Australian)',
                                'Units in Unlisted Unit Trusts (Australian)',
                                'Plant and Equipment (at written down value) - Unitised',
                                'Real Estate Properties ( Australian - Residential)',
                                'Derivatives (Options, Hybrids, Future Contracts)',
                                'Other Assets',
                                'Loans to Associated Entities (In house loans) - Unitised',
                                'Stapled Securities',
                                'Mortgage Loans (Australian)',
                                'Fixed Interest Securities (Australian) - Unitised',
                                'Shares in Unlisted Private Companies (Australian)',
                                'Units in Listed Trusts (Australian)',
                               
                                'Sundry Debtors',
                                'ANZ - Premium Cash Account',
                                'ANZ - E*trade Cash Investment Account',
                                'SMA - Cash Account',
                                'Unsettle Trade',
                                'Dividends Receivable',
                                'CBA Direct Investment Account',
                                'Distributions Receivable',
                                'Income Tax Refundable',
                                'Deferred Tax Liability'

                                'Income Tax Payable',
                                'PAYG Payable',
                                'Sundry Creditors',
                                'Amounts owing to other persons',

                                'Trust Distributions',
                                'Dividends Received',
                                'Interest Received',
                                'Other Investment Income',
                                'Property Income',

                                'Employer Contributions',
                                'Personal Concessional',
                                'Personal Non Concessional',

                                'Forex Gain/Loss',
                                'Life Insurance Premiums',

                                'Accountancy Fees',
                                'ATO Supervisory Levy',
                                'Investment Expenses',
                                "Auditor's Remuneration",
                                'ASIC Fees',
                                'Forex Exchange Loss',
                                'Other Expenses',
                                'Other Expenses - Non deductible',
                                'Bank Charges',
                                'Depreciation',
                                'Interest Paid',
                                'Property Expenses - Agents Management Fees',
                                'Property Expenses - Council Rates',
                                'Property Expenses - Insurance Premium',
                                'Property Expenses - Repairs Maintenance',
                                'Property Expenses - Sundry Expenses',
                                'Property Expenses - Water Rates',
                                'Administration Costs',
                                'Investment Expenses',
                                'Unsettled Trades',

                                'Benefits accrued as a result of operations before income tax',
                                'Income Tax Expense',

                                'Pensions Paid',
                                'Benefits Paid/Transfers Out',
                                'Refund Excess Contributions',

                                'Changes in Market Values',

            ]


            word_based_credits = ['PAYG Payable','Employer Contributions','Interest Received','Employer Contributions','Personal Non Concessional',
                                  'Personal Concessional', 'Other Contributions','Other Investment Income','Property Income','Forex Gain/Loss']

            #For matched values has to store as dictionary data structure
            matched_values = {}
            Link_notGenerated = []
            #Open the PDF_file Using PyPDF2
            pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
            
            #For using pdfplumber to get the matched values like page number , matched values data
            with pdfplumber.open(pdf_path)  as pdf:
                for word in words_to_find:
                    matched_amount = None
                    matched_page_number = None
                    matched_word = None
                    for page_num, page in enumerate(pdf.pages):
                        if page_num <= 4:
                            lines = page.extract_text().split('\n')
                            for line in lines:
                                
                                if word in line:
                                    # data_values = re.findall(r'\((\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)', line)
                                    # print(data_values)
                                    data_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                    print(data_values)
                                    if data_values:
                                        if data_values[0] != 0:
                                            matched_amount = data_values[0]   # Extract the first value from the line
                                            print(word,matched_amount)
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

                
                for word in words_to_find:
                    if  word in matched_values and matched_values[word]['value'] != '0.00' :         
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
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                                        pdf_writer.addLink(
                                                            matched_goto_pagenumber,
                                                            page_no_to_palce_link,
                                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                            border=[1,1,1]
                                                        )
                                                        break
                                    except Exception as e:
                                        print('word:' , matched_word_string)
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
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
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                                        pdf_writer.addLink(
                                                            matched_goto_pagenumber,
                                                            page_no_to_palce_link,
                                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                            border=[1,1,1]
                                                        )
                                                        break
                                    except Exception as e:
                                        print('word:' , matched_word_string)
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
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
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                                        pdf_writer.addLink(
                                                            matched_goto_pagenumber,
                                                            page_no_to_palce_link,
                                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                            border=[1,1,1]
                                                        )
                                                        break
                                    except:
                                        Link_notGenerated.append(word)
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
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                                        pdf_writer.addLink(
                                                            matched_goto_pagenumber,
                                                            page_no_to_palce_link,
                                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                            border=[1,1,1]
                                                        )
                                                        break
                                    except Exception as e:
                                        print('word:' , matched_word_string)
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
                                        pass    
                        
                        elif (matched_word_string == 'Managed Investments (Australian)' or matched_word_string == 'Managed Investments (Overseas)' or
                              matched_word_string == 'Shares in Listed Companies (Australian)' or matched_word_string == 'Shares in Listed Companies (Overseas)' or	
                              matched_word_string == 'Shares in Unlisted Private Companies (Overseas)' or matched_word_string == 'Units in Listed Unit Trusts (Australian)' or
                              matched_word_string == 'Units in Unlisted Unit Trusts (Australian)' or matched_word_string == 'Plant and Equipment (at written down value) - Unitised' or
                              matched_word_string == 'Real Estate Properties ( Australian - Residential)' or matched_word_string == 'Derivatives (Options, Hybrids, Future Contracts)' or
                              matched_word_string == 'Other Assets' or matched_word_string == 'Loans to Associated Entities (In house loans) - Unitised' or
                              matched_word_string == 'Stapled Securities' or matched_word_string == 'Mortgage Loans (Australian)' or matched_word_string == 'Fixed Interest Securities (Australian) - Unitised' or
                              matched_word_string == 'Shares in Unlisted Private Companies (Australian)') or matched_word_string == 'Units in Listed Trusts (Australian)':
                            

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
                                                if value_to_find in line:
                                                    for subsequent_line in lines[lines.index(line) + 1:]:
                                                        if second_word_Tofind in subsequent_line:
                                                            for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                                if subsequent_word in second_subsequent_line:
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
                                                                    
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                        print(keyword_matched_amount)
                             
                                        word_instances = matched_page.search_for(keyword)
                                        if len(word_instances) > 0:

                                            x, y, x1, y1 = word_instances[-1]

                                            page_height = matched_page.rect.height

                                            # Calculate the new y-coordinate for the bottom placement
                                            new_y = page_height - y1
                                            pdf_writer.addLink(
                                                matched_goto_pagenumber,
                                                page_no_to_palce_link,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border=[1, 1, 1]
                                            )
                                            tentative_matched_amount = None
                                            break
                                    except Exception as e:
                                        print('word:' , matched_word_string)
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
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
                                        pdf_writer.addLink(
                                            page_no_to_palce_link,
                                            matched_goto_pagenumber,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border = [1,1,1]
                                        )
                                        
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
                                            pdf_writer.addLink(
                                                matched_goto_pagenumber,
                                                page_no_to_palce_link,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border=[1,1,1]
                                            )
                                            break
                                    except Exception as e:
                                        print('word:' , matched_word_string)
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
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
                                            second_word_Tofind = word

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
                                                                    matched_goto_pagenumber = page_num
                                                                    break
                                            #this if statement is used for next page to find the third word because it can't find means it goes to next page
                                            if matched_page_number is not None:
                                                i = page_num + 1
                                                for data in enumerate(pdf.pages):
                                                    next_line = pdf.pages[i].extract_text().split('\n')
                                                    for end_line in next_line:
                                                        if third_word_Tofind in end_line:
                                                            for end_line in next_line:
                                                                if keyword_matched_amount in end_line:
                                                                    matched_goto_pagenumber = i
                                                                    break
                                                    if matched_goto_pagenumber is None:
                                                        i += 1
                                                    else:
                                                        break
                                                break
                                                    
                                        #to generate top link of the pdf
                                        pdf_writer.addLink(
                                            page_no_to_palce_link, #top page to palce link
                                            matched_goto_pagenumber, #Bottom page to place link
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]), #rectangel box for the matched data
                                            border=[1, 1, 1]    #color of the rectangle box
                                        )

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
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1, 1, 1]
                                                            )
                                                            break
                                                    #else if for the amount is not equal means it place the link in last index of matched amount 
                                                    else:
                                                    
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        #
                                                        keyword = keyword_matched_amount
                                                    
                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:

                                                            x, y, x1, y1 = word_instances[-1]

                                                            page_height = matched_page.rect.height

                                                            #calculate the new y-coordinate for the bottom placement
                                                            new_y = page_height - y1
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1, 1, 1]
                                                            )
                                                            break

                                    except Exception as e:
                                        print(F"An error occurred: {str(e)}")
                                        Link_notGenerated.append(word)
                                        pass           
                                    
                            # else:
                            #     Link_notGenerated.append(word)
                #Below code only for memeber statement - Start

                #variable statement to find the sentence in the pdf from start account to end account variable in between member *amount
                start_account = "Liability for accrued benefits allocated to members' accounts"
                end_account = "Total Liability for accrued benefits allocated to members' accounts"

                #To store the amount and page no. as a dictionary data structure
                matched_client_values = {}

                #Gather the inbetween amount and page no.
                for page_num, page in enumerate(pdf.pages):
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

                                    pdf_writer.addLink(
                                        client_nameTo_placeLink,
                                        matched_memberPageNo,
                                        RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                        border=[1,1,1]
                                    )
                                except Exception as e:
                                    print('word:' , matched_word_string)
                                    print(F"An error occurred: {str(e)}")
                                    pass
                        
                        #This for below matched amount to set bottom to top link in the pdf
                        doc = fitz.open(pdf_path)
                        if matched_memberPageNo is not None:
                            matched_client_page_up = doc[matched_memberPageNo]
                            word_instance = matched_client_page_up.search_for(client_data_no)

                            if len(word_instance) > 0:
                                
                                try:
                                    x,y, x1,y1 = word_instance[-2]
                                    page_height = matched_client_page_up.rect.height

                                    new_y = page_height - y1

                                    pdf_writer.addLink(
                                        matched_memberPageNo,
                                        client_nameTo_placeLink,
                                        RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                        border=[1,1,1]
                                    )
                                except Exception as e:
                                    print('word:' , matched_word_string)
                                    print(F"An error occurred: {str(e)}")
                                    pass

                            else:
                                print('Word not found in the PDF')

                #End memeber statement 
                # Link_notGenerated.pop(-2)
                print(Link_notGenerated)
                
                # save the modified PDF
                filename = os.path.splitext(pdf_file)[0] #Extract the filename without extension
                output_file = path.join(path_folder, f'Automated_link_{filename}.pdf')

                # output_file_error_log = path.join(path_folder, f'Error_log_File_{filename}.txt')
                # with open(output_file_error_log, 'w') as file:
                #     file.write("_______________ Failing to generate link for this below Word's _______________"+'\n')
                #     file.write('\n')
                #     for item in Link_notGenerated:
                #         file.write(item + '\n')
                #         file.write('\n')
                # print(f'Data has been written to {output_file_error_log}')

                with open(output_file, 'wb') as link_pdf:
                    pdf_writer.write(link_pdf)
                print(f'Link added to the PDF: {output_file}')                           
                                                

else:
    print('Password is Incorrect!')

