# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:59:53 2020

@author: Lucas Muller Gomes 
Acoustic Engineegiring - UFSM

"""
import tables
import numpy
import acoular

N_channels = # Number of channels
fs = # Sample rating
data = # data to save in the hdf5 - the shape must be (num_samples, number of channels)
data = numpy.array(data)
savename = "DataToAcoular.h5"

acoularh5 = tables.open_file(savename, mode = "w", title = savename)
acoularh5.create_earray('/','time_data', atom=None, title='', filters=None, expectedrows=100000, chunkshape=[256,N_channels], \
                         byteorder=None, createparents=False, obj=data)
acoularh5.set_node_attr('/time_data','sample_freq', fs)
acoularh5.close()

# Acoular data

ts=acoular.TimeSamples(name= savename)

