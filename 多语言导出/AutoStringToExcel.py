# -*- coding: utf-8 -*-
# coding=utf-8
import json
import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np

excel_file = 'translations.xlsx'
project_name = "Note"

lang_tables = {
    'CHINE_NEW': 'zh-rCN',  # 简体中文
    'CHINE_HK': 'zh-rHK',  # 香港中文
    'CHINE_OLD': 'zh-rTW',  # 台湾中文
    'English': 'en',  # 英语
    'English_US': 'en-rUS',  # 美英语

    'FRENCH': 'fr',  # 法语
    'DUTCH': 'nl',  # 荷兰
    'GERMAN': 'de',  # 德国
    'GREEK': 'el',  # 希腊
    'HUNGARIAN': 'hu',  # 匈牙利
    'ITALIAN': 'it',  # 意大利
    'PORTUGUESE': 'pt',  # 葡萄牙
    'SPANISH': 'es',  # 西班牙
    'TURKISH': 'tr',  # 土耳其
    'POLISH': 'pl',  # 波兰
    'CZECH': 'cs',  # 捷克
    'MALAY': 'ms',  # 马来语
    'INDONESIAN': 'id',  # 印尼
    'SLOVAK': 'sk',  # 斯洛伐克
    'ROMANIAN': 'ro',  # 罗马尼亚
    'SLOVENIAN': 'sl',  # 斯洛文尼亚
    'THAI': 'th',  # 泰国
    'SERBIAN': 'sr',  # 塞尔维亚
    'GALICIAN': 'gl',  # 加利西亚
    'VIETNAMESE': 'vi',  # 越南
    'BRAZILIAN': 'pt-rBR',  # 巴西
    'JAPANESE': 'ja',  # 日语
    'LATINESP': 'es-rLA',  # 拉丁西班牙语
    'FARSI': 'fa',  # 波斯
    'CROATIAN': 'hr',  # 克罗地亚
    'RUSSIAN': 'ru',  # 俄语
    # IDOL3 与 MIE 差异
    'ARABIC': 'ar',  # 阿拉拍语
    'CATALAN': 'ca',  # 加泰罗尼亚
    'DANISH': 'da',  # 丹麦
    'FINNISH': 'fi',  # 芬兰
    'FRENCH_CA': 'fr-rCA',  # 法语-加拿大
    'NORWEGIAN': 'nb-rNo',  # 挪威
    'SWEDISH': 'sv',  # 瑞典
    'EUSKERA': 'eu',  # 巴斯克
    # IDOL3 新增语言
    'ALBANIAN': 'sq',  # 阿尔巴尼亚文
    'BENGALI': 'bn-rBD',  # 孟加拉
    'BULGARIAN': 'bg',  # 保加利亚语
    'CAMBODIAN': 'km-rKH',  # 柬埔寨
    'ESTONIAN': 'et',  # 爱沙尼亚语
    'HEBREW': 'he',  # 希伯来语
    'KOREAN': 'ko',  # 朝鲜语
    'LAOTIAN': 'lo-rLA',  # 老挝语
    'LATVIAN': 'lv',  # 拉脱维亚语
    'LITHUANIAN': 'lt',  # 立陶宛
    'MACEDONIAN': 'mk',  # 马其顿
    'MYANMAR': 'my-rMM',  # 缅甸
    'UKRAINIAN': 'uk',  # 乌克兰语
    'Urdu': 'ur_PK',  # 巴基斯坦
}


# 获取语言类型
def get_lang_type(lang):
    for (d, x) in lang_tables.items():
        print('d==='+d+'===x==='+x)
        print('lang==='+lang)

        if x.lower() == lang.lower():
            return d
        elif x.lower()=='':
            return 'English'
        else:
            return lang.upper()
    return lang.upper()


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
                # print("当前文件是===" + spath)
                root = tree.getroot()
                nodes = root.findall('string')
                for node in nodes:
                    key = node.attrib['name']
                    value = node.text
                    print('key===' + key + "===value===" + value)
                    if key not in keys :
                        keys.append(key)
                    string_dict[key] = value
            file_dict[dir] = string_dict
    keys.sort(reverse=False)
    for key_item in keys:
        for itme, itme_value in file_dict.items():
            if key_item not in itme_value:
                itme_value[key_item] = ''
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
    print(dirs)
    for cl in dirs:
        pos = cl.find('-')
        if pos >= 0:
            langtype = get_lang_type(cl[pos + 1:])
        else:
            langtype = get_lang_type('default')
        print(langtype)
        if langtype is not None:
            if cl in file_dict.keys():
                val = file_dict[cl]
                item_values = []
                for item_key, item_val in val.items():
                    item_values.append(item_val)
                data[langtype] = item_values

    print(data.columns)
    save_to_excel(data)
    pass


def main():
    parse_xml()


if __name__ == '__main__':
    main()
