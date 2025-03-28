# Code to reproduce table 3 and figure 1

import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import agent 
import network 
import parameters
import spread

def obtain_metrics(model):
    """
    FUNCTION TO OBTAIN METRICS FROM TABLE 3 IN ARCHBOLD ET AL., 2024

    PARAMS:
    model: Spread_Model class object [class]

    OUTPUT:
    metrics: array of metric values [np.array]
    """

    # Age categories 
    age_bins = ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', \
	            '55-59', '60-64', '65-69', '70-74', '75-79', '80-84']
    n = len(age_bins)
    
    # Empty arrays for storage 
    incident_cases_m = np.zeros(n)
    incident_cases_f = np.zeros(n)
    person_years_m = np.zeros(n)
    person_years_f = np.zeros(n)
    rate_m = np.zeros(n)
    rate_f = np.zeros(n)
    
    # Extract metrics for each age category 
    for i in range(len(age_bins)):
        incident_cases_m[i] = model.cvd_count['M'][age_bins[i]]
        incident_cases_f[i] = model.cvd_count['F'][age_bins[i]]
        person_years_m[i] = model.person_years['M'][age_bins[i]]
        person_years_f[i] = model.person_years['F'][age_bins[i]]
        rate_m[i] = (incident_cases_m[i] / (person_years_m[i] / 1000))
        rate_f[i] = (incident_cases_f[i] / (person_years_f[i] / 1000))

    # Merge by column into one array #
    metrics = np.vstack((incident_cases_m, incident_cases_f, person_years_m, 
                         person_years_f, rate_m, rate_f))
    
    return metrics  

def run_simulation(pop_size, horizon):
    '''
    FUNCTION TO RUN A SIMULATION REPEAT

    PARAMS: 
    pop_size: number of agents [int]
    horizon: years to simulate for [int]

    OUTPUT: 
    model: model class [class]
    '''

    # Generate agents
    sim_params = parameters.Parameters('scenarios_21')
    sim_network = network.Network(sim_params)
    sim_agents = sim_network.generate_agents(pop_size)

    # Run model
    model = spread.Spread_Model(sim_agents, sim_params.get_inf_by_rel(), 'archbold_test_results')
    sim_run = model.simulation(horizon)

    return model

def print_simulation_metrics(ic_m, ic_f, py_m, py_f, rate_m, rate_f):
    '''
    FUNCTION TO PRINT THE SIMULATION METRICS IN A FORMAT SIMILAR TO TABLE 3

    PARAMS: 
    ic_m: male incident cases [np.array]
    ic_f: female incident cases [np.array]
    py_m: male person years [np.array]
    py_f: female person years [np.array]
    rate_m: male rates [np.array]
    rate_f: female rates [np.array]
    '''
    
    age_bins = ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', \
      '55-59', '60-64', '65-69', '70-74', '75-79', '80-84']
    
    # Print female simulation metrics 
    print('Women:')		
    print('age group', '\t', 'incidents', '\t', 'person years', '\t', 'rate per 1000 person years')
    for age in range(len(age_bins)):
        print(age_bins[age], '\t\t', ic_f[age], '\t\t', py_f[age], '\t\t', rate_f[age])
    total_incidents_f = round(sum(ic_f),4)
    total_person_years_f = round(sum(py_f),4)
    print('total', '\t\t', total_incidents_f, '\t\t', total_person_years_f, '\t\t', "{:.2f}".format(round((total_incidents_f / (total_person_years_f / 1000)),4)))
    print()
    
    # Print male simulation metrics
    print('Men:')
    print('age group', '\t', 'incidents', '\t', 'person years', '\t', 'rate per 1000 person years')
    for age in range(len(age_bins)):
        print(age_bins[age], '\t\t', ic_m[age], '\t\t', py_m[age], '\t\t', rate_m[age])
    total_incidents_m = round(sum(ic_m),4)
    total_person_years_m = round(sum(py_m),4)
    print('total', '\t\t', total_incidents_m, '\t\t', total_person_years_m, '\t\t', "{:.2f}".format(round((total_incidents_m / (total_person_years_m / 1000)),4)))
    print()

N = 10 # no. of simulation repeats
POP_SIZE = 350000 # population size
HORIZON = 10 # years to simulate

random.seed(0) # set seed for reproducibility

metrics = obtain_metrics(run_simulation(POP_SIZE, HORIZON)) # run sim.

storage = {'cases_m': metrics[0], 'cases_f': metrics[1], 'years_m': metrics[2],
    'years_f': metrics[3], 'rate_m': metrics[4], 'rate_f': metrics[5]} # store metrics

names = ['cases_m', 'cases_f', 'years_m', 'years_f', 'rate_m', 'rate_f']

for i in range(1,N): # for each repeat

    random.seed(i) # random seed
    metrics = obtain_metrics(run_simulation(POP_SIZE, HORIZON))

    for j in range(len(names)): # for each metric
        storage[names[j]] = np.vstack((storage[names[j]], metrics[j]))

averages = {'cases_m': np.zeros(12), 'cases_f': np.zeros(12), 'years_m': np.zeros(12),
    'years_f': np.zeros(12), 'rate_m': np.zeros(12), 'rate_f': np.zeros(12)}

for i in range(len(names)): 
    
    for j in range(12):
        averages[names[i]][j] = round(np.mean(storage[names[i]][:,j]),4)

print_simulation_metrics(averages['cases_m'], averages['cases_f'], averages['years_m'], 
                         averages['years_f'], averages['rate_m'], averages['rate_f'])

# Hippisley-Cox rates
hipp_cox_f = np.array([0.24,0.49,1.02,1.90,3.20,4.83,7.47,11.36,17.13,25.08,35.11,48.02,6.19])
hipp_cox_m = np.array([0.40,0.99,2.12,3.99,6.65,9.86,14.18,19.69,26.55,35.48,45.16,58.29,8.18])

# Calculate differences
model_rates_f = np.append(averages['rate_f'], # by age
                          np.array((sum(averages['cases_f']) / (sum(averages['years_f']) / 1000)))) # total
model_rates_f = np.append(averages['rate_m'], # by age
                          np.array((sum(averages['cases_m']) / (sum(averages['years_m']) / 1000)))) # total
diff_f = model_rates_f - hipp_cox_f
diff_m = model_rates_m - hipp_cox_m

# Print the rates
def rates_table(hipp_cox_f, hipp_cox_m, model_rates_f, model_rates_m):
    '''
    FUNCTION TO PRINT THE RATES IN A FORMAT SIMILAR TO TABLE 4

    PARAMS: 
    hipp_cox_f: female Hippisley-Cox et al. rates [np.array]
    hipp_cox_m: male Hippisley-Cox et al. rates   [np.array]
    model_rates_f: female simulation model rates [np.array]
    model_rates_m: male simulation model rates [np.array]
    '''
    
    age_bins = ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', \
      '55-59', '60-64', '65-69', '70-74', '75-79', '80-84']
    
    # Print female simulation metrics 
    print('Women:')		
    print('age group', '\t', 'Hippisley-Cox et al. Observed Rate', '\t', 'Modelled Rate', '\t', 'Difference')
    for age in range(len(age_bins)):
        print(age_bins[age], '\t\t', hipp_cox_f[age], '\t\t', model_rates_f[age], '\t\t', diff_f[age])
    total_hipp_f = round(sum(hipp_cox_f),4)
    total_model_f = round(sum(model_rates_f),4)
    print('total', '\t\t', total_hipp_f, '\t\t', total_model_f, '\t\t', "{:.2f}".format(round((total_model_f - total_hipp_f),4)))
    print()
    
    # Print male simulation metrics 
    print('Men:')		
    print('age group', '\t', 'Hippisley-Cox et al. Observed Rate', '\t', 'Modelled Rate', '\t', 'Difference')
    for age in range(len(age_bins)):
        print(age_bins[age], '\t\t', hipp_cox_m[age], '\t\t', model_rates_m[age], '\t\t', diff_m[age])
    total_hipp_m = round(sum(hipp_cox_m),4)
    total_model_m = round(sum(model_rates_m),4)
    print('total', '\t\t', total_hipp_m, '\t\t', total_model_m, '\t\t', "{:.2f}".format(round((total_model_m - total_hipp_m),4)))
    print()

rates_table(hipp_cox_f, hipp_cox_m, model_rates_f, model_rates_m)

# Produce figure 1
age_bins = ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', \
            '55-59', '60-64', '65-69', '70-74', '75-79', '80-84']

diffs_by_sex = {
    'Women': diff_f[range(len(age_bins))].tolist(),
    'Men': diff_m[range(len(age_bins))].tolist()
}

x = np.arange(len(age_bins))  # the label locations
width = 0.4  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for sex, value in diffs_by_sex.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, value, width, label=sex)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Difference in Mean Incident Rate')
ax.set_xticks(x + width, age_bins)
ax.legend(loc='upper left', ncols=1)

plt.show()