# Reproducibility analysis: Archbold et al. (2024)

This repository documents a reproducibility analysis of Archbold etb al., 2024. The original paper used agent-based modelling to investigate the spread of cardiovascular disease risk factors within a social network. Workplace interventions targetting diet and inactivity were simulated. See the reference below.  

> J. Archbold, S. Clohessy, D. Herath, N. Griffiths and O. Oyebode, An Agent-Based Model of the Spread of Behavioural Risk-Factors for Cardiovascular Disease in City-Scale Populations, PLoS ONE, 19(5): e0303051, 2024.>

Original source code can be found at <https://github.com/nathangriffiths/CVD-Agent-Based-Model.git>

## Code

The `.py` files associated with the reproducibility analysis can be found in `/code` folder.

All four original files are included, albeit with some minor modifications (necessary for running workplace intervention simulations). I have also attached a fifth file `intervention.py` which is a slightly more tweaked version of the `spread.py` file, and is required for the simulating the workplace interventions. 

## Parameters

The data to inform the model is stored in `/parameters` and contains information for workplace contact sizes of 4 and 21. These files are all copies from the original repository. 