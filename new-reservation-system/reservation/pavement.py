#!/usr/bin/python

from paver.easy import *
import paver.doctools
import os
import glob
import shutil
import sys

sys.path.append(os.path.dirname(__file__))

@task
def setup():
    sh('python -m pip install -U coverage')  
    pass

@task
def test():
    sh('python -m coverage run --source booking -m unittest discover -s test')
    sh('python -m coverage html')
    sh('python -m coverage report --show-missing')
    pass

@task
def clean(): 
    for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
    for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
    for pycache in glob.glob("./__pycache__"): shutil.rmtree(pycache)
    try:
        shutil.rmtree(os.getcwd() + "/cover")
    except:
        pass
    pass

@task
@needs(['setup', 'clean', 'test'])
def default():
    pass

