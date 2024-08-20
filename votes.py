# This file contains functions for working with votes.

# get_votes_by_postnum() takes a post number and does the following:
# 1 - Find the phase with the largest associated post number that is less than or equal to the given post number.
# 2 - Retrieve all votes that were cast between that phase's start and the given post number.
# 3 - Return the list of votes.
# Aliases are checked here - if a vote is placed for an alias, the vote is recorded for the player's main username.
def get_votes_by_postnum(postnum, game):
    return NotImplemented

# get_votes_by_voter() retrieves all votes that were cast by the given voter, and returns them as a list.
# Aliases are checked here - if a vote is placed for an alias, the vote is recorded for the player's main username.

def get_votes_by_voter(voter, game):
    return NotImplemented

# get_votes_by_target() retrieves all votes that were cast for the given target, and returns them as a list.
# Aliases are checked here - if a vote is placed for an alias, the vote is recorded for the player's main username.

def get_votes_by_target(target, game):
    return NotImplemented

# check_hammer() takes a list of votes and checks if any player has been voted by a majority of living players.
# If a hammer has occured, the function returns the player who was hammered and a list of all votes placed up to and including the hammer.
# If no hammer has occured, the function returns None.
# Aliases are checked here - if a vote is placed for an alias, the vote is recorded for the player's main username.

def check_hammer(votes):
    return NotImplemented

# get_votecount() takes a postnum and returns a dictionary of players and the votes for them. Also returns true if a hammer has occurred, false otherwise.
# The dictionary is sorted by the number of voters, with the player who has received the most votes first.
# If there is a tie, the dictionary is sorted alphabetically by key (player name).
# However, "not voting" is always listed last, regardless of the number of votes.
def get_votecount(postnum, game):
    # Start with a list of vote objects (called "votes"), obtained by get_votes_by_postnum
    # Check for a hammer in the list. If one occurs, replace the list of votes with the sublist up to and including the hammer

    # Create a new list of votes (called "votecount"), initially sorted alphabetically by player, where each player is listed as "not voting"
    # For each vote in the list of votes:
        # Remove the voter's current vote from the votecount
        # Append the voter's new vote to the votecount

    # Create a new dictionary (called "votecount_dict") by iterating through the votecount list. This dictionary has:
    # KEY: Player name
    # VALUE: List of votes (voter, target, url, postnum) for that player
    
    # Sort the dictionary by the number of voters, with the player who has received the most votes first
    # If there is a tie, sort the dictionary alphabetically by key (player name)
    # Return the sorted dictionary and whether a hammer has occurred 
    return NotImplemented


# There will need to be vote formatting happening somewhere. This will either be here (where a function will return an HTML-formatted votecount) 
# or in the actual frontend, if it's able to accept a dictionary and work with it.