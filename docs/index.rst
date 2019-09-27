
########################################
Welcome to Avgangstider's documentation!
########################################

Table of contents
=================
.. toctree::
   :maxdepth: 2

   api
   flask_app
   developing


Screenshots
===========

This is what you would see in your browser for Oslo S:

.. image:: _static/Oslo_S.png
    :width: 80%
    :align: center

...or for Jernbanetorget:

.. image:: _static/Jernbanetorget.png
    :width: 80%
    :align: center


Run from Docker container
=========================

Avgangstider comes with a Docker container ready to run. In order to run your
own server, just do::

   docker run -d -p 5000:5000 marhoy/avgangstider

You can then access your own server at http://localhost:5000/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
