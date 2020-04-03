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


# @file _fork_blend.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief fork and blend pipes
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

import sys
sys.path.append('../')

import numpy as np
import pipeline as pl

def get_info():
    x = {
        'name': 'addition',
        'author': 'Filipe Chagas',
        'email': 'filipe.ferraz0@gmail.com',
        'source': 'https://github.com/FilipeChagasDev/image-processing-pipeline',
        'plugin_version': (0,1,0),
        'ipp_version': (0,1,0)
    }
    return x

def get_classes():
    x = {
        'AdditionPipe': AdditionPipe
    }
    return x

class AdditionPipe(pl.Pipe):
    clip = np.vectorize(lambda x: 255 if x > 255 else (0 if x < 0 else (x)))
    
    def __init__(self):
        self.value = 0
        self.clipping = True
        
        params = {'value':int, 'clipping': bool}
        
        super(AdditionPipe, self).__init__([pl.BusFormat.Universal], [pl.BusFormat.Universal], params)
        
        self.arguments['value'] = self.value
        self.arguments['clipping'] = self.clipping

        self.param_changed_callback('value', AdditionPipe.value_changed)
        self.param_changed_callback('clipping', AdditionPipe.clipping_changed)

    def value_changed(self, old_value, new_value):
        self.value = new_value

    def clipping_changed(self, old_value, new_value):
        self.clipping = new_value

    def callback(self, input: list):
        in_data = input[0].astype(np.float)
        add_data = in_data + self.value
        out_data = AdditionPipe.clip(add_data) if self.clipping == True else add_data
        return [out_data]