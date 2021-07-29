from astropy import units as u
import setigen as stg
import matplotlib.pyplot as plt

from main import DopplerFinder


# Define observation parameters
f_start = 3e9  #Hz
BW = 1e6 #Hz
tsamp=1 #seconds
f_stop = f_start + BW
n_fine_chans = int(1e6)
ntime = int(64)
mjd=59423.2


# Define fake signal parameters
snr_of_fake_pulse=100
drift_rate = -2
width = 5 #Hz

print("Creating fake signal...")
# Create a fake signal
frame = stg.Frame(fchans=n_fine_chans*u.pixel,
                  tchans=ntime*u.pixel,
                  df=BW/n_fine_chans*u.Hz,
                  dt=tsamp*u.s,
                  fch1=f_start*u.Hz)

noise = frame.add_noise(x_mean=10, noise_type='chi2')
signal = frame.add_signal(stg.constant_path(f_start=frame.get_frequency(index=n_fine_chans/2), #injecting exactly in middle of band
                                            drift_rate=drift_rate*u.Hz/u.s),
                          stg.constant_t_profile(level=frame.get_intensity(snr=snr_of_fake_pulse)),
                          stg.gaussian_f_profile(width=width*u.Hz),
                          stg.constant_bp_profile(level=1))

print("Done.")


print("Clancy's being initialised")
clancy = DopplerFinder(filename="CH0_TIMESTAMP", source_name="test", src_raj=7.456805, src_dej=5.225785,
                        tstart=mjd, tsamp=tsamp, f_start=f_start, f_stop=f_stop, n_fine_chans=n_fine_chans, 
                        n_ints_in_file=ntime)

print("Clancy's searching for ET")
clancy.find_ET(frame.data)
