# Phases are moderator-defined stages of a game. Usually, this is used for day 1, day 2, etc
# Phases are used by the retrospective votecounts to determine which votes are in the current phase
# Phases have a user-defined name and a post number that marks the beginning of the phase.

class phase:
  def __init__(self, postnum, phase_name):
    self.postnum = postnum
    self.phase_name = phase_name