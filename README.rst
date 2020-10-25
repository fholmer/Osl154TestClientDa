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

-   Python 3.7 or newer: https://www.python.org/downloads/windows
-   Graybox Free OPC DA Auto Wrapper: http://gray-box.net/download_daawrapper.php?lang=en

.. note::

    Make sure you install the 64bit version of Python and register the 64-bit version of OPC DA Auto Wrapper


Installation
------------

#.  Install Python and OPC DA Auto Wrapper.

#.  Open command line and create an empty folder:

    .. code-block:: doscon

        > mkdir C:\Project\Osl154TestClientDa
        > cd C:\Project\Osl154TestClientDa

#.  Create an virtual environment for python and install required packages using pip:

    .. code-block:: doscon

        > py -3 -m venv venv
        > venv\Scripts\activate
        > pip install https://github.com/fholmer/Osl154TestClientDa/archive/main.zip

Usage
-----

First check that your opc-server is available by running this command:

.. code-block:: doscon

    > py -m osl154 list-servers

The name of your server should appear in this list. This is the name to be
used in the next step.

Create some initial bmp-data for your sign:

.. code-block:: doscon

    > py -m osl154 create SIGN1 -server SERVER.1 -tag SSA1_SIGN1 -width 304 -height 104

.. note:: Make sure server, opctag, width and height match your server and sign

This command will create a directory ``signs/SIGN1``:

.. code-block:: text

    /signs
        /SIGN1
            /sign.json
            /1.bmp

BMP-file can be duplicated and edited to make different test images.
sign.json can also be edited to adjust opc-tag names.

.. warning::

    if you run the ``create`` command again all changes will be overwritten.

Send a rgb-on command to the sign:

.. code-block:: doscon

    > py -m osl154 rgb-on SIGN1 -image 1.bmp

Image ``1.bmp`` will now be loaded in ``IMAGE_TOSET``. ``VALUE`` is set to 9999
and after a short delay the ``COMMAND`` is set to ``RGB-ON``.
