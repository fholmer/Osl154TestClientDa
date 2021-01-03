Osl154TestClientDa
==================

Summary
-------

Opc Da command line test client for Osl154 specification

Requirements
------------

OS:

-   Windows 10 or newer

Software:

-   Python 3.8 x86 (32-bit) or newer: https://www.python.org/downloads/windows
-   Graybox Free OPC DA Auto Wrapper: http://gray-box.net/download_daawrapper.php?lang=en

Installation
------------

#.  Make sure you install the 32bit version of Python

#.  Open command line and create an empty folder:

    .. code-block:: doscon

        > mkdir C:\Projects\Osl154Da
        > cd /d C:\Projects\Osl154Da

#.  Register the 32bit version of OPC DA Auto Wrapper. 

    .. code-block:: doscon

        # unzip graybox_opc_automation_wrapper.zip
        > py -m zipfile -e graybox_opc_automation_wrapper.zip lib
        # register as 32bit
        > %systemroot%\SysWoW64\regsvr32.exe %cd%\lib\x86\gbda_aut.dll

#.  Create an virtual environment for python and install required packages using pip:

    .. code-block:: doscon

        > py -3-32 -m venv venv
        > venv\Scripts\activate
        > pip install https://github.com/fholmer/Osl154TestClientDa/archive/main.zip

Usage
-----

First check that your opc-server is available by running this command:

.. code-block:: doscon

    > osl154da list-servers

The name of your server should appear in this list. This is the name to be
used in the next step.

Create some initial BMP-data for your sign. You can use the discover function:

.. code-block:: doscon

    > osl154da discover-sign SERVER.1

Or add it manually:

.. code-block:: doscon

    > osl154da create sign1 -server SERVER.1 -tag SSA1_SIGN1 -width 304 -height 104

.. note:: Make sure server, opctag, width and height match your server and sign

This command will create a directory ``signs/default``:

.. code-block:: text

    /signs
        /default
            /sign.json
            /1.bmp
            /2.bmp
            /3.bmp
            /4.bmp

BMP-file can be duplicated and edited to make different test images.
``sign.json`` can also be edited to adjust opc-tag names.

.. warning::

    if you run the ``add-sign`` or ``discover-sign`` command again all
    changes will be overwritten.

Read the values currently on the sign:

.. code-block:: doscon

    > osl154da read

Send a rgb-on command to the sign:

.. code-block:: doscon

    > osl154da rgb-on -image 1.bmp

Image ``1.bmp`` will now be loaded in ``IMAGE_TOSET``. ``VALUE`` is set to 9999
and after a short delay the ``COMMAND`` is set to ``RGB-ON``.
