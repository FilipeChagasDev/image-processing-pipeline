# Image Processing Pipeline (IPP)

## Brief
**Image Processing Pipeline (IPP)** is a Python image processing helper.

This program processes images through a pipeline architecture, where the filters are arranged as pipes and connected by buses.

This program can be integrated into another Python application as a library.

## Team
* **Filipe Chagas** (project owner) *github.com/filipechagasdev*
  
## Progress
It's still very premature...

### Main architecture
* [x] Bus class (not tested)
* [x] Pipe class (not tested)
* [x] Pipeline class (not tested)
* [ ] Plug-in loading
* [ ] XML parsing

### Pipes
* [x] Split and merge pipes (not tested)
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