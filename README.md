# Data Smooth Method
This repo's codes provide a simple data smoother based penalized least squares, known as Whittaker smoother as well.
This smoother is extremely fast, gives continuous control over smoothness, interpolates automatically.

## Prerequisites
- `Python 3`
- `Scipy`, `Numpy`

## Usage
Class `SIGSMOOTH` in `signal_smooth.py` provides two methods for differenet situation.
- `PLS_expect`: a general situation as interval of x-coordinate is equal
- `PLS_interpolation`: used as if interval of x-coordinate is not equal

## Example
Following the steps in `test.py` to find a most probable distribution line for data in `Test.txt`, you might have a glance at our method. 

## License
This repository is licensed under the **GNU GPLv3**.
