# -*- coding: utf-8 -*-


import acoular as ac
import numpy as np
import matplotlib.pyplot as plot

fs = 44100 # Sample frequency
tr = ac.Trajectory() #Trajectory
tmax = 1 # Max time
v = 10 # Velocity
f = 2000 # Source frequency tonal

##############################################################################

tr.points[0] = (-(tmax/2)*v,1,5) # initial point, heigth, distance to the array
tr.points[tmax] = ((tmax/2)*v,1,5) # final point, heigth, distance to the array

##############################################################################
# Creating the array
x = np.array((0.10,0.05,0.00,-0.05,-0.10,-0.05,0.00,0.05,0.15,-0.05,-0.25,
 -0.30,-0.15,0.05,0.25,0.30,0.10,-0.20,-0.40,-0.35,-0.10,0.20,0.40,0.35
 ,0.05,-0.35,-0.50,-0.40,-0.05,0.35,0.50,0.40))

y = np.array((0,0.05 ,0.10,0.05,0.00,-0.05,-0.10,-0.05,0.25,0.30,0.15,-0.05,-0.25,-0.30,-0.15,0.05,0.40,0.35,0.10,-0.20,-0.40,-0.35,-0.10,0.20,0.50,0.40,0.05,-0.35,-0.50,-0.40,-0.05,0.35))
y = y +1.2
z = np.zeros(32)
m = ac.MicGeom()
m.mpos_tot = np.array((x,y,z))

##############################################################################
# Source generator

long= int

s0 = ac.SineGenerator(sample_freq=fs, numsamples=long(fs*tmax), freq=f, \
    phase=np.pi)

p0 = ac.MovingPointSource(signal=s0, mics=m, trajectory=tr)

#

t = p0

# Saving 32 channel wav

# ww = ac.WriteWAV(source = t)
# ww.channels = [0,32]
# ww.save

##############################################################################

fi = ac.FiltFiltOctave(source=t, band=f, fraction='Third octave')
g = ac.RectGrid(x_min=-2.0, x_max=+2.0, y_min=0.0, y_max=+4.0, z=0, \
    increment=0.2)# grid point of origin is at trajectory (thus z=0)
st = ac.SteeringVector(grid=g, mics=m)
# beamforming with trajectory (rvec axis perpendicular to trajectory)
bts = ac.BeamformerTimeSqTraj(source=fi, steer=st, trajectory=tr, \
    rvec = np.array((0,0,1.0)))
avgts = ac.TimeAverage(source=bts, naverage=int(fs*tmax/2))

##############################################################################
    
cacht = ac.TimeCache(source=avgts) 
map1 = np.zeros(g.shape)


plot.figure(2,(8,7))
i = 1
for res in cacht.result(1):
    res0 = res[0].reshape(g.shape)
    map1 += res0 # average
    i += 1  
    plot.subplot(4,4,i)
    mx = ac.L_p(res0.max())
    plot.imshow(ac.L_p(np.transpose(res0)), vmax=mx, vmin=mx-10, interpolation='nearest',\
        extent=g.extend(), origin='lower')
    plot.colorbar()
map1 /= i


    
##############################################################################