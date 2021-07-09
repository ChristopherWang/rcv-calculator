#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

# Set number of voters
num_voters = 100000
# Give dummy IDs for each voter
voter_names = ['V' + str(i+1) for i in range(num_voters)]

# Set number of candidates
num_candidates = 10
# Give dummy names for each candidate
candidate_names = ['C' + str(i+1) for i in range(num_candidates)]
# Set the column names
column_names = ['choice_' + str(i+1) for i in range(num_candidates)]
# Set distribution of candidates (uniform distribution is given)
candidate_dist = [1/num_candidates] * num_candidates
candidate_cumsum = np.cumsum(candidate_dist)

# Randomly assign each voter (num_candidate) choices
sim_data = np.random.rand(num_voters, num_candidates)
## For each element of the sim data, map the random number to a candidate based on the given distribution
sim_voter_choices = [[candidate_names[np.argmax(candidate_cumsum > sim_data[i, j])] for j in range(num_candidates)] for i in range(num_voters)]

# Replace duplicate choices with "None"
for i in range(num_voters):
    ## For each voter create an empty set to fill with their choices
    voter_choice_set = set()
    found_dupe = False
    ## Iterate through all the choices sequentially
    for j in range(num_candidates):
        curr_choice = sim_voter_choices[i][j]
        ## If a duplicate has been found, replace the entry with 'None'
        ## Additionally replace all subsequent choices with 'None'
        if found_dupe:
            sim_voter_choices[i][j] = "None"
        elif curr_choice in voter_choice_set:
            sim_voter_choices[i][j] = "None"
            found_dupe = True
        ## Otherwise add the unique choice to the voter's choice set
        else:
            voter_choice_set.add(curr_choice)

# Create a data frame from the choice_list
sim_election_data = pd.DataFrame(sim_voter_choices, columns = column_names)
# Add voter_id as an index column
sim_election_data.insert(0, 'voter_id', voter_names)

# Export to CSV
sim_election_data.to_csv('ballots/sim_election_data.csv', 
                         index = False)