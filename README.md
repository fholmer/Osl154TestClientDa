# Osl154TestClientDa

Opc Da command line test client for Osl154 spesification

# Requirements

OS:

-   Windows 10 or newer

Software:

-   Python 3.7 or newer (https://www.python.org/downloads/windows)
-   Greybox Free OPC DA Auto Wrapper (http://gray-box.net/download_daawrapper.php?lang=en)

NB! Make sure you install the 64bit version of Python and register the 64-bit version of OPC DA Auto Wrapper

# Installation

1. Install Python and OPC DA Auto Wrapper. 

2. Open command line and create an empty folder:

> mkdir C:\Project\Osl154TestClientDa
> cd C:\Project\Osl154TestClientDa

3. Clone or download content of https://github.com/fholmer/Osl154TestClientDa into current dir

> gh repo clone fholmer/Osl154TestClientDa .

4. Create an virtual environment for python and install required packages using pip:

> py -3 -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt

5. (optional) Run tests
> pytest -Wignore

Every test should pass if everything is good

# Usage

First create bmp-data for your sign:

> py -m osl154 create SSA1_SIGN1 -width 304 -height 104

Make sure opctag, width and height match your sign

