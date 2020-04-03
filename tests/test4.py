'''
TEST SCRIPT FOR CHANNEL PRODUCT
By Filipe Chagas
'''

import sys
sys.path.append('../src')
sys.path.append('../src/plugins')

import pipeline as pl
import product as prod
import numpy as np
import random as rd

#pipeline
my_pipeline = pl.Pipeline()

#buses
my_pipeline.create_bus('input', pl.BusFormat.Channel)
my_pipeline.create_bus('output', pl.BusFormat.Channel)

#pipes
my_prod = prod.ProductPipe()

#params

#build
my_pipeline.insert_pipe('my_prod', my_prod, ['input'], ['output'])
my_pipeline.set_pipe_layer('my_prod', 0)

my_pipeline.set_layers_sequence([0])

#test
if __name__ == '__main__':
    for n in range(100):
        print('TEST ' + str(n)) 
        
        #input data
        in_data = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500))*255, np.uint8)
        print('input')
        print(in_data)

        #add value
        pv = float(rd.randint(0,255))
        po = float(rd.randint(0,255))
        my_prod.set_param('value', pv)
        my_prod.set_param('offset', po)

        #expected output
        expected_out = prod.ProductPipe.clip((in_data.astype(np.float) - po)*pv + po).astype(np.uint8)
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

        