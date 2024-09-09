import shutil
import os
from re import match

def getFilesInPath(path, regexp = None):
    # getting all files in the specified path
    if regexp is None:
        files = [f for f in os.listdir(path) if os.path.isfile(path + f)]
    else:
        files = [f for f in os.listdir(path) if os.path.isfile(path + f) and match(regexp, f)]

    return files

def moveTo(file, path):
    shutil.move(file, path)

