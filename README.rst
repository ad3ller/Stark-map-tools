Stark map tools
===============

v0.0.1.dev.

Python tools for plotting Stark and Zeeman maps.

Install
-------

Clone and install using setuptools.

.. code-block:: bash

   git clone https://github.com/ad3ller/Stark-map-tools
   cd Stark-map-tools
   python setup.py install

Usage
--------

.. code-block:: python

    >>> from smtools import sm_sort, lc_cmap

sm_sort(arr)    
    sort a Stark/ Zeeman map to preserve the state order through exact crossings.

lc_cmap(xvals, yvals, colors)
    apply a colormap to matplotlib.pyplot.plot using LineCollections.
     
See notebooks for examples.
