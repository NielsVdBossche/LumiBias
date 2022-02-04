# LumiBias

Python implementation for simulating VdM scans and obtaining a measurement of the bias obtained in a VdM scan.

To obtain a bias estimate, the beam parameters are provided in a json file. Next, the code can be ran using:
```console
python3 RunVDMSim.py <JSON filename>
```

Currently working with this method:
- Single Gaussian
- Double Gaussian

For a Beam Imaging scan, use:
```console
python3 RunVDMSim.py <JSON filename> BI
```
