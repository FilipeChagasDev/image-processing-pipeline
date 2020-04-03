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


# @file _split_merge.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief Split and merge pipes
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

import sys
sys.path.append('../')

import numpy as np
import pipeline as pl

def get_info():
    x = {
        'name': 'split & merge',
        'author': 'Filipe Chagas',
        'email': 'filipe.ferraz0@gmail.com',
        'source': 'https://github.com/FilipeChagasDev/image-processing-pipeline',
        'plugin_version': (1,0,0),
        'ipp_version': (1,0,0)
    }
    return x

def get_classes():
    x = {
        'SplitPipe': SplitPipe,
        'MergePipe': MergePipe
    }
    return x

'''
@brief Splits the 3 channels of the input image for 3 single channel buses.

[Triple] => <Split> => [Channel, Channel, Channel]
'''
class SplitPipe(pl.Pipe):
    my_params = {}
    my_default_args = {}

    def __init__(self):
        in_formats = [pl.BusFormat.Triple]
        out_formats = [pl.BusFormat.Channel, pl.BusFormat.Channel, pl.BusFormat.Channel]
        super(SplitPipe, self).__init__(in_formats, out_formats)

    def callback(self, input: list) -> list:
        data = input[0]
        return [data[:,:,0],data[:,:,1],data[:,:,2]]

'''
@brief Merge the 3 input buses for the output triple bus.

[Channel, Channel, Channel] => <Merge> => [Triple]
'''
class MergePipe(pl.Pipe):
    my_params = {}
    my_default_args = {}
    
    def __init__(self):
        in_formats = [pl.BusFormat.Channel, pl.BusFormat.Channel, pl.BusFormat.Channel]
        out_formats = [pl.BusFormat.Triple]
        super(MergePipe, self).__init__(in_formats, out_formats)

    def callback(self, input: list) -> list:
        in_data0, in_data1, in_data2 = input
        
        shape = [in_data0.shape[0],in_data0.shape[1],1] #[W,H,Channels]
        shape[2] = 3 # 3 Channels
        output_data = np.zeros(shape, np.uint8)

        output_data[:,:,0] = in_data0
        output_data[:,:,1] = in_data1
        output_data[:,:,2] = in_data2

        return [output_data]
