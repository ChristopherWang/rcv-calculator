#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

# Set number of votes
num_voters = 100000
# Set number of candiates
num_candidates = 10
# Set the column names
column_names = ['choice_' + str(i+1) for i in range(num_candidates)]

# Randomly assign each voter (num_candidate) choices
simulated_ballot_data = np.random.randint(0,num_candidates,size=(num_voters,num_candidates))

# Replace duplicate choices with -1 (effectively "No Value")
for i in range(num_voters):
    ## For each voter create an empty set to fill with their choices
    voter_choice_set = set()
    found_dupe = False
    ## Iterate through all the choices sequentially
    for j in range(num_candidates):
        curr_choice = simulated_ballot_data[i,j]
        ## If a duplicate has been found, replace the entry with '-1'
        ## Additionally replace all subsequent choices with '-1'
        if found_dupe:
            simulated_ballot_data[i,j] = -1
        elif curr_choice in voter_choice_set:
            simulated_ballot_data[i,j] = -1
            found_dupe = True
        ## Otherwise add the unqiue choice to the voter's choice set
        else:
            voter_choice_set.add(curr_choice)

# Convert to DataFrame
sim_ballot = pd.DataFrame(simulated_ballot_data, columns = column_names)

# Export to CSV
sim_ballot.to_csv('ballots/sim_ballot.csv')