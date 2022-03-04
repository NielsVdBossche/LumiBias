# LumiBias

Python implementation for simulating VdM scans and obtaining a measurement of the bias obtained in a VdM scan.

To obtain a bias estimate, the beam parameters are provided in a json file. Next, the code can be ran using:
```console
python3 RunVDMSim.py <JSON filename>
```
Alternatively, the code can also be used as a callable function. Two options are possible:
```python
import RunVDMSim

RunVDMSim.runVDMSimOnJSON("/path/to/JSONfile")
RunVDMSim.runVDMSim(dict) # Where dict represents a dictionary with the same internal structure as the jsonfile
```
Both options return a list of 2 values: the bias from a Single Gaussian and a Double Gaussian fit to the VdM simulation.

Currently working with this method:
- Single/Double/Triple Gaussian
- (Double) Super Gaussian

For a Beam Imaging scan, use:
```console
python3 RunVDMSim.py <JSON filename> BI
```
