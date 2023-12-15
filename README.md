# Skynet
## UCS Satellite Database

## Overview

The UCS Satellite Database is the premier free and openly accessible database cataloging all of the over 5,000 actively operating satellites. It provides a detailed record of 28 different aspects of each satellite, from its launch details, orbit position, to its functionality. The database is a fundamental tool for space professionals, researchers, journalists, and satellite enthusiasts. As the pace of satellite launches is surging rapidly with organizations like SpaceX and One Web planning satellite constellations numbering in tens of thousands, there's an increasing need to automate the data collection and verification process. We aim to integrate automation in data collection and also explore innovative ways to present data using images and tables for users who may not be technically inclined.

## Technologies Stack
- Python
- Vue
- Electron
- Scrapy
- Selenium
- PostgreSQL

## Setup
There might be some formatting issues when running the program on a Windows machine, it is **strongly recommended** to 
run this program on a **macOS** or **Linux** environment.

**Note:** If it's necessary to run on a Windows environment, there will be things needed to be modified in the codebase.
1. Look into `./skynet_scrapy/myspider/myspider/pipelines.py` and switch every line of `value = parsed_date.strftime('%-m/%-d/%y')` 
to `value = parsed_date.strftime('%m/%d/%y')`.
2. Look into `./skynet_scrapy/myspider/myspider/spiders/thespacereport.py` and modify the `service = Service(executable_path="chromium.chromedriver")` line. Change the `executable_path` to specify the path to chromedriver.exe driver that's downloaded on the machine. An example, `executable_path=r"C:\path\to\chromedriver.exe"`
```bash
# installing virtual environment (recommended, not required), may need --user flag
py -m pip install --user virtualenv

# create new venv environment (do in backend folder)
python -m venv <VirutalEnvName>

# starting venv in windows with powershell/visual studio terminal
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process venv\Scripts\Activate.ps1

# starting venv on mac
source myvenv/bin/activate

# Install all required packages
python Packages.py
```

## About chromedriver on mac
Installing chromedriver can be tricky. Please follow these steps:
1. Go to https://googlechromelabs.github.io/chrome-for-testing/ to download the chromedriver for the version of chrome you are working with.<sup>*</sup>
2. Unzip and copy the chromedriver executable
3. Open finder and press cmd + shift + g. This will open a window where you can enter filepath addresses to hidden folders.
4. Navigate to `/usr/local/bin/` by entering /usr/local/bin/ in the address box. In case you don't have a `/usr/local/bin/`, enter /usr/local/ and create a bin directory in this folder and open it.
5. Paste chromedriver in `/usr/local/bin/``
6. In `./skynet_scrapy/myspider/myspider/pipelines.py` lines 38-43 contain information on how to configure your executable_path. If you are on mac and have followed the above steps, you are done setting up the chromedriver.

**Note:** You might run into an error when you run the scrapers for the first time, it happens because Apple blocks the execution of chromedriver binary by defauly. Please execute the following command in terminal:
```bash
sudo xattr -d com.apple.quarantine $(which chromedriver)
```

<sup>*</sup> Although not mandatory, but we recommend you download both the chromedriver and chrome/chrome-headless-shell from the website. Once you install chrome, you will have Google Chrome for Testing on your machine which runs seperately from your personal version of chrome. Please execute the command below if you install this:
```bash
sudo xattr -cr /Applications/Google\ Chrome\ for\ Testing.app
```

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.
