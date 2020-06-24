import acoular as ac
import numpy as np
import matplotlib.pyplot as plot

fs = 44100 # Sample frequency [hz]
tr0 = ac.Trajectory() #Trajectory
tr1 = ac.Trajectory() #Trajectory
tr_beam = ac.Trajectory()
tmax = 0.1 # Max time [s]
v = 15 # Velocity [m/s]
f = 3000 # Source frequency tonal [hz]

##############################################################################

#source 0
tr0.points[0] = (-(tmax/2)*v,1,5) # initial point, heigth, distance to the array
tr0.points[tmax] = ((tmax/2)*v,1,5) # final point, heigth, distance to the array

#source 1
tr1.points[0] = (-(tmax/2)*v -1 ,1.5,5) # initial point, heigth, distance to the array
tr1.points[tmax] = ((tmax/2)*v - 1,1.5,5) # final point, heigth, distance to the array

# moving grid
tr_beam.points[0] = (-(tmax/2)*v,0,5) # initial point, heigth, distance to the array of the moving grid
tr_beam.points[tmax] = ((tmax/2)*v,0,5) # final point, heigth, distance to the array of the moving grid


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

s1 = ac.SineGenerator(sample_freq=fs, numsamples=long(fs*tmax), freq=f, \
    phase=np.pi)

p0 = ac.MovingPointSource(signal=s0, mics=m, trajectory=tr0)

p1 = ac.MovingPointSource(signal=s1, mics=m, trajectory=tr1)

#

t = ac.Mixer(source = p0, sources = [p1,])

# Saving 32 channel wav

# ww = ac.WriteWAV(source = t)
# ww.channels = [0,32]
# ww.save

##################### Frequency beamforming fixed focus ######################

fi = ac.PowerSpectra(time_data=t, window='Hanning', overlap='50%', block_size=128, \
    ind_low=1,ind_high=15) # CSM calculation 
g = ac.RectGrid(x_min=-2, x_max=+2, y_min=0, y_max=+4, z=5, increment=0.1)

st = ac.SteeringVector(grid=g, mics=m)
b = ac.BeamformerBase(freq_data=fi, steer=st)
map1 = b.synthetic(f,3)

mx = ac.L_p(map1.max())
plot.figure()
plot.imshow(ac.L_p(np.transpose(map1)), vmax=mx, vmin=mx-5, interpolation='bilinear',\
        extent=g.extend(), origin='lower')
plot.colorbar()

##################### Time beamforming moving focus ##########################

fi = ac.FiltFiltOctave(source=t, band=f, fraction='Third octave')
g = ac.RectGrid(x_min=-2.0, x_max=+2.0, y_min=0.0, y_max=+4.0, z=0.0, \
    increment=0.1)# grid point of origin is at trajectory (thus z=0)
st = ac.SteeringVector(grid=g, mics=m)
# beamforming with trajectory (rvec axis perpendicular to trajectory)
bts = ac.BeamformerTimeSqTraj(source=fi, steer=st, trajectory=tr_beam, \
    rvec = np.array((0,0,0)))
avgts = ac.TimeAverage(source=bts, naverage=int(fs*tmax/2))
  
cacht = ac.TimeCache(source=avgts) 
cacht_data = cacht.result(int(cacht.numsamples))
data = next(cacht_data)

map1 = np.zeros(g.shape)
for i in range(data.shape[0]):
  map1 =+ np.reshape(data[i,:],g.shape)
  
mx = ac.L_p(map1.max())
plot.figure()
plot.imshow(ac.L_p(np.transpose(map1)), vmax=mx, vmin=mx-5, interpolation='bilinear',\
        extent=g.extend(), origin='lower')
plot.colorbar()