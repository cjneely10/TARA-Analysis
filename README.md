[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/cjneely10/TARA-Analysis/main/TARAVisualize/main.py)


# TARA Data summary

Open this repo in `streamlit` using the link above, or follow the installation instructions below for a standalone version.

### Installation

This visualizer requires a modern browser and a system that can support NodeJS/React.

Dependencies: `conda`, `git`.

```
git clone https://github.com/cjneely10/TARA-Analysis.git
cd TARA-Analysis
conda env create -f environment.yml
```

### Local Usage

Running the visualizer will use &ge; 450MB of system RAM.

```shell
conda activate TARA-Analysis
streamlit run TARAVisualize/main.py
```

Your browser should launch a window at `http://localhost:8501/`
