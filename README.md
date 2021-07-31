# turboseti-stream

A "hack-ey" way to get turboSETI to accept data in a streaming fashion, i.e. straight from memory, instead of reading `fil`/`HDF5` files from disk. 
This is especially useful for real-time pipelines where data need to be analysed as they are being recorded.

The aim is to eventually integrate this piece of code into a GNURadio block to perform SETI searches with the platform.

## Requirements
- [turbo_seti](https://github.com/UCBerkeleySETI/turbo_seti) (also submodule'd)
- [setigen](https://github.com/bbrzycki/setigen)

## Running main.py from a Filterbank File
- Edit ```spectra_gen/spectra_gen.cfg``` and change parameter values as needed.  Do not add or delete any sections or parameters.
- Run bash script ```mkspectra.sh``` which will regenerate ```/tmp/spectra.fil```.
- Finally, run the ```test_synth_signal.py``` Python program to execute ```main.py``` against the new version of ```/tmp/spectra.fil```.
