'''
TEST SCRIPT FOR SPLIT & MERGE
By Filipe Chagas
'''

import sys
sys.path.append('../src')
sys.path.append('../src/plugins')

import pipeline as pl
import split_merge as sm
import numpy as np
import random as rd

#pipeline
my_pipeline = pl.Pipeline()

#buses
my_pipeline.create_bus('input', pl.BusFormat.Triple)
my_pipeline.create_bus('c0', pl.BusFormat.Channel)
my_pipeline.create_bus('c1', pl.BusFormat.Channel)
my_pipeline.create_bus('c2', pl.BusFormat.Channel)
my_pipeline.create_bus('output', pl.BusFormat.Triple)

#pipes
my_split = sm.SplitPipe()
my_merge = sm.MergePipe()

my_pipeline.insert_pipe('my_split', my_split, ['input'], ['c0','c1','c2'])
my_pipeline.set_pipe_layer('my_split', 0)

my_pipeline.insert_pipe('my_merge', my_merge, ['c0','c1','c2'], ['output'])
my_pipeline.set_pipe_layer('my_merge', 1)

my_pipeline.set_layers_sequence((0,1))

if __name__ == '__main__':
    for n in range(100):
        print('TEST ' + str(n)) 
        
        #random input
        in_data = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500), 3)*255, np.uint8)
        print(in_data)

        #process and get out
        my_pipeline.buses['input'].set_data(in_data)
        my_pipeline.process()
        out_data = my_pipeline.buses['output'].get_data()

        print(out_data)

        #output must be equal to input
        ans = (in_data == out_data) 
        if not isinstance(ans, bool):
            if ans.all():
                print('Success!')
            else:
                print('FAILURE')
                break
        else:
            if ans:
                print('Success!')
            else:
                print('FAILURE')
                break

        my_pipeline.reset_buses()