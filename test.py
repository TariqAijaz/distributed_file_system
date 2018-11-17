import socket
import sys
import os
import json
import pprint
from functools import reduce
import sys
import subprocess
def path_to_dict(path):
      d = {'name': os.path.basename(path)}
      if os.path.isdir(path):
            d['types'] = "directory"
            d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
                              (path)]
      else:
            d['type'] = "file"
      return d
      
startpath = os.getcwd()
root = startpath+'\\root'

# root_dict.update(children)
# root_dict['children'].update(file)
# exit()
# directory_structure = path_to_dict(root)

# with open(root+'\\files.json', 'w') as f:
#     json.dump(root_dict, f, indent=4)

f = open(root+'\\files.json', 'r')
dictionary = json.load(f)

# exit()
# if 'children' in dictionary.keys():
#       print('ok')
#       # if isinstance('root',dict):
#       for v in dictionary.values():
#             if isinstance(v, dict):
#                   print('ok')


# def recursive_lookup(k, dictionary):
#       if k in dictionary:
#             return dictionary[k]
#       for v in dictionary.values():
#             if isinstance(v, dict):
#                   return recursive_lookup(k, v)
#       return None

# print('ba', recursive_lookup('tariq', dictionary))

# exit()
# blah = {'root' : {'type':'f','children': {"tariq": {
#                 "name": "tariq",
#                 "type": "directory",
#                 "children": {
#                     "sakina.txt": {
#                         "name": "sakina.txt",
#                         "type": "file"
#                     }
#                 }
#             }}}}

def list_directory(path):
      values = []
      path_component = {}
      for p in path:
            path_component = path.split('\\')
      f = open(root+'\\files.json', 'r')
      structure = json.load(f)
      for comp in path_component:
            if comp in structure.keys():
                  structure = structure[comp]['children']
      for value in structure.keys():
            values.append(value)
      return values
            
def make_directory(path, folder_name):
      directory_structure = { folder_name: {
            'name':folder_name,
            'type':'directory',
            'children':{}
            }
      }
      path_component = {}
      for p in path:
            path_component = path.split('\\')
      with open(root+'\\files.json', 'r') as f:
            prev_structure = json.load(f)
      structure = prev_structure
      for comp in path_component:
            if comp in structure.keys():
                  structure = structure[comp]['children']

      if folder_name in structure.keys():
            print('Folder Exists!')
      else:
            structure.update(directory_structure)
            print("Directory Created")

      for key in prev_structure:
          if key in structure:         
            prev_structure[key].update(structure[key])

      with open(root+'\\files.json', 'w') as f:
          json.dump(prev_structure, f, indent=4)

def make_file(path, file_name,sock):
      file_name = { file_name: {
            'name': file_name,
            'type':'file',
            'map': sock
            }
      }
      path_component = {}
      for p in path:
            path_component = path.split('\\')
      with open(root+'\\files.json', 'r') as f:
            prev_structure = json.load(f)
      structure = prev_structure
      for comp in path_component:
            if comp in structure.keys():
                  structure = structure[comp]['children']
      
      if file_name in structure.values():
            print('File Exists!')
      else:
            structure.update(file_name)
            print("File Created")

      for key in prev_structure:
          if key in structure:         
            prev_structure[key].update(structure[key])

      with open(root+'\\files.json', 'w') as f:
          json.dump(prev_structure, f, indent=4)

def open_file(path, filename):
      files = list_directory(path)
      if filename in files:
            theproc = subprocess.Popen(['notepad',filename])
            theproc.communicate()
      
# def change_directory(path, directory_name):
      # directory = list_directory(path)
      # if directory_name in directory:
      #       print('Directory Changed')
      # else:
      #       print('Invalid')
      

path = "root"
# open_file(path,'asra.txt')
print(list_directory(path))
# make_directory(path,'asra')
# make_file(path,'asra.txt')
# change_directory(path,'tariq')
# def runcmd(cmd):
#     x = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
#     return x.communicate()


      



            # if file in structure.values():
            #       recursive_lookup(file, structure)
      
            # else:
            #       print('file exists')
            #       structure[filename] 
            #       if 'children' in structure.keys():
            #             current_pointer = structure['children']
            #             for files in current_pointer.key():
                  
      

# for files in dictionary['children']:
#       if type(dictionary['children']) == dict:
#             print('ok')
#       else:
#             print('not ok')
            # if 'tariq' in dictionary['children'].keys():
            #       if 'name' in dictionary['tariq'].keys():

            # # root_dict.update(dictionary)
            #             print('root_dict')
# with open(root+'\\files.json', 'w') as f:
#     json.dump(root_dict, f, indent=4)
# path = 'root'


# print(level)






# if 'children' in dictionary.keys():
#       for files in dictionary['children']:
#             # if 'tariq' in files:
#                   print(files)
                        # x = dictionary['children'].get(filename)
                        # for keys, values in x.items():
                        #       if 'name' in keys:
                        #             print(values)
                              


# if 'children' in dictionary.keys():
#       for files in dictionary['children']:
#             print(files)
      
# with open(root+'\\files.json', 'w') as f:
#     json.dump(root_dict, f, indent=4)

# def read_from_directory_structure(root):
#       if 'children' in directory_structure.keys():
#             for c in root['children']:
#                   print(c['name'])

            
      # a = 'Neew FOlder'
      # if 'children' in directory_structure.keys():
      #       for c in root['children']:
      #             if c['name'] == a:
      #                   root = c['name']
      # else:
      #       print('folder is empty')
      # print(directory_structure)
            
      # for name in dicte.items():
            # print(name['children'])
            # for children in name['children'].items():
            #       print(children)
      # print(dicte['type'])


# print(read_from_directory_structure(root))
# for x in dicte:
#       print(dicte)
# with open(BASE_PATH+'/files.txt', 'w') as f:
#       json.dump(list_files(startpath), f, indent=4)
# print("Path at terminal when executing this file")
# print(os.getcwd() + "\n")

# print("This file path, relative to os.getcwd()")
# print(__file__ + "\n")

# print("This file full path (following symlinks)")
# full_path = os.path.realpath(__file__)
# print(full_path + "\n")

# print("This file directory and name")
# path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")

# print("This file directory only")
# print(os.path.dirname(full_path))


# directory = os.listdir()
# str1 = '\n'.join(directory)
# print(str1)

# config_file = {
#                   "Server_A": {
#                   "ip": "localhost",
#                   "port": 30000
#                   },
#                   "Server_B":  {
#                   "ip": "localhost",
#                   "port": 30001
#                   },
#                   "Server_C": {
#                   "ip": "localhost",
#                   "port": 30002
#                   }
#             }
# print(config_file['Server_A']['port'])

# f = open("configA.txt", "r")
# with open("config.txt", 'w+') as fp:
#       json.dump(config_file, fp, indent=4)

# f = open('configA.txt', 'r')

#your_dictionary = f.read()
# dicte = json.load(f)
#print(dicte["connections"])
# connections = dicte['connections']

# for server,connection in connections.items():
#       #print(server)
#       print(connection['port'])

# for line in f:
#       for word in line.split():
#             print(word)  

# data = json.loads(f.read())
# print(data)
      # print(port)
      # print(ip)
      # for key in 
      # for key in server_info:
      # print()

# def myprint(d):
#       for k, v in d.items():
#             if isinstance(v, dict):
#                   myprint(v)
#       else:
#             print("{0} : {1}".format(k, v))

# myprint(config_file)
# x = os.path.dirname(__file__)
# str1 = "this is really a string example....wow!!!"
# str2 = "is"

# # print(str1.rfind(str2))
# BASE_PATH = os.path.realpath(os.getcwd())
# x = os.walk(BASE_PATH)
# print(BASE_PATH)
# print(x)
# import socket
# socket_between_servers = None


# def connect_to(host='', port=1060):
#    global socket_between_servers
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#       sock.connect((host, port))  #check if the first server is already waiting
#       socket_between_servers = sock
#    except socket.error:
#       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#       s.bind((host, port))
#       s.listen(5)  # waiting for the 4 clients plus the other server
#       print ('waiting for the peers...')
#       n = 0
#       while n < 5:
#          sc, sockname = s.accept()
#          if sockname == 'ip addresse of the other server':
#             socket_between_servers = sc
#          n += 1
#    else:
#       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#       s.bind((host, port + 1))
#       s.listen(4)  # waiting for the 4 clients
#       n = 0
#       while n < 4:
#          sc, sockname = s.accept()