#!/usr/bin/env bash

conda env create -f environment.yml

git clone https://github.com/streamlit/component-template.git
cd component-template/template/my_component/frontend
npm install
npm install react-plotly.js plotly.js