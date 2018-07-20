# -*- coding: utf-8 -*-
# coding=utf-8
import xml.etree.ElementTree as ET
import os
import pandas as pd

excel_file = 'translations.xlsx'
project_name = "Calculator"

lang_dicts = {'ALBANIAN': 'sq',
              'ARABIC': 'ar',
              'BRAZILIAN': 'pt-rBR',
              'BULGARIAN': 'bg',
              'CATALAN': 'ca',
              'CHINE_HK': 'zh-rHK',
              'CHINE_NEW': 'zh-rCN',
              'CHINE_OLD': 'zh-rTW',
              'CROATIAN': 'hr',
              'CZECH': 'cs',
              'DANISH': 'da',
              'DUTCH': 'nl',
              'ENGLISH': 'en',
              'ESTONIAN': 'et',
              'EUSKERA': 'eu',
              'FARSI': 'fa',
              'FINNISH': 'fi',
              'FRENCH': 'fr',
              'FRENCH_CA': 'fr-rCA',
              'GALICIAN': 'gl',
              'GERMAN': 'de',
              'GREEK': 'el',
              'HEBREW': 'iw-rIL',
              'HINDI': 'hi-rIN',
              'HUNGARIAN': 'hu',
              'INDONESIAN': 'id',
              'ITALIAN': 'it',
              'JAPANESE': 'ja',
              'KOREAN': 'ko',
              'LATINESP': 'es-rES',
              'LATVIAN': 'lv-rLV',
              'LITHUANIAN': 'it-rIT',
              'MACEDONIAN': 'mk',
              'MALAY': 'ms',
              'NORWEGIAN': 'nb-rNO',
              'POLISH': 'pl',
              'PORTUGUESE': 'pt',
              'ROMANIAN': 'ro',
              'RUSSIAN': 'ru',
              'SERBIAN': 'sr',
              'SLOVAK': 'sk',
              'SLOVENIAN': 'sl',
              'SPANISH': 'es',
              'SWEDISH': 'sv',
              'THAI': 'th',
              'TURKISH': 'tr',
              'UKRAINIAN': 'uk',
              'URDU': 'ur-rPK',
              'VIETNAMESE': 'vi'
              }


# 获取语言类型
def get_lang_type(lang):
    lang_tables = dict(zip(lang_dicts.values(), lang_dicts.keys()))
    if lang in lang_tables.keys():
        return lang_tables[lang]
    else:
        return None


def get_name_path(file_dir):
    dirs = []
    curPath = os.getcwd() + "\\" + file_dir
    filelist = os.listdir(file_dir)
    for f in filelist:
        # spath = os.path.join(curPath, f)
        if not f.startswith("values"):
            continue
        else:
            # spath = os.path.join(spath, "strings.xml")
            dirs.append(f)

    return dirs
    pass


# 解析excle文档
def save_to_excel(data):
    writer = pd.ExcelWriter(excel_file)
    # index=False 不打印index
    data.to_excel(writer, 'Sheet1', float_format='%.5f', index=False)
    writer.save()
    print("export successfuly")
    pass


def parse_xml():
    dirs = get_name_path('target')
    curPath = os.path.join(os.getcwd(), 'target')
    file_dict = {}
    keys = []
    for dir in dirs:
        spath = os.path.join(curPath, dir, "strings.xml")
        if os.path.exists(spath):
            tree = ET.parse(spath)
            string_dict = {}
            if tree is not None:
                root = tree.getroot()
                nodes = root.findall('string')
                for node in nodes:
                    key = node.attrib['name']
                    value = node.text
                    # print('key===' + key + "===value===" + value)
                    if key not in keys:
                        keys.append(key)
                    string_dict[key] = value
            file_dict[dir] = string_dict
    keys.sort(reverse=False)
    for key in keys:
        for itme, item_value in file_dict.items():
            # print(item_value)
            if key not in item_value.keys():
                item_value[key] = ''

    data = pd.DataFrame()
    refVals = []
    modOPVals = []
    infoVals = []
    zoneTypesVals = []
    isMonoVals = []
    isUKVals = []
    isGSMVals = []
    isTradUpdatableVals = []
    for key in keys:
        refVal = 'S:' + project_name + ':' + key
        refVals.append(refVal)
        modOPVals.append(project_name)
        infoVals.append(None)
        zoneTypesVals.append('ZONE_ANDROID')
        isMonoVals.append('0')
        isUKVals.append('0')
        isGSMVals.append('0')
        isTradUpdatableVals.append(1)
    data['RefName'] = refVals
    data['ModOP'] = modOPVals
    data['Info'] = infoVals
    data['ZoneType'] = zoneTypesVals
    data['ZoneType'] = isMonoVals
    data['IsUK'] = isUKVals
    data['IsGSM'] = isGSMVals
    data['IsTradUpdatable'] = isTradUpdatableVals
    langs = []
    for cl in dirs:
        pos = cl.find('-')
        if pos >= 0:
            if cl[pos + 1:] not in langs:
                langs.append(cl[pos + 1:])
        else:
            if 'en' not in langs:
                langs.append('en')
    cls = []
    for cl in dirs:
        pos = cl.find('-')
        if pos >= 0:
            langtype = get_lang_type(cl[pos + 1:])
        else:
            langtype = get_lang_type('en')
        if langtype is not None:

            if cl in file_dict.keys():
                val = file_dict[cl]
                item_values = []
                for key in keys:
                    item_values.append(val[key])
                data[langtype] = item_values
                cls.append(langtype)
    cls.sort(reverse=False)
    save_to_excel(data)
    pass


def main():
    parse_xml()


if __name__ == '__main__':
    main()
