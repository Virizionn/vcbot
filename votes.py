# This file contains a function to calculate the votecount for a given postnum in a given game.

import database

def get_votecount(game, postnum):
    current_phase = None

    #identify what phase the post is in
    phases = database.get_phases(game)
    for phase in reversed(phases):
        if postnum >= phase['postnum']:
            current_phase = phase
            break
    
    votes = database.get_votes_by_range(game, current_phase['postnum'], postnum)
    
    #temp dict. Format is {voter: target}        
    working_votes = {}

    for vote in votes:
        working_votes[vote['voter']] = vote
    #end result is a dictionary representing the most recent votes
    
    #check for aliases
    aliases = database.get_aliases()

    for voter in working_votes.keys():
        target = working_votes[voter]['target']
        if target.lower() in aliases.keys():
            working_votes[voter]['target'] = aliases[target.lower()]
    
    #dictionary representing the final votecount. Format: {target: [vote, vote, vote]}
    votecount = {}
    for voter in working_votes.keys():
        target = working_votes[voter]['target']
        if target not in votecount.keys():
            votecount[target] = [working_votes[voter]]
        else:
            votecount[target].append(working_votes[voter])
    
    #check hammer
    #Add this feature when we have a way of getting a list of players

    #format votecount
    
    output = "{} Votecount:\n".format(current_phase['phase'])
    #sort the votecount by number of votes, high to low
    votecount = dict(sorted(votecount.items(), key=lambda item: len(item[1]), reverse=True))
    for target in votecount.keys():
        output += "{}: ".format(target)
        for vote in votecount[target]:
            output += "{}, ".format(vote['voter'])
        output = output[:-2] + "\n"

    return(output)