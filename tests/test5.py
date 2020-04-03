'''
TEST SCRIPT FOR TRIPLE ADDITION
By Filipe Chagas
'''

import sys
sys.path.append('../src')
sys.path.append('../src/plugins')

import pipeline as pl
import addition as add
import numpy as np
import random as rd

#pipeline
my_pipeline = pl.Pipeline()

#buses
my_pipeline.create_bus('input', pl.BusFormat.Triple)
my_pipeline.create_bus('output', pl.BusFormat.Triple)

#pipes
my_add = add.AdditionPipe()

#params
#my_add.set_param('value', 10)
my_add.set_param('clipping', True)

#build
my_pipeline.insert_pipe('my_add', my_add, ['input'], ['output'])
my_pipeline.set_pipe_layer('my_add', 0)

my_pipeline.set_layers_sequence([0])

#test
if __name__ == '__main__':
    for n in range(100):
        print('TEST ' + str(n)) 
        
        #input data
        in_data = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500), 3)*255, np.uint8)
        print('input')
        print(in_data)

        #add value
        addv = rd.randint(0,255)
        my_add.set_param('value', addv)

        #expected output
        expected_out = add.AdditionPipe.clip(in_data.astype(np.float) + addv).astype(np.uint8)
        print('expected out')
        print(expected_out)

        #process and get output
        my_pipeline.buses['input'].set_data(in_data)
        my_pipeline.process()
        out_data = my_pipeline.buses['output'].get_data()

        print('out')
        print(out_data)

        #check
        ans = (out_data == expected_out)

        if isinstance(ans, bool):
            if ans == True:
                print('SUCCESS')
            else:
                print('FAILURE')
                break
        else:
            if ans.all() == True:
                print('SUCCESS')
            else:
                print('FAILURE')
                break 
        
        my_pipeline.reset_buses()

        