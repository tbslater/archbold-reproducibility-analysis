# Code to reproduce figure 2

import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import agent 
import network 
import parameters
import spread

def obtain_incident_rates(model):
    '''
    FUNCTION TO OBTAIN M/F INCIDENT RATES FOR FIGURE 2 REPRODUCTION

    PARAMS 
    model: Spread_Model class object [class]

    OUTPUT
    rates: dictionary of M/F incident rates [dict]
    '''

    rates = {
        'Male': sum(model.cvd_count['M'].values()),
        'Female': sum(model.cvd_count['F'].values())
    }

    return rates

random.seed(0)

pop_sizes = np.append([3.5], range(2,13)) * 100000

incident_rates = {}

for N in pop_sizes:

    mod = run_simulation(N, 10)
    incident_rates[N] = obtain_incident_rates(mod)

    print('Iteration {}K complete'.format(N/1000))

male_ir = []
female_ir = []
for i in pop_sizes:
    male_ir.append(incident_rates[i]['Male'])
    female_ir.append(incident_rates[i]['Female'])

male_ir.insert(2, male_ir.pop(0))
print(male_ir)
female_ir.insert(2, female_ir.pop(0))
print(female_ir)
x = list(pop_sizes)
x.insert(2, x.pop(0))
y = np.array(x)

plt.plot(y/1000, female_ir, ':o', label = "Women", color = 'orange')
plt.plot(y/1000, male_ir, '--+', label = "Men", color = 'teal')
plt.legend()
plt.xlabel('Population size (1000s)')
plt.ylabel('Mean Incident Rate')
plt.show()