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
        'name': 'fork & blend',
        'author': 'Filipe Chagas',
        'email': 'filipe.ferraz0@gmail.com',
        'source': 'https://github.com/FilipeChagasDev/image-processing-pipeline',
        'plugin_version': (0,1,0),
        'ipp_version': (0,1,0)
    }
    return x

def get_classes():
    x = {
        'ChannelForkPipe': ChannelForkPipe,
        'TripleForkPipe': TripleForkPipe,
        'ChannelBlendPipe': ChannelBlendPipe,
        'TripleBlendPipe': TripleBlendPipe
    }
    return x

# ---- BASE FORK & BLEND PIPES ----
'''
@brief Copy input data to any outputs
[format] => <fork> => [format]*number_of_outputs
'''
class BaseForkPipe(pl.Pipe):
    def __init__(self, bus_format: pl.BusFormat):
        self.n_outs = 2
        self.bus_format = bus_format
        default_in_formats = [bus_format]
        default_out_formats = [bus_format] * self.n_outs

        params = {'number_of_outputs':int}

        super(BaseForkPipe, self).__init__(default_in_formats, default_out_formats, params)
        self.arguments['number_of_outputs'] = 2
        self.param_changed_callback('number_of_outputs', BaseForkPipe.n_outs_changed)
        
        

    def n_outs_changed(self, old_arg: int, new_arg: int):
        self.set_out_formats( [self.bus_format] * new_arg )
        self.n_outs = new_arg

    def callback(self, input: list):
        in_data = input[0]
        output = [np.copy(in_data) for x in [0]*self.n_outs]
        return output

'''
@brief Outputs a weighted sum of the input images
[format]*number_of_inputs => <blend> => [format]
'''
class BaseBlendPipe(pl.Pipe):
    def __init__(self, bus_format: pl.BusFormat):
        self.n_ins = 2
        self.bus_format = bus_format
        default_in_formats = [bus_format] * self.n_ins
        default_out_formats = [bus_format]

        params = {'number_of_inputs':int, 'weights':list}

        super(BaseBlendPipe, self).__init__(default_in_formats, default_out_formats, params)
        self.arguments['number_of_inputs'] = 2
        self.param_changed_callback('number_of_inputs', BaseBlendPipe.n_ins_changed)

    def n_ins_changed(self, old_arg: int, new_arg: int):
        self.set_in_formats( [self.bus_format] * new_arg )
        self.n_ins = new_arg

    def callback(self, input: list):
        weights = self.get_param('weights')
        weights = [float(w) for w in weights] #convert weights to float
        w_sum = sum(weights)
        normalized_weights = [w/w_sum for w in weights]

        out_data = np.zeros(input[0].shape)
        for i in range(len(input)):
            out_data += input[i] * normalized_weights[i]

        return [out_data]


# ---- SUB FORK & BLEND PIPES ----
'''
[Channel] => <ChannelFork> => [Channel]*number_of_outputs
'''
class ChannelForkPipe(BaseForkPipe):
    def __init__(self):
        super(ChannelForkPipe, self).__init__(pl.BusFormat.Channel)

'''
[Triple] => <TripleFork> => [Triple]*number_of_outputs
'''
class TripleForkPipe(BaseForkPipe):
    def __init__(self):
        super(TripleForkPipe, self).__init__(pl.BusFormat.Triple)

'''
[Channel]*number_of_inputs => <ChannelBlend> => [Channel]
'''
class ChannelBlendPipe(BaseBlendPipe):
    def __init__(self):
        super(ChannelBlendPipe, self).__init__(pl.BusFormat.Channel)

'''
[Triple]*number_of_inputs => <TripleBlend> => [Triple]
'''
class TripleBlendPipe(BaseBlendPipe):
    def __init__(self):
        super(TripleBlendPipe, self).__init__(pl.BusFormat.Triple)