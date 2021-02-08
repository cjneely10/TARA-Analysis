# TARA Data summary

### Installation

This visualizer requires a modern browser and a system that can support NodeJS/React.

Dependencies: `conda`, `git`.

```
git clone https://github.com/cjneely10/TARA-Analysis.git
cd TARA-Analysis
./install.sh
```

A conda environment will be created to contain the `nodejs` and `streamlit` dependencies.

### Usage

Running the visualizer will use &ge; 450MB of system RAM.

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
