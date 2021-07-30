r"""
Data definitions for spectra_gen_main.py
"""

from astropy import units as u


VERSION = "1.0"
DEBUGGING = False


class SetigenParms:
    r"""Object definition for setigen parameters"""

    def __init__(self):

        # Parameters for all signals
        self.fchans = int(4e6) # number of (fine) channels
        self.tchans = 64 # number of time samples
        self.df = 1.0 * u.Hz # fine channel width in Hz
        self.dt = 1.0 * u.s #sampling time in seconds
        self.fch1 = 8437.625 * u.MHz # Starting frequency in MHz
        self.adding_noise = True # Add noise?
        self.noise_std = 0.05 # Gaussian standard deviation
        self.ascending = True # Ascending frequencies?

        # Signal 1 parameters
        self.signal_start_1 = self.fchans / 5 # index to frequency columns
        self.drift_rate_1 = 1.3 * u.Hz/u.s # drift rate to inject
        self.width_1 = 1.0 * u.Hz # signal width in Hz
        self.snr_1 = 100.0 # SNR which will determine setigen intensity level

        # Signal  2 parameters
        self.signal_start_2 = 4 * self.fchans / 5
        self.drift_rate_2 = -2.6 * u.Hz/u.s
        self.width_2 = 2.0 * u.Hz
        self.snr_2 = 200.0

        # Signal 3 parameters
        self.signal_start_3 = self.fchans / 3
        self.drift_rate_3 = 3.9 * u.Hz/u.s
        self.width_3 = 3.0 * u.Hz
        self.snr_3 = 300.0
