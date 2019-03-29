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
    origin_dirs = get_name_path2('origin')
    for ori in origin_dirs:
        for tar in target_dirs:
            if ori == tar:
                oripath = os.path.join(os.getcwd(), 'origin', ori, 'string.xml')
                tarpath = os.path.join(os.getcwd(), 'target', tar, 'strings.xml')
                if os.path.exists(tarpath):
                    if os.path.exists(oripath):
                        print("从" + oripath + "导入文件到" + tarpath)
                        contents = reads_string(oripath)
                        write_string(tarpath, contents)


def reads_string(path):
    file = open(path, 'r', encoding='UTF-8')
    lines = file.readlines()
    return lines


def write_string(path, lines):
    # lines.pop(0)
    file = open(path, 'r+', encoding='UTF-8')
    localLines = file.readlines(100000)
    localLines.pop(len(localLines) - 1)
    file.close()
    targetFile = open(path, 'w+', encoding='UTF-8')
    targetFile.writelines(localLines + lines[2:])
    targetFile.close()


if __name__ == '__main__':
    main()
