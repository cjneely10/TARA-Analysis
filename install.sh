#!/usr/bin/env bash

# Create conda environment
conda env create -f environment.yml

# Identify install source
CONDA=`which conda`
CONDA_DIRNAME=`dirname $CONDA`
MINICONDA=`dirname $CONDA_DIRNAME`
SOURCE=$MINICONDA/etc/profile.d/conda.sh

# Activate new environment
source $SOURCE
conda activate TARA-Analysis

# Pull streamlit-components templates
cd TARAVisualize/components
git clone https://github.com/streamlit/component-template.git
cp *.tsx component-template/template/my_component/frontend/src/
rm component-template/template/my_component/frontend/__init__.py

# Install dependencies and custom components
cd component-template/template/my_component/frontend
npm install react-plotly.js plotly.js @types/react-plotly.js
npm install
