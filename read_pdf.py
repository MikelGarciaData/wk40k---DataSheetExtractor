from PyPDF2 import PdfReader
import pandas as pd
import re
import json

pdf_file = open('tyranids_sample.pdf', 'rb')
print(pdf_file)

sample_file = 'tyranids_sample.pdf'

# Leer el pdf (True) o leer el JSON (False)
leer_pdf = False


def readPDF(filename, to_json):

    # Lectura del PDF
    pdf_file = open(filename, 'rb')
    read_pdf = PdfReader(pdf_file)
    #param
    num_pages = read_pdf._get_num_pages()
    content = []
    for i in range(num_pages):
        page = read_pdf.pages[i]
        page_content = page.extract_text()
        content.append(page_content)

    pdf_file.close()

    if to_json == True:
        with open(f'{filename[:-4]}_pdf_content.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

    return content


def extract_data(content):

    data = []
    name_regex = re.compile("[A-Z _'-]+")
    unit_stats_regex = re.compile('\d+" \d+ \d\+ \d+ \d\+ \d')

    # para el arma se necesita nombre, keywords y perfil
    nombre_regex = r"[A-Z][\w\s '-]+"
    weapkeys_regex = r"\[(\w+(?:-\w+)?(?:,\s*\w+(?:-\w+)?)*)\]"
    weapstats_regex = '(\d+"|Melee)\s(\d?D\d(\+\d)?|\d)\s(N\/A|\d\+)\s(\d)\s(-?\d)\s\d'
    #weap_regex = re.compile(fr'{nombre_regex} ({weapkeys_regex})? {weapstats_regex}')
    weap_regex = re.compile('(?:\\n)?((?!C\n)[A-Z][a-z\s\’-]+)\s*(\n)?(\[[^\]]*?\])?\s*(Melee|\d+")\s*(\d?D\d\+?\d?|\d+)\s*(N\/A|\d\+)\s*(\d+)\s*(-?\d)\s*(\d?D\d(\+\d)?|\d+)')
#                            '(?:\s+[A-Z]+)?\s*\\n([\w\s\'-]+)\s*\[[^\]]*?\]\s*(Melee|\d+")\s*(\d?D\d(\+\d)?|\d+)\s*(N\/A|\d\+)\s*(\d+)\s*(-?\d)\s*\d')
    # \\n([\w\s\'-]+)\s*(\[[^\]]*?\])?\s*(Melee|\d+")\s*
    #print(content)
    unit_pages = content[::2]
    wargear_pages = content[1::2]

    # extraer caracteristicas de la unidad
    for page, wargear in zip(unit_pages, wargear_pages):
        unit_data = unit_stats_regex.search(page).group().split(" ")

        data.append({ 'Name': name_regex.search(page).group(),
            'M': int(re.findall('\d+', unit_data[0])[0]),
            'T': int(re.findall('\d+', unit_data[1])[0]),
            'SV': int(re.findall('\d+', unit_data[2])[0]),
            'W': int(re.findall('\d+', unit_data[3])[0]),
            'LD': int(re.findall('\d+', unit_data[4])[0]),
            'OC': int(re.findall('\d+', unit_data[5])[0]),
                      # Mapeo las tuplas a tuplas filtradas sin ''. Utilizo directamente la lista extraida
            'WEAPONS': list(map(lambda tupla: tuple(filter(lambda x: x != '', tupla)), weap_regex.findall(page)))
        })
        print(name_regex.search(page).group(),':',list(map(lambda tupla: tuple(filter(lambda x: x != '', tupla)), weap_regex.findall(page))))

    df = pd.DataFrame.from_records(data)

    return df
    #df.to_csv("preprocessed_data.csv", index=False)

    #df = pd.DataFrame(content)
    #df.to_csv("raw_data.csv", index=False)


def insert_none(row):
    if '[' not in row[1]:
        return (row[0], 'None', *row[1:])
    else:
        return row


# Leemos el archivo de texto

if leer_pdf:
    pages_text = readPDF(filename=sample_file, to_json=True)
else:
    with open(f'{sample_file[:-4]}_pdf_content.json', encoding='utf-8') as f:
        pages_text = json.load(f)

#print(pages_text)

df = extract_data(pages_text)
df = df.explode('WEAPONS')
df['WEAPONS'] = df['WEAPONS'].apply(insert_none)
df[['weap_name', 'weap_kw', 'range', 'attack', 'skill', 'strength', 'arm_pen', 'damage']] = pd.DataFrame(df['WEAPONS'].tolist(), index=df.index)
df = df.drop('WEAPONS', axis=1)
print(df.to_string())

df.to_csv('clean_tyranid_sample.csv', index=False, quotechar="'")
