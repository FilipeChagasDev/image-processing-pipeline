'''
TEST SCRIPT FOR TRIPLE HADAMARD WITH MASK UNIFORM NORMALIZATION AND CLIPPING
By Filipe Chagas
'''

import sys
sys.path.append('../src')
sys.path.append('../src/plugins')

import pipeline as pl
import hadamard as hd
import numpy as np
import random as rd
import cv2 as cv

#pipeline
my_pipeline = pl.Pipeline()

#buses
my_pipeline.create_bus('input', pl.BusFormat.Triple)
my_pipeline.create_bus('mask', pl.BusFormat.Triple)
my_pipeline.create_bus('output', pl.BusFormat.Triple)

#pipes
my_had = hd.TripleHadamardPipe()

#params
my_had.set_param('normalize_mask', True)
my_had.set_param('uniform_normalization', True)
my_had.set_param('clipping', True)

#build
my_pipeline.insert_pipe('my_had', my_had, ['input', 'mask'], ['output'])
my_pipeline.set_pipe_layer('my_had', 0)

my_pipeline.set_layers_sequence([0])

#test
tolerance = 1
clip = np.vectorize(lambda x : 255 if x > 255 else (0 if x < 0 else (x)))

if __name__ == '__main__':
    for n in range(100):
        print('TEST ' + str(n)) 
        
        #input data
        in_data = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500), 3)*255, np.uint8)
        print('input')
        print(in_data)

        #expected output
        mask = np.array(np.random.rand(rd.randint(1,500),rd.randint(1,500), 3)*255, np.uint8)
        mask_rs = cv.resize(mask, (in_data.shape[1], in_data.shape[0])).astype(np.float)
        mask_unorm = mask_rs / np.max(mask_rs)

        expected_out = clip(in_data.astype(np.float) *  mask_unorm)
        expected_out = expected_out.astype(np.uint8)
        
        print('expected out')
        print(expected_out)

        #process and get output
        my_pipeline.buses['input'].set_data(in_data)
        my_pipeline.buses['mask'].set_data(mask)
        my_pipeline.process()
        out_data = my_pipeline.buses['output'].get_data()

        print('out')
        print(out_data)

        #check
        diference = out_data - expected_out
        ans0 = (diference > tolerance)
        ans1 = (diference < tolerance)
        
        if (not ans0.all()) or (not ans1.all()):
            print('SUCCESS')
        else:
            print('FAILURE')
            break

        my_pipeline.reset_buses()

        