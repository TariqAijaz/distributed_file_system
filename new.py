# Save
import json
import os
import pprint
from functools import reduce

dictionary = {}

host = 'localhost'
port = 30000
connections = {'30001' : {'ip':'127.0.0.0','port':30001}, '30002' : {'ip':'127.0.0.0','port':30002}}
filess = {}

BASE_PATH = os.path.dirname(os.getcwd())

import os

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        dirs[:] = [d for d in dirs if d not in ['_pycache_','.git']]
        folders = path[start:].split(os.sep)
        value = {'Type':'F', 'Version': 1}
        subdir = dict.fromkeys(files, value)
        parent = reduce(dict.get, folders[:-1], dir)
        #print(parent)
        parent[folders[-1]] = subdir
    return dir

filess = get_directory_structure(BASE_PATH)

#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(filess)

thing = BASE_PATH+'/config.txt'
dictionary = {'host' : host, 'port' : port, 'connections':connections}

with open(thing, 'w') as fp:
   json.dump(dictionary, fp, indent=4)

with open(BASE_PATH+'/files.txt', 'w') as f:
    json.dump(filess, f, indent=4)

with open(thing, 'r') as fp:
    data = json.load(fp)
    print(str(data))