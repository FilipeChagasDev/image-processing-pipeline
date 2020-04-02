# MIT License
# 
# Copyright (c) 2020 Filipe Chagas
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# @file loader.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief IPP plug-ins loading
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

'''
=================================================
===== BEGIN OF RELATIVE PATH CORRECTION CODE ====
=================================================
This code must be at the beginning of all python modules that can be imported dynamically 
or are imported by scripts from other directories.
The goal of this is to allow this script file to use its relative paths in the file system.
@see: https://gist.github.com/FilipeChagasDev/c8736b145ee916f7f5af39b5a63f5da2
'''
import sys

'''
@brief The global variable script_path contains the path of this script in relation to the location of the importer script.
'''
script_path = './'

'''
@bief The global variable my_filename must contain the name of this script file (without the full path).
'''
my_filename = 'loader.py'


'''
@brief The find_script_path function finds and defines script_path.
'''
def find_script_path():
    found = False
    for my_path in sys.path:
        if len(my_path) > 0:
            my_path = my_path + '/' if my_path[-1] != '/' else my_path
        else:
            my_path = './'

        globals()['script_path'] = my_path

        try:
            open(script_path + my_filename)
            found = True
        except:
            continue

        break

    return found

'''
@brief The rpath function returns the correctness of a path relative to the location of this script file.
@param my_path Path in relation to this script file.
'''
def rpath(my_path: str) -> str:
    if not my_path[0] == '/': #not a root path
        return script_path + my_path
    else:
        return my_path

class RPath:
    def __init__(self, my_path):
        if isinstance(my_path, str):
            self.txt = rpath(my_path)
        elif isinstance(my_path, RPath):
            self.txt = my_path.txt
        else:
            raise Exception('Invalid my_path type')

    def to_str(self):
        return self.txt

find_script_path()

'''
===============================================
===== END OF RELATIVE PATH CORRECTION CODE ====
===============================================
'''

import os
import fnmatch as fm

'''
@brief Import module dynamically
@param fn Module file path
@return (name, module)
'''
def get_module(fn: str):
    script_fn = fn.split('/')[-1] #remove 'root/' from 'root/filename.py'
    
    script_root = fn.split('/')
    del script_root[-1] #remove 'filename.py' from 'root/filename.py'
    script_root = '/'.join(script_root) + '/'
    
    module_name = script_fn.split('.')[0] #remove '.py' from 'filename.py'
    
    if script_root not in sys.path:
        sys.path.append(script_root)
    
    return (module_name, __import__(module_name))


#constant
plugins_dir_name = 'plugins' 


'''
@brief Load all plug-in modules from plugins directory
@return Dictionary with all the modules. Format: {'module_name': module_object, ...}
'''
def load_plugins():
    plugins_path = rpath(plugins_dir_name) + '/'
    plugins_dir_list = [plugins_path + fn for fn in os.listdir(plugins_path)]
    plugin_files = [fn for fn in plugins_dir_list if (os.path.isfile(fn) and fm.fnmatch(fn, '*.py'))]

    module_dict = {}
    for pf in plugin_files:
        mod_name, mod_obj = get_module(pf)
        module_dict[mod_name] = mod_obj

    return module_dict


