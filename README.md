# QtSWINE - PyQt GUI for [SWINE](https://github.com/ajulik1997/SWINE)
An application that uses Monte-Carlo methods to analyse the effects of varying slit widths on the average neutron flux of neutron beamline facilities.
Although originally designed for use with the [OffSpec reflectometer](https://www.isis.stfc.ac.uk/Pages/Offspec.aspx) at [ISIS Neutron Source](https://www.isis.stfc.ac.uk), this application is now heavily customisable and can work with any compatible [McStas](http://mcstas.org/) instrument file.

## Table of Contents

- [How It Works](#how-it-works)
  - [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisistes)
  - [Installing](#installing)
  - [Running Simulations](#running-simulations)
  - [Plotting Data](#plotting-data)
- [Customisations](#customisations)
  - [Using Different Versions of McStas](#using-different-versions-of-mcstas)
  - [Customising Parameters on Default Instrument](#customising-parameters-on-default-instrument)
  - [Using Custom McStas Instruments](#using-custom-mcstas-instruments)
    - [McStas Instrument Compatibility Guidelines](#mcstas-instrument-compatibility-guidelines)
  - [Changing Simulation Parameters](#changing-simulation-parameters)
- [When Things Go Wrong](#when-things-go-wrong)
  - [Incompatible Customised McStas Installations](#incompatible-customised-mcstas-installations)
  - [Issues with Compiling Instrument Files](#issues-with-compiling-instrument-files)
  - [Installing to Non-root Directories](#installing-to-non-root-directories)
  - [More About the Data File (.npz) Format](#more-about-the-data-file-(.npz)-format)
- [Built With](#built-With)
- [Licencing](#licencing)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

## How It Works

### Features

## Getting Started

### Prerequisites

### Installing

### Running Simulations

### Plotting Data

## Customisations

### Using Different Versions of McStas

### Customising Parameters on Default Instrument

### Using Custom McStas Instruments

#### McStas Instrument Compatibility Guidelines

### Changing Simulation Parameters

## When Things Go Wrong

### Incompatible Customised McStas Installations

### Issues with Compiling Instrument Files

### Installing to Non-root Directories

### More About the Data File (.npz) Format

## Built With

* [**McStas 2.4.1** for Windows](http://mcstas.org/download/install_windows/)
* [**Python 3.4.5**](https://www.python.org/downloads/) packaged with McStas using [Miniconda3](https://conda.io/miniconda.html)
* [**PyQt4**](https://www.riverbankcomputing.com/software/pyqt/download) for connecting underlying processes to UI elements
* [**Qt4 Designer**](http://doc.qt.io/archives/qt-4.8/designer-manual.html) for UI design
* [**Matplotlib 2.2.2**](https://matplotlib.org/2.2.2/index.html) for plotting data
* [**PyInstaller 3.3.1**](https://www.pyinstaller.org/) for packaging final python script into a standalone executable

## Licencing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author

**Alexander Liptak** - Theoretical Physics student at [Royal Holloway University of London](https://www.royalholloway.ac.uk/physics/)

Under the supervision of [**Dr Jos Cooper**](https://www.isis.stfc.ac.uk/Pages/Dr-Joshaniel-Cooper.aspx) and [**Dr. Nina-Juliane Steinke**](https://www.isis.stfc.ac.uk/Pages/Dr-Nina-Juliane-Steinke.aspx)

As part of a 2017 Summer Internship at [ISIS Neutron & Muon Source](https://www.isis.stfc.ac.u)

## Acknowledgements

* [**@willend**](https://github.com/willend) for putting up with my many [McCode](https://github.com/McStasMcXtrace/McCode) bug reports
* [**@jfkcooper**](https://github.com/jfkcooper) for thoroughly troubleshooting and ironing out issues with my code
* [**Talha Shameem**](mailto:Talha.Shameem.2015@live.rhul.ac.uk) for reviewing my code and providing GUI design feedback
* [**@ukarim**](https://github.com/ukarim) for providing an excellent [dark theme](https://draculatheme.com/notepad-plus-plus/) for my [favourite editor](https://notepad-plus-plus.org/)
