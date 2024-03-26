from io import StringIO
import re
import json


from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
with open('munitorum_field_manual.pdf', 'rb') as in_file:
    print(in_file   )
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

pdf_pages = output_string.getvalue().split("")

paragraphs = pdf_pages[28].split('\n\n')

print(pdf_pages[28])
# paragraphs[1].split('\n', 1) extraer nombre, datos a parte
# ... Extraer nombre, estructurar datos
paragraphs = paragraphs[1:-2]
# Extraer solo nombre con regex
unitnames = []
for string in paragraphs:
    unitnames.append(re.match("(.*?)\\n",string).group()[:-1])
    # te doy ideas: re.search("\\n(.*?) model") # cantidad
    #               re.search(".(.*?) pts") # puntos

print(unitnames)
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(unitnames, f, ensure_ascii=False, indent=4)