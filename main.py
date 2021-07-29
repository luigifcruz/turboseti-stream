import os
import logging
import numpy as np
from pkg_resources import resource_filename

from turbo_seti.find_doppler.kernels import *
import turbo_seti.find_doppler.find_doppler as fd

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

class DataLoader():

    def __init__(self, data_obj, drift_indices):
        self.drift_indices = drift_indices
        self.data_obj = data_obj
        print("turboseti-stream DataLoader __init__: data_obj:", self.data_obj)

    def load(self, spectra):
        self.spectra = spectra
        print("turboseti-stream DataLoader load: spectra shape:", self.spectra.shape)

    def load_npy_file(self, spectra_file_path):
        self.spectra = np.load(spectra_file_path)
        print("turboseti-stream DataLoader load_npy_file: spectra shape:", self.spectra.shape)

    def get(self):
        return (self.data_obj, self.spectra, self.drift_indices)

class DopplerFinder():

    def __init__(self, filename, source_name, src_raj, src_dej, tstart, tsamp, f_start, f_stop, n_fine_chans, n_ints_in_file,
                 coarse_chan_num=0, n_coarse_chan=1, min_drift=0.00001, max_drift=4.0, snr=25.0, out_dir='./',
                 flagging=False, obs_info=None, append_output=False, blank_dc=True,
                 kernels=None, gpu_backend=False, precision=1, gpu_id=0):

        if not kernels:
            self.kernels = Kernels(gpu_backend, precision, gpu_id)
        else:
            self.kernels = kernels

        if obs_info is None:
            obs_info = {'pulsar': 0, 'pulsar_found': 0, 'pulsar_dm': 0.0, 'pulsar_snr': 0.0,
                        'pulsar_stats': self.kernels.np.zeros(6), 'RFI_level': 0.0, 'Mean_SEFD': 0.0, 'psrflux_Sens': 0.0,
                        'SEFDs_val': [0.0], 'SEFDs_freq': [0.0], 'SEFDs_freq_up': [0.0]}

        fftlen = n_fine_chans
        shoulder_size = 0
        tsteps = n_ints_in_file

        # Data Object Header
        self.header = Map({
            "coarse_chan": 0, # Coarse channel number, NOT the same as n_coarse_chan == the amount of coarse channels?
            "obs_length": n_ints_in_file * tsamp,
            "DELTAF": (f_stop - f_start) / n_fine_chans * 1e-6,
            "NAXIS1": fftlen,
            "FCNTR": ((f_stop + f_start) / 2) * 1e-6, # 1/2 way pt between the lowest and highest fine channel frequency
            "baryv": 0, # Never used anywhere
            "SOURCE": source_name, # ATA Track Scan takes source name/id OR ra/dec OR az/el
            "MJD": tstart, # Observation start time, from ATA block
            "RA": src_raj,
            "DEC": src_dej,
            "DELTAT": tsamp, # Time step in seconds
            "max_drift_rate": max_drift,
        })

        # Data Loader
        self.find_doppler_instance = Map({
            "data_handle": Map({
                "filename": filename,
                "header": self.header
            }),
            "log_level_int": logging.INFO,
            "min_drift": min_drift,
            "max_drift": max_drift,
            "out_dir": out_dir,
            "snr": snr,
            "status": True,
            "flagging": flagging,
            "obs_info": obs_info,
            "append_output": append_output,
            "flag_blank_dc": blank_dc,
            "n_coarse_chan": n_coarse_chan,
            "kernels": self.kernels,
        })

        # Data Object
        self.data_dict = Map({
            "f_start": f_start,
            "f_stop": f_stop,
            "tsteps": n_ints_in_file,
            "tsteps_valid": n_ints_in_file,
            "tdwidth": int(fftlen + shoulder_size * tsteps),
            "fftlen": n_fine_chans // n_coarse_chan,
            "shoulder_size": shoulder_size,
            "drift_rate_resolution": (1e6 * np.abs(self.header['DELTAF'])) / self.header['obs_length'],
            "coarse_chan": coarse_chan_num,
            "header": self.header
        })

        # Create Custom Data Loader
        dia_num = int(np.log2(self.data_dict.tsteps))
        file_path = resource_filename('turbo_seti', f'/drift_indexes/drift_indexes_array_{dia_num}.txt')

        if not os.path.isfile(file_path):
            raise ValueError(":(")

        di_array = np.array(np.genfromtxt(file_path, delimiter=' ', dtype=int))

        ts2 = int(self.data_dict.tsteps/2)
        drift_indexes = di_array[(self.data_dict.tsteps_valid - 1 - ts2), 0:self.data_dict.tsteps_valid]

        self.dataloader = DataLoader(self.data_dict, drift_indexes)

    def find_ET(self, spectra):
        self.dataloader.load(spectra)
        fd.search_coarse_channel(self.data_dict, self.find_doppler_instance, dataloader=self.dataloader)

        
    def find_ET_from_synth(self, spectra_file_path):
        self.dataloader.load_npy_file(spectra_file_path)
        fd.search_coarse_channel(self.data_dict, self.find_doppler_instance, dataloader=self.dataloader)

        
# Example usage:
# clancy = DopplerFinder(filename="CH0_TIMESTAMP", source_name="luyten", src_raj=7.456805, src_dej=5.225785, 
#                        tstart=0, tsamp=1, f_start=0, f_stop=1, n_fine_chans=1, n_ints_in_file=16)
# clancy.find_ET(np.zeros((256)))
# clancy.find_ET_from_synth("/path-to-synthetic-gnu-radio-data.npy")
