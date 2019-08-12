"""Support shorthand import of our classes into the namespace.
"""
import sys
import logging

from .scraper import Scraper
from .stats import Stats
from .config import Config
from .statistics import Statistics
from .dbsession import DBSession
from .datamodel import DataModel
from .dropboxcacher import DropBoxCacher

ROOT = logging.getLogger()
ROOT.setLevel(logging.DEBUG)

if not ROOT.hasHandlers():
    HANDLER = logging.StreamHandler(sys.stdout)
    HANDLER.setLevel(logging.INFO)
    FORMATTER = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    HANDLER.setFormatter(FORMATTER)
    ROOT.addHandler(HANDLER)
