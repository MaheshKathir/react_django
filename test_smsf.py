import pdfplumber
import re

pdf_path = 'Clarkville Super Fund - Workpaper 2019.pdf'
words_to_find = ['Employer', 'Government Co-Contributions']

matched_values = {}
to_finded = []
matched_words = {}
matched_page_numbers = {}


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
            matched_values[word] = matched_value
            matched_page_numbers[word] = matched_page_number

        sentence_to_find = 'Transactions: '
        to_find = sentence_to_find + word
        to_finded.append(to_find)

    for sentence in to_finded:
        matched_word = None
        matched_p_number = None
        for page_num, page in enumerate(pdf.pages):
            lines = page.extract_text().split('\n')
            for line in lines:
                if sentence in line:
                    matched_word = sentence
                    matched_p_number = page_num
                    break
        if matched_word:
            matched_words[sentence] = matched_word
            matched_page_numbers[sentence] = matched_p_number

# Print the matched words and page numbers
for word, page_number in matched_page_numbers.items():
    print(f"Word: {word}  Page Number: {page_number}")
