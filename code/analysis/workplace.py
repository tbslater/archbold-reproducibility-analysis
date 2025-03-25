# Code to reproduce table 6

# Import files 
import agent 
import network 
import parameters
import intervention

# Import packages
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def assign_intervention(agents, adoption):
    '''
    Function to assign agents to the workplace intervention group. 

    PARAMS
    ------
    agents: list of agents generated from network.py [list]
    adoption: fraction of agents to include in the intervention [float]

    OUTPUT
    ------
    None
    '''

    if adoption == 1:
        for agent in agents: # set all to the intervention
            agent.intervention = True 

    elif adoption >= 0 and adoption < 1:  
        
        target_no = int(len(agents) * adoption) # target number of agents
        retained = set(agents) # agents currently not assigned to the intervention
        assigned = set() # agents currently assigned to the intervention

        while len(assigned) < target_no: # while the target numbr has not been reached

            agent = random.choice(tuple(retained)) # choose a random agent
            agent.intervention = True # assign to intervention group
            assigned.update([agent]) # update set of assigned agents
            if agent.workplace: # if agent has workplace contacts
                for x in agent.workplace: # for each of these contacts
                    x.intervention = True # assign to intervention group
                    assigned.update(agent.workplace) # update set of assigned agents
            retained = retained.difference(assigned) # update list of retained agents

    else: 
        print('ERROR: Adoption value must be between 0 and 1.')

def get_intervention_inf(influences, risk):
    '''
    Function to change the workplace influence. 

    PARAMS
    ------
    influences: influences for all relationships/interventions [dict]
    risk: risk factor(s) to change Diet/Inactivity/Both [str]

    OUTPUT
    ------
    dict: dictionary of influences 
    '''

    if risk == 'Diet':

        for i in range(1,5):
            # Set workplace influence to half the friendship influence
            influences['Workplace'][i]['Diet'][0] = 0.5 * influences['Friendship']['Diet'][0]
            influences['Workplace'][i]['Diet'][1] = 0.5 * influences['Friendship']['Diet'][1]

    if risk == 'Inactivity':

        for i in range(1,5):
            # Set workplace influence to half the friendship influence
            influences['Workplace'][i]['Inactivity'][0] = 0.5 * influences['Friendship']['Inactivity'][0]
            influences['Workplace'][i]['Inactivity'][1] = 0.5 * influences['Friendship']['Inactivity'][1]

    if risk == 'Both': 

        for i in range(1,5): 
            # Set workplace influence to half the friendship influence
            influences['Workplace'][i]['Diet'][0] = 0.5 * influences['Friendship']['Diet'][0]
            influences['Workplace'][i]['Diet'][1] = 0.5 * influences['Friendship']['Diet'][1]
            influences['Workplace'][i]['Inactivity'][0] = 0.5 * influences['Friendship']['Inactivity'][0]
            influences['Workplace'][i]['Inactivity'][1] = 0.5 * influences['Friendship']['Inactivity'][1]

    return influences

rates = {
        'Diet': {
            0: {'M': 0, 'F': 0},
            0.25: {'M': 0, 'F': 0},
            0.5: {'M': 0, 'F': 0},
            0.75: {'M': 0, 'F': 0},
            1: {'M': 0, 'F': 0}
        },
        'Inactivity': {
            0: {'M': 0, 'F': 0},
            0.25: {'M': 0, 'F': 0},
            0.5: {'M': 0, 'F': 0},
            0.75: {'M': 0, 'F': 0},
            1: {'M': 0, 'F': 0}
        },
        'Both': {
            0: {'M': 0, 'F': 0},
            0.25: {'M': 0, 'F': 0},
            0.5: {'M': 0, 'F': 0},
            0.75: {'M': 0, 'F': 0},
            1: {'M': 0, 'F': 0}
        }
}

adoption_rates = [0, 0.25, 0.5, 0.75, 1]
risk_factors = ['Diet', 'Inactivity', 'Both']

N = 350000
horizon = 10
params = 'scenarios_21' # change to scenarios_4 for mean workplace size of 4

for adoption in adoption_rates:
    number = 0
        
    for risk in risk_factors:

        sim_params = parameters.Parameters(params)
        sim_network = network.Network(sim_params)
        sim_agents = sim_network.generate_agents(N)
        assign_intervention(sim_agents, adoption)
        intervention_inf = get_intervention_inf(sim_params.get_inf_by_rel(), risk = risk)
        model = intervention.Spread_Model(sim_agents, sim_params.get_inf_by_rel(), intervention_inf, 'archbold_test_results')
        model.simulation(horizon)
        rates[risk][adoption]['M'] = round(sum(model.cvd_count['M'].values())/
                                     (sum(model.person_years['M'].values())/1000), 4)
        rates[risk][adoption]['F'] = round(sum(model.cvd_count['F'].values())/
                                     (sum(model.person_years['F'].values())/1000), 4)

        number = number + 1
        print('Simulation number {} complete'.format(number))
        
print(rates)