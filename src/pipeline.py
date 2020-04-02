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

bus_compatibility = {
    BusFormat.BGR: [BusFormat.BGR],
    BusFormat.RGB: [BusFormat.RGB],
    BusFormat.HSV: [BusFormat.HSV],
    BusFormat.Channel: [BusFormat.Channel],
    BusFormat.Triple: [BusFormat.Triple, BusFormat.BGR, BusFormat.RGB, BusFormat.HSV],
    BusFormat.Universal: [BusFormat.Universal, BusFormat.Channel, BusFormat.Triple, BusFormat.BGR, BusFormat.RGB, BusFormat.HSV]
}

def fit_tuple(input_tuple: tuple, default_value, out_len: int) -> tuple:
    in_len = len(input_tuple)

    out = [default_value] * out_len
    
    if out_len >= in_len:
        for i in range(in_len):
            out[i] = input_tuple[i]
    else:
        for i in range(out_len):
            out[i] = input_tuple[i]
            
    return tuple(out)

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
        self.empty = True

    '''
    @brief Reset attributes to a new feed-foward process. 
    '''
    def reset(self):
        self.data = None
        self.empty = True

    '''
    @brief Put an image data into the bus
    '''
    def set_data(self, data):
        if self.empty == True:
            self.data = np.array(data, np.uint8)
            self.empty = False
        else:
            self.raise_fault('A bus cannot have more than one input')

    '''
    @brief Get image data from the bus
    '''
    def get_data(self):
        if self.empty == True:
            self.raise_fault('Empty bus')

        return self.data

    def raise_fault(self, msg: str):
        raise Exception( str(self.name) + ' BUS FAULT: ' + msg)

'''
@brief The Pipe class corresponds to a processing unit in the pipeline. The methods of this class perform image processing and bus connection tasks.
'''
class Pipe(object):
    auto_counter = -1 #global
    undefined_arg = None #constant
   
    '''
    @param in_formats List of the input buses formats
    @param out_formats List of the output buses formats 
    @param params (optional) Pipe parameters dictionary with {'param_name':type} relation for each param 
    '''
    def __init__(self, in_formats: list, out_formats: list, params: dict = {}):
        Pipe.auto_counter += 1 
        self.name = 'Pipe' + str(Pipe.auto_counter)
        self.parent_pipeline = None
        self.in_formats = in_formats
        self.out_formats = out_formats
        
        self.params = params #format: {'param_name':type, ...}
        self.param_changed_callbacks = {} #format: {'param_name':function, ...}
        self.arguments = {} #format: {'param_name':value, ...}
        for param in params:
            if type(param) != str:
                self.raise_fault('Param name must be a string. Error in param ' + str(param))
            
            if not isinstance(params[param], type):
                self.raise_fault('Param must have a type. Error in param ' + str(param))

            self.arguments[param] = Pipe.undefined_arg


    def set_in_formats(self, in_formats: list):
        self.in_formats = in_formats

    def set_out_formats(self, out_formats: list):
        self.out_formats = out_formats

    '''
    @brief Set a callback method to be called after the param argument changes
    @param param_name Name of the param
    @param method Callback method. format: Pipe.method(self, old_argument, new_argument)
    '''
    def param_changed_callback(self, param_name: str, method):
        if param_name not in self.params:
            self.raise_fault('Undefined param: ' + str(param_name))
        
        self.param_changed_callbacks[param_name] = method

    '''
    @brief Set the value of a param
    @param param_name Name of the param
    @param argument Value of the param
    '''
    def set_param(self, param_name: str, argument):
        if param_name not in self.params:
            self.raise_fault('Undefined param: ' + str(param_name))
        
        if not isinstance(argument, self.params[param_name]):
            self.raise_fault('Invalid argument type for ' + str(param_name) + '. ' + str(argument) + ' is not instance of ' + str(self.params[param_name]))

        old_argument = self.arguments[param_name]
        self.arguments[param_name] = argument

        if param_name in self.param_changed_callbacks:
            callback_method = self.param_changed_callbacks[param_name]
            callback_method(self, old_argument, argument)
            
    
    '''
    @brief Get the value of a param
    @param param_name Name of the param
    @return argument Value of the param
    '''
    def get_param(self, param_name: str):
        if param_name not in self.params:
            self.raise_fault('Undefined param: ' + str(param_name))
        
        argument = self.arguments[param_name]
        if not isinstance(argument, self.params[param_name]):
            self.raise_fault('Undefined argument for ' + str(param_name) + '. ' + str(argument) + ' is not instance of ' + str(self.params[param_name]))

        return argument

    '''
    @brief Set the reference to the Pipeline object where this Pipe is nested.
    @param parent_pipeline Pipeline object where this Pipe is nested.
    '''
    def set_parent(self, parent_pipeline):
        self.parent_pipeline = parent_pipeline

    '''
    @brief Check if is there any error in the buses settings.
    @param in_bus_names List of the input buses names.
    @param out_bus_names List of the output buses names.
    '''
    def check_buses(self, in_bus_names: list, out_bus_names: list) -> bool:
        if len(in_bus_names) != len(self.in_formats) or len(out_bus_names) != len(self.out_formats):
            self.raise_fault('Number of input or output buses incompatible with the pipe')
        
        for i in range(len(in_bus_names)):
            if self.in_formats[i] not in bus_compatibility[self.parent_pipeline.buses[in_bus_names[i]].format]:
                self.raise_fault('Input buses formats incompatible with the pipe')
        
        for i in range(len(out_bus_names)):
            if self.out_formats[i] not in bus_compatibility[self.parent_pipeline.buses[out_bus_names[i]].format]:
                self.raise_fault('Output buses formats incompatible with the pipe')


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
                if fit_tuple(output_list[i].shape,1,3)[2] != 1:
                    raise Exception(str(self.name) + ' PIPE FAULT: Pipe.callback returning invalid data format. Internal error.')
            elif self.out_formats[i] != BusFormat.Universal:
                if fit_tuple(output_list[i].shape,1,3)[2] != 3:
                    raise Exception(str(self.name) + ' PIPE FAULT: Pipe.callback returning invalid data format. Internal error.')

            #Send data to bus
            self.parent_pipeline.buses[out_bus_names[i]].set_data(output_list[i])
        
    '''
    @brief Method that will be called to apply the filtering. It must be overwrited.
    @param input List of input images
    @return List of output images
    '''
    def callback(self, input: list) -> list:
        self.raise_fault('It is not possible to use the Pipe class without overwriting callback')
        return []

    def raise_fault(self, msg: str):
        raise Exception(str(self.name) + ' PIPE FAULT: ' + msg)


'''
@brief A Pipe that does nothing, just transports the image between two buses.
'''
class BypassPipe(Pipe):
    def __init__(self):
        super(BypassPipe, self).__init__([BusFormat.Universal], [BusFormat.Universal])

    def callback(self, input: list) -> list:
        return input


'''
@brief The pipeline is a graph of pipes separated by layers and interconnected by buses.

The image must be inserted into an input bus. When processing is done, this image will be
processed by a pipe circuit and the final result will be deposited on an output bus.
'''
class Pipeline(object):
    def __init__(self):
        self.buses = {} #format: {'bus_name': bus_object, ...}
        self.pipes = {} #format: {'pipe_name': pipe_object, ...}
        self.pipe_inputs = {} #format: {'pipe_name': ['bus0', 'bus1',...], ...}
        self.pipe_outputs = {} #format: {'pipe_name': ['bus0', 'bus1',...], ...}
        self.layers = {} #format: {layer_index: ['pipe_name0', 'pipe_name1',...], ...}
        self.sequence = [] #format: [layer_index0, layer_index1, layer_index2, ...]

    '''
    @brief Create a new bus in the pipeline.
    @param name Unique name across the pipeline for the bus
    @param format BusFormat of the bus
    '''
    def create_bus(self, name: str, format: BusFormat):
        if type(name) != str:
            raise Exception('PIPELINE FAULT on create_bus call: name argument is not str: name=' + str(name))
        
        if name not in self.buses:
            new_bus = Bus(name, format)
            self.buses[name] = new_bus
        else:
            raise Exception('PIPELINE FAULT on create_bus call: There is already a bus with the name ' + name)
             
    '''
    @brief Set an existing layer for the pipe.
    @param name Name of the existing pipe
    @param layer Name or index of the layer (if it does not already exist in the pipeline, it will be created).
    '''
    def set_pipe_layer(self, name: str, layer):
        if name not in self.pipes:
            raise Exception('PIPELINE FAULT on set_pipe_layer call: pipe ' + str(name) + ' not found')

        if layer not in self.layers:
            self.layers[layer] = []

        self.layers[layer].append(name)

    '''
    @brief Insert a Pipe object in the pipeline
    @param name Unique name across the pipeline for the Pipe
    @param pipe Pipe object
    @param input_buses List of names of input buses
    @parem output_buses List of names of output buses
    '''
    def insert_pipe(self, name: str, pipe: Pipe, input_buses: list, output_buses: list):
        if type(name) != str:
            raise Exception('PIPELINE FAULT on insert_pipe call: name argument is not str: name=' + str(name))

        if not isinstance(pipe, Pipe):
            raise Exception('PIPELINE FAULT on insert_pipe call: pipe argument is not Pipe: pipe=' + str(pipe))

        if name not in self.pipes:
            pipe.name = name
            pipe.set_parent(self)
            self.pipes[name] = pipe
            self.pipe_inputs[name] = input_buses
            self.pipe_outputs[name] = output_buses
        else:
            raise Exception('PIPELINE FAULT on insert_pipe call: There is already a pipe with the name ' + name)

    '''
    @brief Define the order witch the layers will be processed.
    @param sequence Tuple or list of layers names in order of the first to the last that will be processed.
    '''
    def set_layers_sequence(self, sequence: tuple):
        for i in sequence:
            if i not in self.layers:
                raise Exception('PIPELINE FAULT on set_layers_sequence call: Undefined layer: ' + str(i))

        self.sequence = sequence

    '''
    @brief Removes images from all buses and prepares the pipeline for further processing.
    '''
    def reset_buses(self):
        for bus_name in self.buses:
            bus = self.buses[bus_name]
            bus.reset()

    '''
    @brief Run the sequential processing of the pipes.
    '''
    def process(self):
        for layer in self.sequence:
            for pipe_name in self.layers[layer]:
                current_pipe = self.pipes[pipe_name]
                current_pipe.process(self.pipe_inputs[pipe_name], self.pipe_outputs[pipe_name])