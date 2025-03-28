# Code to reproduce table 5 from Archbold et al., 2024

import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import agent 
import network 
import parameters
import spread

def change_inf(level, risk = None, all_factors = True, pop_size = 350000):
    '''
    FUNCTION TO OBTAIN INFLUENCE LEVELS ASSOCIATED WITH TABLE 5

    PARAMS:
    - level: level 0 or 2? [int]
    - risk: risk factor to minimise/maximise [str]
    - all_factors: minimise/maximise all factors? [bool]
    - pop_size: number of agents [int]

    RETURNS:
    - list of agent list and influence dictionary [list]
    '''

    # Generate agents
    sim_params = parameters.Parameters('scenarios_21')
    sim_network = network.Network(sim_params)
    sim_agents = sim_network.generate_agents(pop_size)

    # Alter default influence dictionary
    influences = sim_params.get_inf_by_rel()
    relationships = ['Spouse', 'Household', 'Friendship', 'Workplace']
    if all_factors == True:
        for i in relationships:
            if i!='Workplace':
                influences[i]['Inactivity'][level] = 1
                influences[i]['Diet'][level] = 1
                influences[i]['Smoking'][level] = 1
                influences[i]['Alcohol'][level] = 1
            else:
                for j in range(1,5):
                    influences[i][j]['Inactivity'][level] = 1
                    influences[i][j]['Diet'][level] = 1
                    influences[i][j]['Smoking'][level] = 1
                    influences[i][j]['Alcohol'][level] = 1
    else:
        for i in relationships:
            if i!='Workplace':
                influences[i][risk][level] = 1
            else: 
                for j in range(1,5):
                    influences[i][j][risk][level] = 1

    return sim_agents, influences

# Set-up
random.seed(0)
levels = [0,2]
labels = ['Level 0', 'Level 2']
risk_factors = ['Inactivity', 'Diet', 'Smoking', 'Alcohol']
rates = {
    0: {
        risk_factors[0]: {'M': 0, 'F': 0},
        risk_factors[1]: {'M': 0, 'F': 0},
        risk_factors[2]: {'M': 0, 'F': 0},
        risk_factors[3]: {'M': 0, 'F': 0},
        'All': {'M': 0, 'F': 0}
    },
    2: {
        risk_factors[0]: {'M': 0, 'F': 0},
        risk_factors[1]: {'M': 0, 'F': 0},
        risk_factors[2]: {'M': 0, 'F': 0},
        risk_factors[3]: {'M': 0, 'F': 0},
        'All': {'M': 0, 'F': 0}
    }
}

# Run simulations
for level in levels:

    for risk in risk_factors:

        inputs = change_inf(level = level, risk = risk, all_factors = False)
        model = spread.Spread_Model(inputs[0], inputs[1], 'archbold_test_results')
        model.simulation(10)
        rates[level][risk]['M'] = round(sum(model.cvd_count['M'].values())/
                                   (sum(model.person_years['M'].values())/1000), 4)
        rates[level][risk]['F'] = round(sum(model.cvd_count['F'].values())/
                                   (sum(model.person_years['F'].values())/1000), 4)

    inputs = change_inf(level = level)
    model = spread.Spread_Model(inputs[0], inputs[1], 'archbold_test_results')
    model.simulation(10)
    rates[level]['All']['M'] = round(sum(model.cvd_count['M'].values())/
                                   (sum(model.person_years['M'].values())/1000), 4)
    rates[level]['All']['F'] = round(sum(model.cvd_count['F'].values())/
                                   (sum(model.person_years['F'].values())/1000), 4) 
print(rates)