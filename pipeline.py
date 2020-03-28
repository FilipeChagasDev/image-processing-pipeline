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


# @file pipeline.py
# @author Filipe Chagas
# @date 28 / 03 / 2020
# @brief Base classes of image processing pipelines
# @see https://github.com/FilipeChagasDev/image-processing-pipeline

from enum import Enum
import numpy as np

'''
@brief Image data format of a bus
'''
class BusFormat(Enum):
    BGR = 1 # [BLUE, GREEN, RED] for each pixel
    RGB = 2 # [REG, GREEN, BLUE] for each pixel
    HSV = 3 # [HUE, SATURATION, VALUE] for each pixel
    Channel = 4 # Single channel image data
    Triple = 5 # Triple channel image data (BGR or RGB or HSV)
    Universal = 6 # Single channel or triple channel

'''
@brief Bus perform the connection between the pipes of the pipeline
'''
class Bus(object):
    '''
    @param name Unique name across the pipeline for the bus.
    @param format BusFormat of the bus.
    '''
    def __init__(self, name: str, format: BusFormat):
        self.name = name
        self.format = format
        self.data = None

    '''
    @brief Reset attributes to a new feed-foward process. 
    '''
    def reset(self):
        self.data = None

    '''
    @brief Put an image data into the bus
    '''
    def set_data(self, data):
        if self.data == None:
            self.data = data
        else:
            raise Exception( str(self.name) + ' BUS FAULT: A bus cannot have more than one input')

    '''
    @brief Get image data from the bus
    '''
    def get_data(self):
        if self.data == None:
            raise Exception( str(self.name) + ' BUS FAULT: Empty bus')

        return self.data

'''
@brief The Pipe class corresponds to a processing unit in the pipeline. The methods of this class perform image processing and bus connection tasks.
'''
class Pipe(object):
    '''
    @param name Unique name across the pipeline for the pipe.
    @param parent_pipeline Pipeline object where it is nested.
    @param in_formats List of the input buses formats
    @param out_formats List of the output buses formats 
    '''
    def __init__(self, name: str, parent_pipeline, in_formats: list, out_formats: list):
        self.name = name
        self.parent_pipeline = parent_pipeline
        self.in_formats = in_formats
        self.out_formats = out_formats

    
    '''
    @brief Check if is there any error in the buses settings.
    @param in_bus_names List of the input buses names.
    @param out_bus_names List of the output buses names.
    '''
    def check_buses(self, in_bus_names: list, out_bus_names: list) -> bool:
        if len(in_bus_names) != len(self.in_formats) or len(out_bus_names) != len(self.out_formats):
            raise Exception(str(self.name) + ' PIPE FAULT: Number of input or output buses incompatible with the pipe')
        
        for i in range(len(in_bus_names)):
            if self.in_formats[i] != self.parent_pipeline.buses[in_bus_names[i]].format:
                raise Exception(str(self.name) + ' PIPE FAULT: Input buses formats incompatible with the pipe')
        
        for i in range(len(out_bus_names)):
            if self.out_formats[i] != self.parent_pipeline.buses[out_bus_names[i]].format:
                raise Exception(str(self.name) + ' PIPE FAULT: Output buses formats incompatible with the pipe')


    '''
    @brief Get all the input images from buses, apply the filtering, get the output images and send to de buses.
    @param in_bus_names List of the input buses names.
    @param out_bus_names List of the output buses names.
    '''
    def process(self, in_bus_names: list, out_bus_names: list):
        self.check_buses(in_bus_names, out_bus_names)
        input_list = []
        
        #Get data from buses
        for n in in_bus_names:
            current_bus = self.parent_pipeline.buses[n]
            input_list.append( np.copy(current_bus.get_data()) )

        output_list = self.callback(input_list)

        # Check output data validity by len
        if len(output_list) != len(out_bus_names):
            raise Exception(str(self.name) + ' PIPE FAULT: Pipe.callback returning invalid data. Internal error.')

        for i in range(len(output_list)):
            #Check output data format by shape
            if self.out_formats[i] == BusFormat.Channel:
                if output_list[i].shape[2] != 1:
                    raise Exception(str(self.name) + ' PIPE FAULT: Pipe.callback returning invalid data format. Internal error.')
            elif self.out_formats[i] != BusFormat.Universal:
                if output_list[i].shape[2] != 3:
                    raise Exception(str(self.name) + ' PIPE FAULT: Pipe.callback returning invalid data format. Internal error.')

            #Send data to bus
            self.parent_pipeline.buses[out_bus_names[i]].set_data(output_list[i])
        
    '''
    @brief Method that will be called to apply the filtering. It must be overwrited.
    @param input List of input images
    @return List of output images
    '''
    def callback(self, input: list) -> list:
        raise Exception(str(self.name) + ' PIPE FAULT: It is not possible to use the Pipe class without overwriting callback')
        return []