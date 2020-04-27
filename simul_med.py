# -*- coding: utf-8 -*-


import acoular as ac
import numpy as np
from matplotlib.pyplot import plot

fs = 44100 # Sample frequency
tr = ac.Trajectory()
tmax = 10 # Max time
t = np.linspace(0,tmax,tmax*(fs)) # Time instants
v = 10 # Velocity
for i in range(0,tmax,tmax*fs):
     tr.points[i] =(t[i]*v,1,8) # Distance = time x velocity

# Creating the array
x = np.array((0.10,0.05,0.00,-0.05,-0.10,-0.05,0.00,0.05,0.15,-0.05,-0.25,
 -0.30,-0.15,0.05,0.25,0.30,0.10,-0.20,-0.40,-0.35,-0.10,0.20,0.40,0.35
 ,0.05,-0.35,-0.50,-0.40,-0.05,0.35,0.50,0.40))

y = np.array((0,0.05 ,0.10,0.05,0.00,-0.05,-0.10,-0.05,0.25,0.30,0.15,-0.05,-0.25,-0.30,-0.15,0.05,0.40,0.35,0.10,-0.20,-0.40,-0.35,-0.10,0.20,0.50,0.40,0.05,-0.35,-0.50,-0.40,-0.05,0.35))
y = y +1.2
z = np.zeros(32)
m = ac.MicGeom()
m.mpos_tot = np.array((x,y,z))

# Source generator

long= int

s2 = ac.SineGenerator(sample_freq=fs, numsamples=long(fs*tmax), freq=1000, \
    phase=np.pi)

p0 = ac.MovingPointSource(signal=s2, mics=m, trajectory=tr)

#

t = p0

# Saving 32 channel wav

ww = ac.WriteWAV(source = t)
ww.channels = [0,32]
ww.save


