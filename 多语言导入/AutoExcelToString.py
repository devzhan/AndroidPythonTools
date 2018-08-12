# -*- coding: utf-8 -*-
# coding=utf-8

import os
import pandas as pd

excel_file = 'Translated_Calculator.xlsx'
firstline = ['<?xml version="1.0" encoding="utf-8" standalone="no"?>',
             '<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">']
lastline = ['</resources>']

lang_tables = {
    'CHINE_NEW': 'zh-rCN',  # 简体中文
    'CHINE_HK': 'zh-rHK',  # 香港中文
    'CHINE_OLD': 'zh-rTW',  # 台湾中文
    'ENGLISH': 'en',  # 英语
    'ENGLISH_US': 'en-rUS',  # 美英语
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
    'INDONESIAN': 'in',  # 印尼
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
    # 'NORWEGIAN': 'nb-rNo',  # 挪威
    'NORWEGIAN': 'no',  # 挪威
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
    'Urdu': 'ur-PK',  # 巴基斯坦
}






# 获取语言类型
def get_lang_type(lang):
    for (d, x) in lang_tables.items():
        if d.lower() == lang.lower():
            return x
    return lang.lower()


# 解析excle文档
def parse_excel():
    datas = pd.read_excel(excel_file, sheet_name='Sheet1')
    colums = datas.columns.tolist()
    values = []
    values = values + colums[7:]
    lines = []
    for value in values:
        lines.clear()
        items = datas.loc[:, ['RefName', value]]
        items =items.dropna()#删除为nan的元素
        langType = get_lang_type(value)
        flodername = 'values-' + langType
        create_folder(flodername)
        filepath = os.path.join(os.getcwd(), flodername, 'string.xml');
        file = open(filepath, 'w', encoding='UTF-8')
        lines.append(firstline[0])
        lines.append(firstline[1])
        for indexs in items.index:
            name = items.loc[indexs].values[0:][0]
            pos = name.rfind(':')
            if pos == 0:
                key = name
            else:
                key = name[pos + 1:]
            key_value = items.loc[indexs].values[0:][1]
            # print('key===' + str(key) + '===value===' + str(key_value))
            # < stringname = "attachments" > "Anhänge" < / string >
            keystr = str(key)
            valuestr = str(key_value)
            # if valuestr != 'nan':
            content = '<string name="' + keystr + '">"' + valuestr + '" </string >'
            lines.append(content)


        lines.append(lastline[0])
        print('将文档的第' + value + '列写入到文件' + filepath)
        file.writelines([line + '\n' for line in lines])
        file.close()
    pass


def create_folder(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    curretnpath = os.getcwd();
    folderpath = os.path.join(curretnpath, path)
    isExists = os.path.exists(folderpath)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在,删除已存在的目录以及下面的文件，并创建新的目录
        print(path + ' 目录已存在')
        del_file(path)
        return False
    pass


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def main():
    parse_excel()


if __name__ == '__main__':
    main()
