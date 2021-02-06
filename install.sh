#!/usr/bin/env bash

conda env create -f environment.yml
npm install react-plotly.js plotly.js

git clone https://github.com/streamlit/component-template.git
cd component-template/template/my_component/frontend
npm install