#!/usr/bin/env bash

conda env create -f environment.yml

CURR_DIR=`pwd`
cd TARAVisualize/components
git clone https://github.com/streamlit/component-template.git
cp *.tsx component-template/template/my_component/frontend/src/
rm component-template/template/my_component/frontend/__init__.py
cd component-template/template/my_component/frontend
npm install react-plotly.js plotly.js @types/react-plotly.js
npm install
