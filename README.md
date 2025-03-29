# DTMF Project

This project demonstrates a simple Dual-Tone Multi-Frequency (DTMF) system.  
It consists of:

1. **Decoder** (decoder.py):  
   - Records audio, performs an FFT, detects the frequency peaks, and determines which DTMF tone (telephone keypad digit) was pressed.

2. **Encoder** (encoder.py):  
   - Generates two sinusoidal signals corresponding to a pressed DTMF key (one for the row frequency, one for the column frequency).  
   - Plays the combined signal (sum of both frequencies).  
   - Also plots time-domain and frequency-domain representations of the signal.

3. **Helper Library** (bib.py):  
   - Contains a class and methods for FFT calculations and plotting.
