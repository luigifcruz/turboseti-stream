r""" Test with synthetic data"""

import logging
from spectra_gen.spectra_gen_config import ConfigObject
from main import DopplerFinder


INFILE = "/tmp/spectra.fil"
MAX_DRIFT_RATE = 10.0


#-------------------------------------------------
# Be sure to run spectra_gen_main.py first:
#-------------------------------------------------
# cd spectra_gen
# python3  spectra_gen_main.py  INFILE
#-------------------------------------------------
# Replace "/tmp/spectra.npy" with whatever path is suitable.
#-------------------------------------------------

cfg = ConfigObject("spectra_gen/spectra_gen.cfg")

# Define observation parameters
n_fine_chans = cfg.fchans # setigen fchans
f_start = cfg.fch1 # MHz, setigen fch1
foff = cfg.df # MHz,        setigen df
f_stop = f_start + (n_fine_chans - 1) * foff # MHz
ntime = cfg.n_ints_in_file # seconds,     setigen tchans
tsamp = cfg.dt # seconds,      setigen dt

mjd = 59423.2


print("Clancy is being initialised")
clancy = DopplerFinder(filename="CH0_TIMESTAMP.h5",
                       source_name="SYNTHETIC",
                       max_drift=MAX_DRIFT_RATE,
                       log_level_int=logging.INFO,
                       src_raj=7.456805,
                       src_dej=5.225785,
                       tstart=mjd,
                       tsamp=tsamp,
                       f_start=f_start,
                       f_stop=f_stop,
                       n_fine_chans=n_fine_chans,
                       n_ints_in_file=ntime)

print("Clancy is searching for ET")
clancy.find_ET_from_file(INFILE)
