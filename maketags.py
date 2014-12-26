#!/usr/bin/python

import sys
import os
import glob
import re

LIB_PATH = sys.path
WORKSPACE = ["/Users/moyunli/workspace"]
REVERSE = 1
NON_REVERSE = 0
OUTPUT_PATH="."
FILENAMETAG="filenametags"
FILELIST="filelist.txt"
ALLFILELIST="allfilelist.txt"

include_list = [
#    [re.compile(r'__init__'), REVERSE],
    [re.compile(r'.*\.py\b'), NON_REVERSE],
    [re.compile(r'.*\.yaml\b'), NON_REVERSE],
]

exclude_list = [
    [re.compile(r'pip'), REVERSE],
    [re.compile(r'build'), REVERSE],
]

def find(path, result_list):
    if (len(path) == 0):
        return

    for item in glob.glob(os.path.join(path, "*")):
        if os.path.isdir(item) :
            find(item, result_list)
        else:
            result_list.append(item)
    return

def grep(source, compiledPattern ,reverse):
    ret = compiledPattern.search(source)
    if (REVERSE == reverse):
        return not ret
    else:
        return ret

def exec_main( generate_lib = True):
    project_list = []
    lib_list=[]
    project_all = []
    lib_all =[]
    for path in LIB_PATH:
        find(path, lib_all)
    for path in WORKSPACE:
        find(path, project_all)
    for f in include_list:
        project_list.extend( [source for source in project_all if grep(source, f[0], f[1])] )
        lib_list.extend( [source for source in lib_all if grep(source, f[0], f[1])] )

    for f in exclude_list:
        project_list = [source for source in project_list if grep(source, f[0], f[1])]
        lib_list = [source for source in lib_list if grep(source, f[0], f[1])]


    all_file_list_name = os.path.join(OUTPUT_PATH, ALLFILELIST)
    proj_file_list_name = os.path.join(OUTPUT_PATH, FILELIST)
    proj_file_tag = os.path.join(OUTPUT_PATH, FILENAMETAG)

    all_file_list_handle = open(all_file_list_name, 'w')
    proj_file_list_handle = open(proj_file_list_name, 'w')
    proj_file_tag_handle = open(proj_file_tag, 'w')
    proj_file_tag_handle.write('!_TAG_FILE_SORTED\t2\t/2=foldcase/\n')

    for s in project_list:
        if s not in lib_list:
            line = "%s\n" % os.path.abspath(s)
            proj_file_list_handle.write(line)
            all_file_list_handle.write(line)
            line = "%s\t%s\t1\n" % (os.path.basename(s), os.path.abspath(s))
            proj_file_tag_handle.write(line)
    proj_file_list_handle.close()
    proj_file_tag_handle.close()

    for s in lib_list:
        all_file_list_handle.writelines("%s\n" % s)
    all_file_list_handle.close()


    ctag_file = os.path.join(OUTPUT_PATH, "tags")
    cscope_file = os.path.join(OUTPUT_PATH, "cscope.out")

    import subprocess
    ret = subprocess.call(["ctags", "-L", all_file_list_name, '-f', ctag_file])
    subprocess.call(["cscope", "-RbqU", "-i", proj_file_list_name, '-f', cscope_file], shell=False)
    print "Done!\n"


if __name__ == '__main__':
    exec_main()
