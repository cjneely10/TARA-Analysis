import os
import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import streamlit as st
from typing import Dict
import matplotlib.pyplot as plt

FILE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(FILE_DIR, "data/tax-summary.tsv.gz")
FASTANI_A = os.path.join(FILE_DIR, "data/all-alex-v-alex.fastani.out.gz")
REPEATS_FILE = os.path.join(FILE_DIR, "data/repeats-summary.bylength.tsv.gz")
TAX_LEVELS = ("kingdom", "clade", "phylum", "class", "subclass", "order", "family", "genus", "species")
TITLE = "TARA oceans data visualizer"
FILTER_BY_OPTIONS = ("size_fraction", "depth")
