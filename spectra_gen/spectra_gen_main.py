r"""
Main program for generating synthetic Gnu Radio spectra
"""

import os
import time
from astropy import units as u
from argparse import ArgumentParser
import setigen as stg
from spectra_gen_defs import SetigenParms, VERSION, DEBUGGING


def generate_fil_file(outpath):
    r"""
    Using setigen, generate a filterbank file.

    Parameters:
        outpath - Path of where to store the resultant numpy file (npy).
    """
    print("spectra_gen_main: Begin outpath = {}".format(outpath))
    t1 = time.time()

    # Set up setigne parameters
    stg_parms = SetigenParms()

    # Instantiate a setigen Frame object
    frame = stg.Frame(fchans=stg_parms.fchans * u.pixel,
                      tchans=stg_parms.tchans * u.pixel,
                      df=stg_parms.df,
                      dt=stg_parms.dt,
                      fch1=stg_parms.fch1,
                      ascending=(stg_parms.ascending))

    # Add noise to stg object.
    if stg_parms.adding_noise:
        frame.add_noise(x_mean=10, noise_type='chi2')

    # Signal 1 will be detected.
    signal_1_intensity = frame.get_intensity(snr=stg_parms.snr_1)
    frame.add_constant_signal(f_start=frame.get_frequency(stg_parms.signal_start_1),
                              drift_rate=stg_parms.drift_rate_1,
                              level=signal_1_intensity,
                              width=stg_parms.width_1,
                              f_profile_type="gaussian")

    # Signal 2 will be detected.
    signal_2_intensity = frame.get_intensity(snr=stg_parms.snr_2)
    frame.add_constant_signal(f_start=frame.get_frequency(stg_parms.signal_start_2),
                              drift_rate=stg_parms.drift_rate_2,
                              level=signal_2_intensity,
                              width=stg_parms.width_2,
                              f_profile_type="gaussian")

    # Signal 3 will be detected.
    signal_3_intensity = frame.get_intensity(snr=stg_parms.snr_3)
    frame.add_constant_signal(f_start=frame.get_frequency(stg_parms.signal_start_3),
                              drift_rate=stg_parms.drift_rate_3,
                              level=signal_3_intensity,
                              width=stg_parms.width_3,
                              f_profile_type="gaussian")

    # Save the frame as a Filterbank file.
    frame.save_fil(outpath)
    
    # Report npy characteristics
    file_size = os.path.getsize(outpath)
    print("spectra_gen_main: 2D shape = {}".format(frame.data.shape))
    print("spectra_gen_main: File size = {} MB".format(file_size / int(1e6)))
    print("spectra_gen_main: End, elapsed time = {:0.1f} s".format(time.time() - t1))


def main(args=None):
    r"""
    This is the entry point to the plotSETI executable.

    Parameters
    ----------
    args : dict

    """
    # Create an option parser to get command-line input/arguments
    parser = ArgumentParser(description="strectra_gen - Generate synthetic Gnu Radio spectra, version {}."
                            .format(VERSION))

    parser.add_argument("output_npy_path", type=str, help="Path to the output numpy file (.npy)")

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    fullpath = os.path.abspath(args.output_npy_path)
    generate_fil_file(fullpath)


if __name__ == "__main__":
    if DEBUGGING:
        main(["/tmp/spectra.npy"])
    else:
        main()
