# Pypdf FileReader and Writer getting  Deprecated Error means install this  -> pip install 'PyPDF2<3.0'
# To Resolve the fitz error , need to install this pymupdf                  -> pip install pymupdf


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
            # words_to_find =['Managed Investments','Shares in Listed Companies','Units in Listed Unit Trusts','Sundry Debtors','ANZ - Premium Cash Account',
            # 'ANZ - E*trade Cash Investment Account','SMA - Cash Account','Unsettle Trade','Dividends Receivable','CBA Direct Investment Account',
            # 'Distributions Receivable','Income Tax Payable','PAYG Payable','Trust Distributions','Dividends Received','Interest Received','Employer Contributions'
            # 'Personal Non Concessional','Accountancy Fees','ATO Supervisory Levy','Investment Expenses','Changes in Market Values','Benefits accrued as a result of operations before income tax' 
            # 'Income Tax Expense']

            words_to_find = ['Unsettle Trade', 'Dividends Receivable', 'Distributions Receivable','PAYG Payable',
                             'Interest Received','Employer Contributions','Personal Non Concessional','Accountancy Fees','ATO Supervisory Levy',
                             'Investment Expenses','Changes in Market Values','Benefits accrued as a result of operations before income tax','Income Tax Expense','Dividends Received','Trust Distributions','Income Tax Payable',
                             'Shares in Listed Companies', 'Units in Listed Unit Trusts', 'Managed Investments', 'ANZ - E*trade Cash Investment Account', 'CBA Direct Investment Account']

            word_based_credits = ['PAYG Payable','Employer Contributions','Interest Received','Employer Contributions','Personal Non Concessional']

            #For matched values has to store as dictionary data structure
            matched_values = {}

            #Open the PDF_file Using PyPDF2
            pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
            
            #For using pdfplumber to get the matched values like page number , matched values data
            with pdfplumber.open(pdf_path)  as pdf:
                for word in words_to_find:
                    matched_amount = None
                    matched_page_number = None
                    matched_word = None
                    for page_num, page in enumerate(pdf.pages):
                        lines = page.extract_text().split('\n')
                        for line in lines:
                            if word in line:
                                data_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                if data_values:
                                    if data_values[0] != 0:
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

                
                for word in words_to_find:
                    if  word in matched_values:         
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
                                    except:
                                        pass    

                        elif matched_word_string == 'Income Tax Expense':
                            
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
                                    except:
                                        pass    

                        elif matched_word_string == 'Trust Distributions' or 'Dividends Received':
                                           
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
                                    except:
                                        pass    
                        
                        elif matched_word_string == 'Shares in Listed Companies' or 'Units in Listed Unit Trusts' or 'Managed Investments':
                            word_instances = page.search_for(keyword_matched_amount)

                            if len(word_instances) > 0:
                                for instance in word_instances:
                                    x, y, x1, y1 = instance
                                    try:
                                        page_height = page.rect.height
                                        new_y = page_height - y1

                                        value_to_find = 'Investment Summary Report'
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
                                        #             doc = fitz.open(pdf_path)
                                        #             matched_page = doc[matched_goto_pagenumber]

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
                                    except:
                                        pass    
                        
                        elif matched_word_string == 'ANZ - E*trade Cash Investment Account' or 'CBA Direct Investment Account':
                            
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
                                    except:
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

                                        second_word_Tofind = word

                                        if word in word_based_credits:
                                            third_word_Tofind = 'Total Credits'
                                        else:
                                            third_word_Tofind = 'Total Debits'
                                        
                                        #To find the above mentioned data from the pdf 
                                        link_goto_pagenumber = None
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
                                            if matched_page_number is None:
                                                i = page_num + 1
                                                for data in enumerate(pdf.pages):
                                                    next_line = pdf.pages[i].extract_text().split('\n')
                                                    for end_line in next_line:
                                                        if third_word_Tofind in end_line:
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

                                    except:
                                        pass           

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
                                values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', subsequent_line)
                                if values:
                                    data_lines.append(values[0])
                                    matched_page_number.append(page_num)
                                if end_account in subsequent_line:
                                    #If end_account is found, extract the data from the collected lines
                                    matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                    print(matched_client_values[start_account])
                                    break #Exit the loop if end_account is found
                                else:
                                    nextPage = page_num + 1
                                    lines = pdf.pages[nextPage].extract_text().split('\n')
                                    for line in lines:
                                        if end_account in line:
                                            matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                            print('else:',matched_client_values[start_account])
                                            break
                            break #Exit the loop if start_account is found
                        
                # print all matched data and their respective page numbers - for client member' account benefits

                #find out the above matched value with below specified member_statementSring value  and place the top link
                for start, (data, client_name_page) in matched_client_values.items():
                    
                    for line_data, client_pageNo in zip(data, client_name_page):
                        print(line_data)
                        print("client_pageNO:",client_pageNo)
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
                                except:
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
                                except:
                                    pass

                            else:
                                print('Word not found in the PDF')

                #End memeber statement 

                # save the modified PDF
                filename = os.path.splitext(pdf_file)[0] #Extract the filename without extension
                output_file = path.join(path_folder, f'Automated_link_{filename}.pdf')
                with open(output_file, 'wb') as link_pdf:
                    pdf_writer.write(link_pdf)
                print(f'Link added to the PDF: {output_file}')                           
                                                


else:
    print('Password is Incorrect!')

