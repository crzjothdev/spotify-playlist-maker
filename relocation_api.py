import os
from sys import argv

def getFilesInPath(path, fileNameFormat = None):
    # getting all files in the specified path
    files = [f for f in os.listdir(path) if os.path.isfile(dir + '/' + f)]

    return files

def moveTo(file, path):
    os.rename(file, path)

