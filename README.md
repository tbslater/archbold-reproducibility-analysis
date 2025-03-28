# Reproducibility analysis: Archbold et al. (2024)

This repository documents a reproducibility analysis of Archbold et al., 2024. The original paper used agent-based modelling to investigate the spread of cardiovascular disease risk factors within a social network. Workplace interventions targeting diet and inactivity were simulated. See the reference below.

> J. Archbold, S. Clohessy, D. Herath, N. Griffiths and O. Oyebode, An Agent-Based Model of the Spread of Behavioural Risk-Factors for Cardiovascular Disease in City-Scale Populations, PLoS ONE, 19(5): e0303051, 2024. <https://doi.org/10.1371/journal.pone.0303051>

Original source code can be accessed [here](https://github.com/nathangriffiths/CVD-Agent-Based-Model.git).

## Code

The `.py` files associated with the reproducibility analysis can be found in `/code` folder.

All four original files are attached in the `/model` sub-folder, albeit with some minor modifications (necessary for running workplace intervention simulations). I have also attached a fifth file `intervention.py` which is a slightly more tweaked version of the `spread.py` file, and is required for the simulating the workplace interventions.

The code for running my analysis is stored in the `/analysis` sub-folder. It contains the following files:

-   `baseline.py`: running baseline scenario and calibration (table 3 and figure 1);
-   `sensitivity.py`: running sensitivity analysis (table 4);
-   `scalability.py`: running code to assess scalability (figure 2);
-   `workplace.py`: running intervention scenarios (table 6).

## Parameters

The data to inform the model is stored in `/parameters` and contains information for workplace contact sizes of 4 and 21. These files are all copies from the original repository.

## Article

The results of my reproducibility analysis are documented in a blog post [here]().

## Citation
