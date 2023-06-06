# #find the single number value
# print('***********************************************************************')

# import pdfplumber
# import re

# pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
# words_to_find = ['Government Co-Contributions', 'Foreign Income', 'Employer', 'Realised Capital Gains', 'Dividends']

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

# #finds the word's dimension in the pdf

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
# page_number = 1
# target_word = '14,830.63'

# word_dimensions = find_word_dimensions(pdf_path, page_number, target_word)
# if word_dimensions is not None:
#     print(f"Dimensions of '{target_word}': {word_dimensions}")
# else:
#     print(f"'{target_word}' not found on page {page_number}.")



# print('***********************************************************************')  


# #define pdf link
# from PyPDF2 import PdfFileWriter, PdfFileReader
# from PyPDF2.generic import RectangleObject
# from os import path

# pdf_writer = PdfFileWriter()
# pdf_writer.addLink(
#     1, # index of the page on which to place the link
#     3, # index of the page to which the link should go
#     rect=RectangleObject([65.58029197080292, 0, 69.48905109489051, 841]), # clickable area x1, y1, x2, y2 (starts bottom left corner)
#     # border
#     # fit 
# )

# with open(path.abspath('Clarkville Super Fund - Workpaper 2019.pdf'), 'wb') as link_pdf:
#     pdf_writer.write(link_pdf)
    
# print('***********************************************************************') 

#Date: 05/06/2023

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

# # finds the word's dimension in the pdf

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
# page_number = 6
# target_word = '75,413.38'

# word_dimensions = find_word_dimensions(pdf_path, page_number, target_word)
# if word_dimensions is not None:
#     print(f"Dimensions of '{target_word}': {word_dimensions}")
# else:
#     print(f"'{target_word}' not found on page {page_number}.")



# print('***********************************************************************')  


# #define pdf link
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path


import fitz

doc = fitz.open('testsample_30_pdf.pdf')
page = doc[5]  

for word_instance in page.search_for('37,347.59'):
    x, y, width, height = word_instance
    print(x, y, width, height) 

pdf_writer = PdfFileWriter()

pdf_reader = PdfFileReader(open('testsample_30_pdf.pdf', 'rb'))
number_of_pages = pdf_reader.getNumPages()

x1, y1, x2, y2 = pdf_reader.getPage(0).mediaBox
print(f'x1, x2: {x1, x2}\ny1, y2: {y1,y2}')


for page in range(number_of_pages):
    current_page = pdf_reader.getPage(page)
    pdf_writer.addPage(current_page)


pdf_writer.addLink(
    5, # index of the page on which to place the link
    3, # index of the page to which the link should go
    # rect=RectangleObject([518.8265380859375, 741.1832275390625, 478.4109802246094, 731.1285400390625]), # clickable area x1, y1, x2, y2 (starts bottom left corner)
    rect=RectangleObject([height, width, x, y]),
    border = [1, 1, 1],
)

# pdf_writer.add_uri(
#     page_number= 5,
#     2,
#     uri=2,
#     rect=(389.656005859375, 226.58053588867188 ,435.12554931640625 ,236.63522338867188)
# )

with open(path.abspath('testsample_32_pdf.pdf'), 'wb') as link_pdf:
    pdf_writer.write(link_pdf)
    
print('***********************************************************************') 

#06/06/2023 define link to the specific page
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path


pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'

# Open the PDF using fitz
doc = fitz.open(pdf_path)
page = doc[5]

# Get the text content of the page
text_content = page.get_text()

# Search for a specific word and retrieve its coordinates
keyword = '37,347.59'
word_instances = page.search_for(keyword)
if len(word_instances) > 0:
    x, y, x1, y1 = word_instances[0]
    print(f'Coordinates: x={x}, y={y}, width={x1-x}, height={y1-y}')
else:
    print('Word not found in the PDF.')
    exit()

# Get the height of the page
page_height = page.rect.height

# Calculate the new y-coordinate for the bottom placement
new_y = page_height - y1

# Create a new PDF using PyPDF2
pdf_writer = PdfFileWriter()
pdf_reader = PdfFileReader(open(pdf_path, 'rb'))

# Copy the existing pages to the new PDF
for page_num in range(pdf_reader.getNumPages()):
    current_page = pdf_reader.getPage(page_num)
    pdf_writer.addPage(current_page)

# Add a link to the new PDF using the updated coordinates
pdf_writer.addLink(
    5, 
    2,
    RectangleObject([x, new_y, x1, new_y + (y1 - y)]),
    border=[1, 1, 1]
)

# Save the modified PDF
output_file = path.abspath('testsample_50_pdf.pdf')
with open(output_file, 'wb') as link_pdf:
    pdf_writer.write(link_pdf)

print(f'Link added to the PDF: {output_file}')
