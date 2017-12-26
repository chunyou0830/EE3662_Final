# MUST USE CONSOLE TO RUN!!
# >python test.py
import pyaudio
import wave
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import multiprocessing
import time

nthread = multiprocessing.cpu_count()

np.set_printoptions(precision=4)

# Global settings
chunk = 2048
fmt = "<" + "hh"*chunk

# Open file
WAVE_INPUT_FILE = 'Party_Animal.wav'
wf = wave.open(WAVE_INPUT_FILE, 'rb')
fs = wf.getframerate()

# Open audio stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = fs,
                output = True)

# Read initial chunk
data = wf.readframes(chunk)

# Unpack the audio bytes to short int
data_conv = wave.struct.unpack(fmt,data)
data_rfft = np.abs(np.fft.fft(data_conv[0::2]))

# Create plot image
fig, (axl, axr, axf) = plt.subplots(nrows=3, ncols=1)

# Create initial line
linel, = axl.plot(np.arange(chunk), data_conv[0::2])
liner, = axr.plot(np.arange(chunk), data_conv[1::2])

# Create FFT initial line
N = len(data_conv[0::2])
T = fs
xf = np.fft.fftfreq(data_rfft.size)
linef, = axf.plot(xf*fs, data_rfft)

# Resize the y axis
axl.set_ylim(-32767, 32768)
axl.figure.canvas.draw()
axr.set_ylim(-32767, 32768)
axr.figure.canvas.draw()
axf.set_ylim(0, 20000000)
axf.figure.canvas.draw()

# Resize the x axis
axf.set_xscale('log')
axf.set_xlim(0, 5000)

# Add title
axl.set_title("Left Channel")
axr.set_title("Right Channel")

# Adjust plot layout
plt.tight_layout()

# Initial light data
lights_data = []

def animate(i):
    start = time.time()
    
    # Read chunk
    data = wf.readframes(chunk)
    
    # Unpack the audio bytes to short int
    data_conv = wave.struct.unpack(fmt,data)
    data_rfft = np.abs(np.fft.fft(data_conv[0::2]))
    
    # Set line data to the left channel audio data
    linel.set_ydata(data_conv[0::2])
    liner.set_ydata(data_conv[1::2])
    linef.set_ydata(data_rfft)
    
    # Print calculate latency bar
    #print("*"*(int((time.time() - start)/0.0001)))
    
    # Print volume bar
    #print('*'*int(np.sum(data_rfft)/5000000))
    
    # Calculate LED energy
    light = np.zeros(5)
    light[0] = np.sum(data_rfft[0:399])/np.sum(data_rfft[0:1999])*255
    light[1] = np.sum(data_rfft[400:799])/np.sum(data_rfft[0:1999])*255
    light[2] = np.sum(data_rfft[800:1199])/np.sum(data_rfft[0:1999])*255
    light[3] = np.sum(data_rfft[1200:1599])/np.sum(data_rfft[0:1999])*255
    light[4] = np.sum(data_rfft[1600:1999])/np.sum(data_rfft[0:1999])*255
    lights_data.append(light)
    print("*"*int(light[0]))
    print("*"*int(light[1]))
    print("*"*int(light[2]))
    print("*"*int(light[3]))
    print("*"*int(light[4]))
    print("-"*30)
    
    # Play chunk data
    stream.write(data)
    return

# Create animation plot function
ani = animation.FuncAnimation(fig=fig,func=animate,interval=10,blit=False)

# Start plot
plt.show()

# Close the stream and file
stream.close()
p.terminate()
