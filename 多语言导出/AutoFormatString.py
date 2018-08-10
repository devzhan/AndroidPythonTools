# -*- coding: utf-8 -*-
# coding=utf-8

# 从origin 文件夹中把数据写入target 文件夹中

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
    origin_dirs = get_name_path('origin')
    print(target_dirs)
    print(origin_dirs)
    for ori in origin_dirs:
        oripath = os.path.join(os.getcwd(), 'origin', ori)
        print(oripath)

        for tar in target_dirs:
            tarpath = os.path.join(os.getcwd(), 'target', tar)
            if tar == ori:
                orifiles = os.listdir(oripath)
                # tarfiles = os.listdir(tarpath)
                for orifile in orifiles:
                    if orifile == 'strings.xml':
                        sourcefile = os.path.join(tarpath, oripath, 'strings.xml')
                        targetfile = os.path.join(tarpath, 'strings.xml')
                        if os.path.exists(targetfile) and os.path.exists(targetfile):
                            star = 0
                            contents = reads_string(sourcefile)
                            for pos in range(0, len(contents)):
                                item = contents[pos]
                                if '<string' in item:
                                    star = pos
                                    break

                            write_string(targetfile, contents[star:])


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
