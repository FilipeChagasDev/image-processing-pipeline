# Image Processing Pipeline (IPP)

![Language](https://img.shields.io/badge/Language-Python3-blue)
![Version](https://img.shields.io/badge/Version-v0.1.0-green)
![License](https://img.shields.io/badge/License-MIT-blue)

## Brief
**Image Processing Pipeline (IPP)** is a Python image processing helper.

This program processes images through a pipeline architecture, where the filters are arranged as pipes and connected by buses.

This program can be integrated into another Python application as a library.

## Dependencies
* Python >= 3
* NumPy
* OpenCV (cv2)

## Team
* **Filipe Chagas** (project owner) *github.com/filipechagasdev*
  
## Progress
It's still very premature...

### Main architecture
* [x] Bus class
* [x] Pipe class
* [x] Pipeline class
* [ ] Plug-in loading
* [ ] XML parsing

### Pipes
* [x] Split and merge pipes
* [x] Fork and blend pipes (not tested)    
* [ ] Addition pipe
* [ ] Product pipe
* [ ] BGR to HSV converter pipe
* [ ] HSV to BGR converter pipe
* [ ] RGB to BGR converter pipe
* [ ] BGR to RGB converter pipe
* [ ] Equalize histogram pipe
* [ ] Ajust average pipe
* [ ] Ajust deviation pipe
* [ ] Gaussian blur pipe
* [ ] Median blur pipe