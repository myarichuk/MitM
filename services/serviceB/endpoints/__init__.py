"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import sys

sys.path.append('../../')
sys.path.append('../')