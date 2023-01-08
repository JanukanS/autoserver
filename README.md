# AutoServer

AutoServer is a python library for making quick web UIs, it was originally made for HackEd 2023. 
## Installation
AutoServer is available on the python package index (PyPI) and can be installed through pip.
```bash
pip install autoserver
```
## Features
- Able to create a form for arguments that are either strings, floats or integers
- Display documentation from RST style docstrings (similar to sphinx)
## Example
We will start with just the functions. This library is able to work on functions with type hinted input parameters and RST style docstrings. Without the type hints, all arguments are assumed to be strings and documentation cannot be displayed without the docstring. 
```python
def deltaWavelength(colour: str, index1: float, index2: float):
    """
    Compute the change in wavelength due to a change in optical index
    :param colour: Any one of 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'
    :param index1: The initial optical index
    :param index2: The final optical index
    :return:
    """
    wlenDict = {
        "red": 700.0,
        "orange": 620.0,
        "yellow": 580.0,
        "green": 532.0,
        "blue": 500.0,
        "indigo": 450.0,
        "violet": 400.0,
    }
    wlen = wlenDict.get(colour, None)
    if wlen:
        return f"The change in wavelength is {wlen*(1/index2-1/index1)} nm."
    else:
        return "Error"

def computeFrequency(wlen: float, index: float):
    """
    Compute the frequency for a given wavelength within an optical medium
    :param wlen: Wavelength expressed in nm
    :param index: Optical Index
    :return:
    """
    freq = 3E8/(index*wlen*1e-9)
    return f"Frequency of light would be {freq:e} Hz."
```
To use autoserver, we need to import it. Then we initialize the server object. Functions can be added to the server through the use of the decorator. Finally the server must be run. 
```python
from autoserver import AutoServer
app = AutoServer()

@app.addfunc
def deltaWavelength(colour: str, index1: float, index2: float):
    """
    Compute the change in wavelength due to a change in optical index
    :param colour: Any one of 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'
    :param index1: The initial optical index
    :param index2: The final optical index
    :return:
    """
    wlenDict = {
        "red": 700.0,
        "orange": 620.0,
        "yellow": 580.0,
        "green": 532.0,
        "blue": 500.0,
        "indigo": 450.0,
        "violet": 400.0,
    }
    wlen = wlenDict.get(colour, None)
    if wlen:
        return f"The change in wavelength is {wlen*(1/index2-1/index1)} nm."
    else:
        return "Error"

@app.addfunc
def computeFrequency(wlen: float, index: float):
    """
    Compute the frequency for a given wavelength within an optical medium
    :param wlen: Wavelength expressed in nm
    :param index: Optical Index
    :return:
    """
    freq = 3E8/(index*wlen*1e-9)
    return f"Frequency of light would be {freq:e} Hz."

app.run()
```