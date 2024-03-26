import re

# extraer de pdfminer

# regex for Movement
regex = '(M\\n\\n)\d"'

# regex for Toughtness
regex = '(T\\n\\n)\d'

# regex for Saving
regex = '(SV\\n\\n)\d\+'

# regex for Wounds
regex = '(W\\n\\n)\d+'

# regex for Leadership
regex = '(LD\\n\\n)\d\+'

# regex for Objective Control
regex = '(OC\\n\\n)\d'

# regex for CORE rules
regex = 'CORE: [a-zA-Z]*(\s+[a-zA-Z0-9]+)*(,[a-zA-Z]*(\s+[a-zA-Z0-9]+))*'

# regex for FACTION, use with findall
regex = 'FACTION: [^,.]+,[^,.]+\\n*\\n'

# regex for KEYWORDS
regex = '\\nKEYWORDS: (?:\w+\s*,\s*)*\w+(?:\s*,\s*\w+)*'

# regex for FACTION KEYWORDS


# regex for weaponry, use pypdf2
#regex = '(\w+-\w+\s|\w+\s)+(\[(\w+\s*)+,*(\s\w+)*,*(\s\w+)*,*(\s\w-\w+)*\])'

# regex for weapon keywords
nombre_regex  = r"[\w'-]+"
weapkeys_regex = regex = r"\[(\w+(?:-\w+)?(?:,\s*\w+(?:-\w+)?)*)\]"

# regex for weap profile
weapstats_regex = '(\d+"|Melee)\s(\dD\d|D\d(\+\d)?|\d)\s(N\/A|\d\+)\s(\d)\s(-?\d)\s\d'
# (\d+"|Melee)\s(2D6|D(3|6)\+\d|\d+)\s

weap_regex = fr'{nombre_regex} ({weapkeys_regex})? {weapstats_regex}'

text = "The available options are [OPTION1, OPTION2, OPTION-3, OPTION-4]."
pattern = r"\[(\w+(?:-\w+)?(?:,\s*\w+(?:-\w+)?)*)\]"

matches = re.findall(pattern, text)
print(matches)
