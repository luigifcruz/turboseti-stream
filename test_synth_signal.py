r""" Test with synthetic data"""

NUMPY_PATH = "/tmp/spectra.npy"

#-------------------------------------------------
# Be sure to run spectra_gen_main.py first:
#-------------------------------------------------
# cd spectra_gen
# python3  spectra_gen_main.py  NUMPY_PATH
#-------------------------------------------------
# Replace "/tmp/spectra.npy" with whatever path is suitable.
#-------------------------------------------------

#import matplotlib.pyplot as plt

from main import DopplerFinder

# Define observation parameters
n_fine_chans = int(4e6) # setigen fchans
ntime = 60 # seconds,     setigen tchans
f_start = 8437.625 # MHz, setigen fch1
foff = 1e-6 # MHz,        setigen df
f_stop = f_start + (n_fine_chans - 1) * foff # MHz
tsamp = 1 # seconds,      setigen dt

mjd = 59423.2


print("Clancy is being initialised")
clancy = DopplerFinder(filename="CH0_TIMESTAMP.h5",
                       source_name="SYNTHETIC",
                       src_raj=7.456805,
                       src_dej=5.225785,
                       tstart=mjd,
                       tsamp=tsamp,
                       f_start=f_start,
                       f_stop=f_stop,
                       n_fine_chans=n_fine_chans,
                       n_ints_in_file=ntime)

print("Clancy is searching for ET")
clancy.find_ET_from_synth(NUMPY_PATH)
