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


# @file fork_blend.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief fork and blend pipes
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

import pipeline as pl 
import numpy as np

# ---- BASE FORK & BLEND PIPES ----

class BaseForkPipe(pl.Pipe):
    def __init__(self, bus_format: pl.BusFormat):
        self.n_outs = 2
        self.bus_format = bus_format
        default_in_formats = [bus_format]
        default_out_formats = [bus_format] * self.n_outs

        params = {'number of outputs':int}

        super(BaseForkPipe, self).__init__(default_in_formats, default_out_formats, params)
        self.param_changed_callback('number of outputs', BaseForkPipe.n_outs_changed)
        

    def n_outs_changed(self, old_arg: int, new_arg: int):
        self.set_out_formats( [self.bus_format] * new_arg )
        self.n_outs = new_arg

    def callback(self, input: list):
        in_data = input[0]
        output = [np.copy(in_data) for x in [0]*self.n_outs]
        return output

#TODO BaseBlendPipe

# ---- SUB FORK & BLEND PIPES ----
class ChannelForkPipe(BaseForkPipe):
    def __init__(self):
        super(ChannelForkPipe, self).__init__(pl.BusFormat.Channel)

class TripleForkPipe(BaseForkPipe):
    def __init__(self):
        super(TripleForkPipe, self).__init__(pl.BusFormat.Triple)

#TODO ChannelBlendPipe
#TODO TripleBlendPipe