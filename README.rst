Avgangstider fra `Entur <https://en-tur.no/>`_
===============================================

Avgangstider consists of two parts:

*  Functionallity to get data from the Entur API
*  A Flask app that shows current departure times for a specific stop.


Run from Docker container
=========================

Avgangstider comes with a Docker container ready to run. In order to run your
own server, just do::

   docker run -d -p 5000:5000 marhoy/avgangstider

You can then access your own server at http://localhost:5000/


Installing
==========
Avgangstider requires Python 3.7. I recommend using `pyenv <https://github
.com/pyenv/pyenv>`_ for installing and managing and can be
installed
from
PyPi::

   pip install avgangstider


