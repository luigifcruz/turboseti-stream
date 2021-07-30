#!/usr/bin/bash

FILESTEM=/tmp/spectra
rm $FILESTEM.* 2> /dev/null
rm CH0* 2> /dev/null
python3 spectra_gen/spectra_gen_main.py $FILESTEM.fil
