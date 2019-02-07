#! /bin/env python

import fnmatch
import chardet
import os
import sys

includes = ['*.cc', "*.c", "*.cpp", '*.h', ".hpp", ".hh", '*.txt' ]  # for files only

def fix_encoding_name(coding):
    coding = coding.upper() if coding != None else ""
    if coding[0:3] == 'UTF' or coding == 'ASCII':
        return coding
    return 'GBK'

def convert_encoding(data, path):
    coding = fix_encoding_name(chardet.detect(data)['encoding'])
    if coding != 'UTF-8' and coding != "ASCII":
        print("Before converting file: {}".format(path))
        # Force to decode GBK
        if sys.version_info >= (3, 0):
            data = str(data, coding).encode('UTF-8')
        else:
            data = unicode(data, coding).encode('UTF-8')
        return (data, True)
    return (data, False)

def detect_and_convert(dir):
    for root, dirs, files in os.walk(dir, topdown=False):
        for pat in includes:
            for f in fnmatch.filter(files, pat):
                path = os.path.join(root, f)
                raw_data = open(path, 'rb').read()
                (convert_data, convert) = convert_encoding(raw_data, path)
                if convert:
                    print("Converting file: {}".format(path))
                    open(os.path.join(root, f), 'wb').write(convert_data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} code_root_path".format(sys.argv[0]))
        exit(-1)
    detect_and_convert(sys.argv[1])