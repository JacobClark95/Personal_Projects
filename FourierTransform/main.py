
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import IPython
from scipy.fftpack import fft
import time

class SoundWave(object):
    """A class for working with digital audio signals."""

    # Problem 1.1
    def __init__(self, rate, samples):
        """Set the SoundWave class attributes.

        Parameters:
            rate (int): The sample rate of the sound.
            samples ((n,) ndarray): NumPy array of samples.
        """
        self.rate = rate
        self.samples = samples
        

    # Problems 1.1 and 1.7
    def plot(self, show_frequencies = False):
        """Plot the graph of the sound wave (time versus amplitude)."""
        time = len(self.samples) / self.rate
        x_axis = np.linspace(0, time, len(self.samples))
        
        
        if show_frequencies:
            
            frequencies = np.array(list(range(len(self.samples)))) / time
            c = fft(self.samples)
            
            plt.figure(1)
            plt.subplot(2,1,1)
            plt.plot(x_axis, self.samples)
            plt.ylim(-32768, 32767)
            plt.title("Sound")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Samples")
            
            plt.subplot(2,1,2)
            plt.title("Frequencies")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Intensity")
            plt.plot(frequencies, c)
            
            plt.show()
        
        else:
            plt.figure(1)
            plt.plot(x_axis, self.samples)
            plt.ylim(-32768, 32767)
            plt.title("Sound")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Samples")
            plt.show()
        
        

    # Problem 1.2
    def export(self, filename, force=False):
        """Generate a wav file from the sample rate and samples. 
        If the array of samples is not of type np.int16, scale it before exporting.

        Parameters:
            filename (str): The name of the wav file to export the sound to.
        """
        if type(self.samples) != np.int16:
            force = True
        
        audio = self.samples
        if force == True:
            audio = np.int16((self.samples * 32767) / np.max(self.samples))
        
        wavfile.write(filename, self.rate, audio)
    
    # Problem 1.4
    def __add__(self, other):
        """Combine the samples from two SoundWave objects.

        Parameters:
            other (SoundWave): An object containing the samples to add
                to the samples contained in this object.
        
        Returns:
            (SoundWave): A new SoundWave instance with the combined samples.

        Raises:
            ValueError: if the two sample arrays are not the same length.
        """
        raise NotImplementedError("Problem 1.4 Incomplete")

    # Problem 1.4
    def __rshift__(self, other):
        """Concatentate the samples from two SoundWave objects.

        Parameters:
            other (SoundWave): An object containing the samples to concatenate
                to the samples contained in this object.

        Raises:
            ValueError: if the two sample rates are not equal.
        """
        raise NotImplementedError("Problem 1.4 Incomplete")
    
    # Problem 2.1
    def __mul__(self, other):
        """Convolve the samples from two SoundWave objects using circular convolution.
        
        Parameters:
            other (SoundWave): An object containing the samples to convolve
                with the samples contained in this object.
        
        Returns:
            (SoundWave): A new SoundWave instance with the convolved samples.

        Raises:
            ValueError: if the two sample rates are not equal.
        """
        raise NotImplementedError("Problem 2.1 Incomplete")

    # Problem 2.2
    def __pow__(self, other):
        """Convolve the samples from two SoundWave objects using linear convolution.
        
        Parameters:
            other (SoundWave): An object containing the samples to convolve
                with the samples contained in this object.
        
        Returns:
            (SoundWave): A new SoundWave instance with the convolved samples.

        Raises:
            ValueError: if the two sample rates are not equal.
        """
        raise NotImplementedError("Problem 2.2 Incomplete")

    # Problem 2.4
    def clean(self, low_freq, high_freq):
        """Remove a range of frequencies from the samples using the DFT. 

        Parameters:
            low_freq (float): Lower bound of the frequency range to zero out.
            high_freq (float): Higher boound of the frequency range to zero out.
        """
        raise NotImplementedError("Problem 2.4 Incomplete")






rate, samples = wavfile.read("note_A.wav")
A = SoundWave(rate, samples)
A.plot(True)



