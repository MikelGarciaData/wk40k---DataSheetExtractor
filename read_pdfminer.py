from io import StringIO
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

"""
output_string = StringIO()
with open('tyranids_sample.pdf', 'rb') as in_file:
    print(in_file   )
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

print(output_string.getvalue())
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd

path = 'tyranids_sample.pdf'

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams )
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 18
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def get_datasheet_numbers(path):
    data = {}
    datasheets = convert_pdf_to_txt(path).split("")
    even_pages = datasheets[::2]
    even_pages.pop(-1)

    # Caracteristicas de unidad
    name_regex = re.compile('[A-Z _-]+')
    mov_regex = re.compile('M\\n\\n\d+"')
    tough_regex = re.compile('T\\n\\n\d+')
    save_regex = re.compile('SV\\n\\n\d\+')
    wound_regex = re.compile('W\\n\\n\d+')
    lead_regex = re.compile('LD\\n\\n\d\+')
    objctrl_regex = re.compile('OC\\n\\n\d')

    # Para un bucle
    for page in even_pages:
        data[name_regex.search(page).group()] = {
            'M': int(re.findall('\d+', mov_regex.search(page).group())[0]),
            'T': int(re.findall('\d+', tough_regex.search(page).group())[0]),
            'SV': int(re.findall('\d+', save_regex.search(page).group())[0]),
            'W': int(re.findall('\d+', wound_regex.search(page).group())[0]),
            'LD': int(re.findall('\d+', lead_regex.search(page).group())[0]),
            'OC': int(re.findall('\d+', objctrl_regex.search(page).group())[0])
        }

    return data






print("\n\n\nNueva funcion \n\n\n")
datasheets = convert_pdf_to_txt('tyranids_sample.pdf').split("")
print(datasheets)

df = pd.DataFrame(get_datasheet_numbers('tyranids_sample.pdf'))
# FUNCIONA


f = lambda x: x.split("\n\n")
ds_split = list(map(f, datasheets))
#ds_clean = [content for page in ds_split for content in page if content != ""] # desanida las listas

aux = []
for sheet in ds_split:
    aux.append(list(filter(lambda x: x != '', sheet)))

ds_clean = aux[:]

del aux
del ds_split
del datasheets

ds_clean.pop(-1)
lengths = list(map(lambda x: len(x), ds_clean))
par = [lengths[i] for i in range(len(lengths)) if i%2==0]
impar = [lengths[i] for i in range(len(lengths)) if i%2==1]
print(par, impar)

df = pd.DataFrame(ds_clean)
df.to_csv("data.csv", index=False)
