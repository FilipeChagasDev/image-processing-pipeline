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


# @file product.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief product pipe
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

import sys
sys.path.append('../')

import numpy as np
import pipeline as pl

def get_info():
    x = {
        'name': 'product',
        'author': 'Filipe Chagas',
        'email': 'filipe.ferraz0@gmail.com',
        'source': 'https://github.com/FilipeChagasDev/image-processing-pipeline',
        'plugin_version': (1,0,0),
        'ipp_version': (1,0,0)
    }
    return x

def get_classes():
    x = {
        'ProductPipe': ProductPipe
    }
    return x

class ProductPipe(pl.Pipe):
    #constants
    my_params = {'value':float, 'offset':float,'clipping': bool}
    my_default_args = {'value':0, 'offset':127, 'clipping': True}
    
    #static functions
    clip = np.vectorize(lambda x: 255 if x > 255 else (0 if x < 0 else (x)))
    
    def __init__(self):
        self.value = 0
        self.offset = 127
        self.clipping = True
        
        super(ProductPipe, self).__init__([pl.BusFormat.Universal], [pl.BusFormat.Universal], ProductPipe.my_params)
        
        for p in ProductPipe.my_default_args:
            self.arguments[p] = ProductPipe.my_default_args[p]

        self.param_changed_callback('value', ProductPipe.value_changed)
        self.param_changed_callback('clipping', ProductPipe.clipping_changed)
        self.param_changed_callback('offset', ProductPipe.offset_changed)

    def value_changed(self, old_value, new_value):
        self.value = new_value

    def clipping_changed(self, old_value, new_value):
        self.clipping = new_value

    def offset_changed(self, old_value, new_value):
        self.offset = new_value

    def callback(self, input: list):
        in_data = input[0].astype(np.float)
        mul_data = ((in_data - self.offset) * self.value) + self.offset
        out_data = ProductPipe.clip(mul_data) if self.clipping == True else mul_data
        return [out_data]