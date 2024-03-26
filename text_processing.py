import re
import pandas as pd

dic = {"UNITNAME": None, "KEYWORDS":None, "RANGED WEAPONS": None, "MELEE WEAPONS":None,
       "FACTION KEYWORDS": None, "ABILITIES": {"CORE": None, "FACTION": None, "UNIT": None}}

text_sample = 'RIPPER SWARMS\n' \
              'KEYWORDS:  Swarm, Great Devourer, Ripper SwarmsRANGED WEAPONS RANGE A BS S AP D\n' \
              'Spinemaws [PISTOL] 6" 4 5+ 3 0 1\n' \
              'MELEE WEAPONS RANGE A WS S AP D\n' \
              'Xenos claws and teeth [SUSTAINED HITS 1] Melee 6 5+ 2 0 1\n' \
              'FACTION KEYWORDS:   \n' \
              'TyranidsABILITIES\n' \
              'CORE: Deep Strike\n' \
              'FACTION: Synapse\n' \
              'Chitinous Horrors (Aura): While an enemy unit is within \n' \
              'Engagement Range of this unit, halve the Objective Control \n' \
              'characteristic of models in that enemy unit.M T SV W LD OC\n' \
              '6" 2 6+ 4 8+ 0\n'



line_list = text_sample.split("\n")

def extract_name(line_list, dic):
    dic["UNITNAME"] = line_list[0]
    return dic

def extractKW_weap1(line_list, dic):
    regex1 = '(RANGED|MELEE)'
    # Primer arma y keywords
    kw_weaps = re.split(regex1, line_list[1])
    dic["KEYWORDS"] = kw_weaps[0].replace("KEYWORDS:  ", "").split(", ")

    # Primer arma puede ser ranged o melee
    if "RANGED".__eq__(kw_weaps[1]):
        # ranged_data = line_list[2].split(" ")
        ranged_data = line_list[2].split("] ")
        aux = ranged_data[1].split(" ")
        ranged_data = ranged_data[0].split(" [") + aux
        dic["RANGED WEAPONS"] = {"NAME": ranged_data[0],
                                 "TYPE": ranged_data[1],
                                 "RANGE": ranged_data[2],
                                 "A": ranged_data[3],
                                 "BS": ranged_data[4],
                                 "S": ranged_data[5],
                                 "AP": ranged_data[6],
                                 "D": ranged_data[7]}

    if "MELEE".__eq__(kw_weaps[1]):
        melee_data = line_list[2].split("] ")
        aux = melee_data[1].split(" ")
        melee_data = melee_data[0].split(" [") + aux
        dic["MELEE WEAPONS"] = {"NAME": melee_data[0],
                                 "TYPE": melee_data[1],
                                 "RANGE": melee_data[2],
                                 "A": melee_data[3],
                                 "WS": melee_data[4],
                                 "S": melee_data[5],
                                 "AP": melee_data[6],
                                 "D": melee_data[7]}

    return dic


def extract_melee(line_list, dic):
    # Puede haber segundo arma a melee
    if 'MELEE WEAPONS RANGE A WS S AP D'.__eq__(line_list[3]):
        aux = line_list[4].split(" Melee ")
        if "[" in aux[0]:
            melee_data = aux[0].replace("]", "").split(" [") + aux[1].split(" ")
        else:
            aux.insert(1, None)
            melee_data = aux[0:2] + aux[2].split(" ")

        dic["MELEE WEAPONS"] = {"NAME": melee_data[0],
                                 "TYPE": melee_data[1],
                                 "RANGE": 'Melee',
                                 "A": melee_data[2],
                                 "WS": melee_data[3],
                                 "S": melee_data[4],
                                 "AP": melee_data[5],
                                 "D": melee_data[6]}

    return dic


def extract_factKW(line_list, dic):
    dic["FACTION KEYWORDS"] = re.findall(r'([A-Z][a-z]+)', line_list[6])
    return dic

def extract_abilities(line_list, dic):
    dic["ABILITIES"] = {"CORE": re.sub(r'CORE:\s*', '', line_list[7]),
                        "FACTION": re.sub(r'FACTION:\s*', '', line_list[8]),
                        "UNIT": "".join(line_list[9:-2]).replace("M T SV W LD OC", "")}
    return dic


def extract_profile(line_list, dic):
    chtics = line_list[-2].split(" ")

    dic["M"] = chtics[0]
    dic["T"] = chtics[1]
    dic["SV"] = chtics[2]
    dic["W"] = chtics[3]
    dic["LD"] = chtics[4]
    dic["OC"] = chtics[5]
    return dic


def text_to_dict(text):
    line_list = text.split("\n")
    dic = {"UNITNAME": None, "KEYWORDS": None, "RANGED WEAPONS": None, "MELEE WEAPONS": None,
           "FACTION KEYWORDS": None, "ABILITIES": {"CORE": None, "FACTION": None, "UNIT": None}}
    dic = extract_name(line_list, dic)
    dic = extractKW_weap1(line_list, dic)
    dic = extract_melee(line_list, dic)
    dic = extract_factKW(line_list, dic)
    dic = extract_abilities(line_list, dic)
    dic = extract_profile(line_list, dic)

    return dic

#dic = text_to_dict(text_sample)

datos = pd.read_csv("data.csv")
print(datos)
jsons = []
for i in range(0, 17, 2):
    print(datos.iloc[i][0])
    dic = text_to_dict(datos.iloc[i][0])
    print(dic)
    jsons.append(dic)
