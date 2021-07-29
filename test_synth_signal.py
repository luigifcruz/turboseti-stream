r""" Test with synthetic data"""

#import matplotlib.pyplot as plt

from main import DopplerFinder

# Define observation parameters
f_start = 3e9  #Hz
BW = 1e6 #Hz
tsamp=1 #seconds
f_stop = f_start + BW
n_fine_chans = int(1e6)
ntime = int(64)
mjd=59423.2


print("Clancy's being initialised")
clancy = DopplerFinder(filename="CH0_TIMESTAMP",
                       source_name="test",
                       src_raj=7.456805,
                       src_dej=5.225785,
                       tstart=mjd,
                       tsamp=tsamp,
                       f_start=f_start,
                       f_stop=f_stop,
                       n_fine_chans=n_fine_chans,
                       n_ints_in_file=ntime)

print("Clancy's searching for ET")
clancy.find_ET_from_synth("/tmp/spectra.npy")
