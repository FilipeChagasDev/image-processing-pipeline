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


# @file hadamard.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief hadamard pipe
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

import sys
sys.path.append('../')

import numpy as np
import cv2 as cv
import pipeline as pl

def get_info():
    x = {
        'name': 'hadamard',
        'author': 'Filipe Chagas',
        'email': 'filipe.ferraz0@gmail.com',
        'source': 'https://github.com/FilipeChagasDev/image-processing-pipeline',
        'plugin_version': (1,0,0),
        'ipp_version': (1,0,0)
    }
    return x

def get_classes():
    x = {
        'ChannelHadamardPipe': ChannelHadamardPipe,
        'TripleHadamardPipe': TripleHadamardPipe
    }
    return x


class BaseHadamardPipe(pl.Pipe):
    my_params = {'normalize_mask': bool, 'uniform_normalization': bool, 'clipping': bool}
    my_default_args = {'normalize_mask': True, 'uniform_normalization': True, 'clipping': False}
    
    def __init__(self, format: pl.BusFormat):
        self.format = format
        in_formats = [format, format] #[image, mask]
        out_formats = [format]
        super(BaseHadamardPipe, self).__init__(in_formats, out_formats, BaseHadamardPipe.my_params)
        
        for p in BaseHadamardPipe.my_default_args:
            self.arguments[p] = BaseHadamardPipe.my_default_args[p]

        self.norm_mask = True
        self.unfrm_norm = True
        self.clip = np.vectorize(lambda x : x)

        self.param_changed_callback('normalize_mask', BaseHadamardPipe.norm_mask_changed)
        self.param_changed_callback('clipping', BaseHadamardPipe.clipping_changed)
        self.param_changed_callback('uniform_normalization', BaseHadamardPipe.unfrm_norm_changed)

    def norm_mask_changed(self, old_arg, new_arg):
        self.norm_mask = new_arg

    def unfrm_norm_changed(self, old_arg, new_arg):
        self.unfrm_norm = new_arg

    def clipping_changed(self, old_arg, new_arg):
        if new_arg == True:
            self.clip = np.vectorize(lambda x : 255 if x > 255 else (0 if x < 0 else (x)))
        else:
            self.clip = np.vectorize(lambda x : x)

    def callback(self, input: list) -> list:
        in_img, mask = (input[0].astype(np.float), input[1])
        mask = cv.resize(mask, (in_img.shape[1], in_img.shape[0]) ).astype(np.float)
        
        if self.norm_mask == True:
            if self.format in pl.bus_compatibility[pl.BusFormat.Triple]: #triple channel image
                if self.unfrm_norm == False: #channel per channel normalization
                    for ch in (0,1,2):
                        mask[:,:,ch] = mask[:,:,ch] / np.max(mask[:,:,ch])
                else: #full array normalization
                    mask = mask / np.max(mask)    
            else: #simple channel image
                mask = mask / np.max(mask)

        out_data = self.clip(in_img * mask)
        return [out_data]

class ChannelHadamardPipe(BaseHadamardPipe):
    def __init__(self):
        super(ChannelHadamardPipe, self).__init__(pl.BusFormat.Channel)

class TripleHadamardPipe(BaseHadamardPipe):
    def __init__(self):
        super(TripleHadamardPipe, self).__init__(pl.BusFormat.Triple)
        