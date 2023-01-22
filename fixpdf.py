import re
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfWriter
import tkinter as tk
from tkinter import filedialog

# select input file
root = tk.Tk()
root.withdraw()

filepath: str = filedialog.askopenfilename(initialdir = "/", title = "Select PDF file", filetypes = (("PDF files", "*.pdf"),))
infile = Path(filepath)

# directory
working_directory = infile.parent

# files (input, change-list, output, extract)
#input_file_name = r'2022-02.pdf'
#infile = Path(working_directory, input_file_name)

changes_file_name = infile.stem + '_changes.txt'
changes_file = Path(working_directory, changes_file_name)

output_file_name = infile.stem + '_out' + infile.suffix
out_file = Path(working_directory, output_file_name)

extract_file_name = infile.stem + '_extract' + infile.suffix
extract_file = Path(working_directory, extract_file_name)

print(f'Input file : {infile.name}\n'
      f'Output file: {output_file_name}\n'
      f'Extract file: {extract_file_name}\n'
      f'Change List: {changes_file_name}')

delete_pages = []
rotate_pages = {}    # key: page number; value: angle (clockwise)
extract_pages = []

# pattern for PDF changes
# <page><operation><optional parameter>
# 2d - page 2, delete
# 7r90 - page 7, rotate, 90 deg
# 7r - page 7, rotate, no angle defaults to 180 deg
# 34e - page 34, extract
pattern = re.compile(r'(\d+)([rde])(\d*)', re.IGNORECASE)

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
                    # default rotation is 180 deg
                    if match.group(3) == '':
                        rotate_pages[int(match.group(1)) - 1] = 180
                    else:
                        rotate_pages[int(match.group(1)) - 1] = int(match.group(3))
                if match.group(2) == 'e':
                    extract_pages.append(int(match.group(1)) - 1)

# validation required!
# changes file must exist & have same name as input file with '_changes' suffix
# page must exist
# report invalid changes (e.g. d42 (should be 42d))
# rotate angle must be valid

# summary of changes
print(f'Summary of changes (Re-indexed to start ay Page 0:')
print(f'Delete pages: {delete_pages}')
print(f'Rotate pages: {rotate_pages}')
print(f'Extract pages: {extract_pages}')

# Make the changes
with open(infile, 'rb') as pdf_file:
    reader = PdfFileReader(pdf_file)
    doc_info = reader.getDocumentInfo()
    print(doc_info)
    number_of_pages = reader.getNumPages()
    print(f'Pages: {number_of_pages}')
    writer = PdfWriter()
    extract_writer = PdfWriter()

    # page numbers are 0 indexed
    for page_num in range(number_of_pages):
        if page_num in delete_pages:
            # skip delete pages
            continue
        elif page_num in extract_pages:
            # extract page
            pdf_page = reader.getPage(page_num)
            extract_writer.addPage(pdf_page)
        else:
            # not delete, not extract. Keep and rotate if needed
            pdf_page = reader.getPage(page_num)
            if page_num in rotate_pages:
                pdf_page.rotateClockwise(rotate_pages[page_num])
            writer.addPage(pdf_page)

    with open(out_file, 'wb') as pdf_out_file:
        writer.write(pdf_out_file)

    if len(extract_pages) > 0:
        with open(extract_file, 'wb') as pdf_out_file:
            extract_writer.write(pdf_out_file)

# next version
# choose input file with file dialog
# only create extract file if there are extract extract_pages

# default rotate to 180, e.g. 34r -> rotate page 34 by 180
# rotate clockwise or counterclockwise r90, r-90
# reverse order of all pages (for when a scan document is fed in wrong way around).
# replace/substitute pages (delete page and insert new page) e.g. s56f1p2 - page 56 substitute with file 1 page 2