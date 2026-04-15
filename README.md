# Biomechoo Ensembler
The plotting environment for the python implementation of biomechZoo
> BiomechZoo for Python available at:
> https://pypi.org/project/biomechzoo/

## Overview
This repository provides the visualization environment for the biomechzoo toolbox implemented in python. The pipeline
reads .zoo files and based on user input of channels and events creates visualizations fit for scientific publications. 

---
## Repository structure 
```
biomechzoo_ensembler/
├── data/
│   └── event_data/               ← Some example data for statistical plots
│   └── line_data/               ← Some example data for line plots
├── src/
│   ├── data_store.py
│   └── ensembler.py
│   ├── helpers.py
│   ├── renderes.py
│   ├── style_content.py
├── main.ipynb                  ← notebook showcasing use cases 
├── main.py                     ← python script with example project
├── ensembler0.0.1.pdf
└── README.md
```

---
## Dependencies
### 1. biomechzoo

The ensembler depends on data being processed with the python implementation of biomechzoo. 


**Setup instructions:**

1. Initialize Python 3.11 for compatibility with https://github.com/stanfordnmbl/opencap-processing
2. Install biomechzoo
```pip install [biomechzoo]```
3. Run biomechzoo pipeline and finish with data normalization ```biomechzoo.normalize(fld)```
4. Initialize the ensembler 

