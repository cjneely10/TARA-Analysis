# TARA Data summary

### Installation

This visualizer requires a modern browser and a system that can support NodeJS/React.

Dependencies: `conda`, `git`

```
git clone https://github.com/cjneely10/TARA-Analysis.git
cd TARA-Analysis
./install.sh
conda activate TARA-Analysis
cd component-template/template/my_component/frontend
npm install react-plotly.js plotly.js @types/react-plotly.js
npm install
```

### Usage

Activate your conda environment (if not done so already):

```
conda activate TARA-Analysis
```

In one terminal, start a `nodejs` development server:

```
./start.sh
```

Run the visualizer in a different terminal:

```
./run.py -t <threads>
```

![](https://github.com/cjneely10/TARA-Analysis/blob/main/assets/main-image.png)
