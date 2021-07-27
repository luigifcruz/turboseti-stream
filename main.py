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

    def load(self, spectra):
        self.spectra = spectra

    def get(self):
        return (self.data_obj, self.spectra, self.drift_indices)

class FindDoppler():

    def __init__(self, filename, f_start, f_stop,
                 tsteps, tsteps_valid, tdwidth, fftlen, shoulder_size, drift_rate_resolution,
                 max_drift=4.0, min_drift=0.00001, snr=25.0, out_dir='./', obs_info=None, flagging=False,
                 n_coarse_chan=1, append_output=False, blank_dc=True, gpu_id=0, precision=1, kernels=None,
                 gpu_backend=False, log_level_int=logging.INFO):

        if not kernels:
            self.kernels = Kernels(gpu_backend, precision, gpu_id)
        else:
            self.kernels = kernels

        # Data Object Header
        self.header = Map({
            "coarse_chan": 1,
            "obs_length": 0,
            "DELTAF": 0,
            "NAXIS1": 0,
            "FCNTR": 0,
            "baryv": 0,
            "SOURCE": 0,
            "MJD": 0,
            "RA": 0,
            "DEC": 0,
            "DELTAT": 0,
            "max_drift_rate": max_drift,
        })

        # Data Loader
        self.find_doppler_instance = Map({
            "data_handle": Map({
                "filename": filename,
                "header": self.header
            }),
            "log_level_int": log_level_int,
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
            "tsteps": tsteps,
            "tsteps_valid": tsteps_valid,
            "tdwidth": tdwidth,
            "fftlen": fftlen,
            "shoulder_size": shoulder_size,
            "drift_rate_resolution": drift_rate_resolution,
            "coarse_chan": 1,
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

    def search(self, spectra):
        self.dataloader.load(spectra)
        fd.search_coarse_channel(self.data_dict, self.find_doppler_instance, dataloader=self.dataloader)

find_doppler = FindDoppler("CH0_TIMESTAMP", 0.0, 1.0, 256, 1, 1, 1, 1, 1);
find_doppler.search(np.zeros((256)))
