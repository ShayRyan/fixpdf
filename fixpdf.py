import re
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfWriter
from PyPDF2 import PdfMerger

# directory
working_directory = r'Q:\Journal\2022'

# files (input, change-list, output)
input_file_name = r'2022-11.pdf'
infile = Path(working_directory, input_file_name)

changes_file_name = infile.stem + '_changes.txt'
changes_file = Path(working_directory, changes_file_name)

output_file_name = infile.stem + '_out' + infile.suffix
outfile = Path(working_directory, output_file_name)

print(f'Input file : {input_file_name}\n'
      f'Output file: {output_file_name}\n'
      f'Change List: {changes_file_name}')

delete_pages = []
rotate_pages = {}    # key: page number; value: angle (clockwise)

# pattern for PDF changes
pattern = re.compile(r'(\d+)([rd])(\d*)', re.IGNORECASE)

# Parse changes
# Human page numbering starts at 1
# Reindex page number changes to 0
with open(changes_file, 'rt') as f:
    lines = f.readlines()
    for line in lines:
        changes = line.strip().split(' ')
        for change in changes:
            match = re.search(pattern, change)
            if match:
                if match.group(2) == 'd':
                    delete_pages.append(int(match.group(1)) - 1)
                if match.group(2) == 'r':
                    rotate_pages[int(match.group(1)) - 1] = int(match.group(3))

# summary of changes
print(f'Summary of changes (Re-indexed to start ay Page 0:')
print(f'Delete pages: {delete_pages}')
print(f'Rotate pages: {rotate_pages}')


# Make the changes
with open(infile, 'rb') as pdf_file:
    reader = PdfFileReader(pdf_file)
    doc_info = reader.getDocumentInfo()
    print(doc_info)
    number_of_pages = reader.getNumPages()
    print(f'Pages: {number_of_pages}')
    writer = PdfWriter()


    # page numbers are 0 indexed
    for page_num in range(number_of_pages):
        if page_num not in delete_pages:
            pdf_page = reader.getPage(page_num)
            if page_num in rotate_pages:
                pdf_page.rotateClockwise(rotate_pages[page_num])
            writer.addPage(pdf_page)

    with open(outfile, 'wb') as pdf_out_file:
        writer.write(pdf_out_file)
