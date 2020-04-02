'''
TEST SCRIPT FOR CHANNEL FORK & BLEND
By Filipe Chagas
'''

import pipeline as pl
import _fork_blend as fb
import numpy as np
import random as rd

#pipeline
my_pipeline = pl.Pipeline()

#buses
my_pipeline.create_bus('input', pl.BusFormat.Channel)
my_pipeline.create_bus('c0', pl.BusFormat.Channel)
my_pipeline.create_bus('c1', pl.BusFormat.Channel)
my_pipeline.create_bus('c2', pl.BusFormat.Channel)
my_pipeline.create_bus('c3', pl.BusFormat.Channel)
my_pipeline.create_bus('output', pl.BusFormat.Channel)

#pipes
my_fork = fb.ChannelForkPipe()
my_blend = fb.ChannelBlendPipe()

#params
my_fork.set_param('number_of_outputs', 4)
my_blend.set_param('number_of_inputs', 4)

#build
my_pipeline.insert_pipe('my_fork', my_fork, ['input'], ['c0','c1','c2','c3'])
my_pipeline.set_pipe_layer('my_fork', 0)

my_pipeline.insert_pipe('my_blend', my_blend, ['c0','c1','c2','c3'], ['output'])
my_pipeline.set_pipe_layer('my_blend', 1)

my_pipeline.set_layers_sequence((0,1))

#test
tolerance = 1
if __name__ == '__main__':
    for n in range(1000):
        #random 4 weights
        curr_weights = [rd.random()*10 for x in [None]*4]
        w_sum = sum(curr_weights)

        my_blend.set_param('weights', curr_weights)

        print('TEST ' + str(n)) 
        
        #input data
        in_data = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500))*255, np.uint8)
        print('input')
        print(in_data)

        #expected output
        expected_out = np.array(sum([(in_data * w)/w_sum for w in curr_weights]), np.uint8)
        print('expected out')
        print(expected_out)

        #process and get output
        my_pipeline.buses['input'].set_data(in_data)
        my_pipeline.process()
        out_data = my_pipeline.buses['output'].get_data()

        print('out')
        print(out_data)

        #diference between expected out and real out
        diference = np.array(expected_out,np.float) - np.array(out_data, np.float)
        print('diference')
        print(diference)

        ans0 = (diference > tolerance) 
        ans1 = (diference < tolerance)

        if (not ans0.all()) or (not ans1.all()):
            print('SUCCESS')
        else:
            print('FAILURE')
            break

        my_pipeline.reset_buses()

        