#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

# Load specified ballot data
ballot_data = pd.read_csv('ballots/sim_election_data2.csv')

# Create a tally dictionary to track the voter's choices
candidate_vote_dict = {}

# Iterate through the rows of the ballot data
for i in range(ballot_data.shape[0]):
    voter_first_choice = ballot_data.iloc[i, 1]
    if voter_first_choice in candidate_vote_dict:
        candidate_vote_dict[voter_first_choice].append([i, 1])
    else:
        candidate_vote_dict[voter_first_choice] = [[i, 1]]

# Tally the votes
tally_results = []
for key in candidate_vote_dict:
    tally_results.append([key, len(candidate_vote_dict[key])])
    
# Convert to dataframe and calculate vote share
tally_results = pd.DataFrame(tally_results, columns = ['Candidate', 'Num_Votes'])
tally_results['Vote_Share'] = tally_results['Num_Votes']/(sum(tally_results['Num_Votes']))

# Print results
print(tally_results)

# Iterate the ranked choice vote algorithm
## If a majority is not found, begin to check the next choices of the voters
while max(tally_results['Vote_Share']) < 0.5:
    # Print some extra space for 
    print()

    ## Get the identity of the candidate with the least votes
    dropped_cand = tally_results['Candidate'][tally_results['Num_Votes'].idxmin()]
    
    print("Dropping candiate: "+str(dropped_cand))
    
    ## Pop the voters of the dropped candidate from candidate_vote_dict
    dropped_voters = candidate_vote_dict.pop(dropped_cand)
    
    ## Iterate through the dropped_voters and find their subsequent choice
    for voter in dropped_voters:
        ## Make sure the voter has not reached the end of the ballot
        if voter[1]+1 < ballot_data.shape[1]:
            ## Find the voter's next choice
            voter_next_choice = ballot_data.iloc[voter[0], voter[1]+1]
            ## Drop if -1
            if voter_next_choice == -1:
                continue
            ## Add to tally if the next choice is still a valid candidate
            elif voter_next_choice in candidate_vote_dict:
                candidate_vote_dict[voter_next_choice].append([voter[0], voter[1]+1])
            ## Otherwise add them back into dropped_voters to check their next choice
            else:
                dropped_voters.append([voter[0], voter[1]+1])
    
    ## Tally the votes
    tally_results = []
    for key in candidate_vote_dict:
        tally_results.append([key, len(candidate_vote_dict[key])])
    
    ## Convert to dataframe and calculate vote share
    tally_results = pd.DataFrame(tally_results, columns = ['Candidate', 'Num_Votes'])
    tally_results['Vote_Share'] = tally_results['Num_Votes']/(sum(tally_results['Num_Votes']))
    
    # Print results
    print(tally_results)