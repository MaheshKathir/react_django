# #find the single number value
# print('***********************************************************************')

# import pdfplumber
# import re

# pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
# words_to_find = ['Vested Benefits at beginning of period']

# matched_values = {}

# with pdfplumber.open(pdf_path) as pdf:
#     for word in words_to_find:
#         matched_value = None
#         for page_num, page in enumerate(pdf.pages):
#             lines = page.extract_text().split('\n')
#             for line in lines:
#                 if word in line:
#                     values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
#                     if values:
#                         matched_value = values[0]  # Extract the first value from the line
#                         break
#             if matched_value:
#                 break

#         if matched_value:
#             matched_values[word] = matched_value

#     for word in words_to_find:
#         if word in matched_values:
#             print(f"Matching value for '{word}':")
#             print(matched_values[word])
#         else:
#             print(f"No matching value found for '{word}'.")
#         print()
        

# print('***********************************************************************')  

#finds the word's dimension in the pdf

# from PyPDF2 import PdfFileReader
# from decimal import Decimal

# def find_word_dimensions(pdf_path, page_number, target_word):
#     pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
#     page = pdf_reader.getPage(page_number)

#     # Get page dimensions
#     x1, y1, x2, y2 = page.mediaBox

#     # Extract the page text
#     page_text = page.extract_text()

#     # Find the position of the target word in the text
#     word_start_index = page_text.find(target_word)
#     word_end_index = word_start_index + len(target_word)

#     # Calculate the word coordinates
#     word_x1 = x1 + (float(word_start_index) / len(page_text)) * (x2 - x1)
#     word_y1 = y1
#     word_x2 = x1 + (float(word_end_index) / len(page_text)) * (x2 - x1)
#     word_y2 = y2

#     return word_x1, word_y1, word_x2, word_y2

# # Usage example
# pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
# page_number = 5
# target_word = '988,130.47'

# word_dimensions = find_word_dimensions(pdf_path, page_number, target_word)
# if word_dimensions is not None:
#     print(f"Dimensions of '{target_word}': {word_dimensions}")
# else:
#     print(f"'{target_word}' not found on page {page_number}.")



print('***********************************************************************')  


#define pdf link
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path


import fitz

doc = fitz.open('Clarkville Super Fund - Workpaper 2019.pdf')
page = doc[5]  

for word_instance in page.search_for('988,130.47'):
    x, y, width, height = word_instance
    print(x, y, width, height) 

pdf_writer = PdfFileWriter()

pdf_reader = PdfFileReader(open('Clarkville Super Fund - Workpaper 2019.pdf', 'rb'))
number_of_pages = pdf_reader.getNumPages()

for page in range(number_of_pages):
    current_page = pdf_reader.getPage(page)
    pdf_writer.addPage(current_page)

pdf_writer.addLink(
    5, # index of the page on which to place the link
    3, # index of the page to which the link should go
    rect=RectangleObject([388.3059997558594, 433.77557373046875, 430.4195556640625, 440.4742431640625]), # clickable area x1, y1, x2, y2 (starts bottom left corner)
    # border
    # fit 
)

with open(path.abspath('saaaf.pdf'), 'wb') as link_pdf:
    pdf_writer.write(link_pdf)
    
print('***********************************************************************') 

