# -*- coding: utf-8 -*-
# coding=utf-8

import os


def get_name_path(file_dir):
    dirs = []
    curPath = os.getcwd() + "\\" + file_dir
    filelist = os.listdir(file_dir)
    for f in filelist:
        spath = os.path.join(curPath, f)
        if not f.startswith("values"):
            continue
        else:
            # spath = os.path.join(spath, "update_strings.xml")
            dirs.append(f)

    return dirs
    pass


def get_name_path2(file_dir):
    dirs = []
    curPath = os.getcwd() + "\\" + file_dir
    filelist = os.listdir(file_dir)
    for f in filelist:
        spath = os.path.join(curPath, f)
        if not f.startswith("values"):
            continue
        else:
            # spath = os.path.join(spath, "strings.xml")
            dirs.append(f)

    return dirs
    pass


def main():
    target_dirs = get_name_path('target')
    for tar in target_dirs:
        tarpath = os.path.join(os.getcwd(), 'target', tar)
        filelist = os.listdir(tarpath)
        for filename in filelist:
            if filename.startswith('string') and filename !='strings.xml':
                filepath = os.path.join(tarpath, filename,)
                targetfile=os.path.join(tarpath,'strings.xml')
                if os.path.exists(targetfile) and os.path.exists(filepath) :
                    content =reads_string(filepath)
                    print(content[3:])
                    write_string(targetfile ,content[3:])
                    os.remove(filepath)








def reads_string(path):
    file = open(path, 'r', encoding='UTF-8')
    lines = file.readlines()
    return lines


def write_string(path, lines):
    file = open(path, 'r+', encoding='UTF-8')
    localLines = file.readlines(100000)
    localLines.pop(len(localLines) - 1)
    file.close()
    targetFile = open(path, 'w+', encoding='UTF-8')
    targetFile.writelines(localLines + lines)
    targetFile.close()


if __name__ == '__main__':
    main()
