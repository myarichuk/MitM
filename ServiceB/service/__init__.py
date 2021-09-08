"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import service.endpoints
import sys

sys.path.append('../')