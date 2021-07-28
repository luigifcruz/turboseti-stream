# turboseti-stream

A "hack-ey" way to get turboSETI to accept data in a streaming fashion, i.e. straight from memory, instead of reading `fil`/`HDF5` files from disk. 
This is especially useful for real-time pipelines where data need to be analysed as they are being recorded.

The aim is to eventually integrate this piece of code into a GNURadio block to perform SETI searches with the platform.
