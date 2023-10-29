# Skynet
## UCS Satellite Database

## Overview

The UCS Satellite Database is the premier free and openly accessible database cataloging all of the over 5,000 actively operating satellites. It provides a detailed record of 28 different aspects of each satellite, from its launch details, orbit position, to its functionality. The database is a fundamental tool for space professionals, researchers, journalists, and satellite enthusiasts. As the pace of satellite launches is surging rapidly with organizations like SpaceX and One Web planning satellite constellations numbering in tens of thousands, there's an increasing need to automate the data collection and verification process. We aim to integrate automation in data collection and also explore innovative ways to present data using images and tables for users who may not be technically inclined.

## Technologies Stack
- Python
- Vue
- Electron
- Scarpy (Web scraping techniques)】

## Usage
```bash
# installing virtual environment (recommended, not required), may need --user flag
py -m pip install --user virtualenv

# create new venv environment (do in backend folder)
python -m venv venv

# starting venv in windows with powershell/visual studio terminal
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process venv\Scripts\Activate.ps1

# starting venv on mac
source myvenv/bin/activate

# install Flask (do in venv)
pip install -U Flask pip install flask flask-cors

# install environmental variables
pip install python-dotenv

```

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.
