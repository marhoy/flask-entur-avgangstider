Developing
==========

#.  Install `pyenv <https://github.com/pyenv/pyenv>`_ with some plugins,
    especially `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_
    and `pyenv-which-ext <https://github.com/pyenv/pyenv-which-ext>`_.
    These extensions will be installed automatically if you use the
    `pyenv-installer <https://github.com/pyenv/pyenv-installer>`_
#. Install Poetry


Setting up your development environment
---------------------------------------
 ::

    pyenv install 3.7.4
    pyenv virtualenv 3.7.4 avgangstider
    git clone git@github.com:marhoy/flask-entur-avgangstider.git
    cd flask-entur-avgangstider
    pyenv local avgangstider 3.7.4
    poetry install


Start a debugging server
------------------------

 ::

    python src/avgangstider/flask_app.py


Run all tests and code checks
-----------------------------

After having made changes: Make sure all tests are still OK, test coverage
is 100% and both flake8 and mypy are happy::

    tox

    [...]
    src/avgangstider/utils.py .                                              [  6%]
    tests/test_entur_api.py ...                                              [ 25%]
    tests/test_entur_query.py ...                                            [ 43%]
    tests/test_flask_app.py .......                                          [ 87%]
    tests/test_utils.py ..                                                   [100%]

    ---------- coverage: platform darwin, python 3.7.4-final-0 -----------
    Name    Stmts   Miss  Cover   Missing
    -------------------------------------
    -------------------------------------
    TOTAL     195      0   100%

    6 files skipped due to complete coverage.


    ============================== 16 passed in 4.21s ==============================
    lint run-test-pre: PYTHONHASHSEED='2636496648'
    lint run-test: commands[0] | poetry run flake8 src tests
    lint run-test: commands[1] | poetry run isort --recursive --check-only src tests
    lint run-test: commands[2] | poetry run mypy src
    ___________________________________ summary ____________________________________
      py37: commands succeeded
      lint: commands succeeded
      congratulations :)


Build new docker image
----------------------

If you want to build your own docker image::

    docker build -t avgangstider .
    docker run -d -p 5000:5000 avgangstider


