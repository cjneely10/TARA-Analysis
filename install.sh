#!/usr/bin/env bash

conda env create -f environment.yml

CURR_DIR=`pwd`
cd TARAVisualize/components
git clone https://github.com/streamlit/component-template.git
cd component-template/template/my_component/frontend
npm install
npm install react-plotly.js plotly.js @types/react-plotly.js
cd -
mv *.tsx component-template/template/my_component/frontend/src/
rm component-template/template/my_component/frontend/__init__.py