# KiCAD EasyEDA Parts

KiCAD Plugin to download footprints, symbols and 3D models from EasyEDA and convert them for KiCAD.

This is a wrapper for [easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py) and adds a shortcut in KiCAD with a
little menu to download parts by their LCSC id.

## Installation

- Install [easyeda2kicad.py](https://github.com/uPesy/easyeda2kicad.py):  
  `pip install easyeda2kicad`
- Add [my repository](https://raw.githubusercontent.com/InfraredAces/InfraredAces-KiCAD-Repository/master/repository.json) to KiCAD:  
  `https://raw.githubusercontent.com/InfraredAces/InfraredAces-KiCAD-Repository/master/repository.json`
- Download the `KiCAD EasyEDA Parts` plugin in the KiCAD Plugin and Content Manager.

## Usage

- Click <img src="icon.png" width="20"/> in the toolbar (PCB Editor).
- Enter the LCSC id of the part you want to download and click Download.
- The files will then be downloaded to ./libs/easyeda/ in you project folder.
- Make sure you've add the libraries in Project Specific Libraries.
