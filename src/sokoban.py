from search import Problem
from typing import List, Set, Tuple
#  __   __                  ____          _         _   _
#  \ \ / /__  _   _ _ __   / ___|___   __| | ___   | | | | ___ _ __ ___
#   \ V / _ \| | | | '__| | |   / _ \ / _` |/ _ \  | |_| |/ _ \ '__/ _ \
#    | | (_) | |_| | |    | |__| (_) | (_| |  __/  |  _  |  __/ | |  __/
#    |_|\___/ \__,_|_|     \____\___/ \__,_|\___|  |_| |_|\___|_|  \___|
class Sokoban(Problem):
    """
    A Sokoban problem instance for search algorithms.
    Come up with your own representation for the state.
    """

    def __init__(self, board: List[str]):
        """
        Initializes the Sokoban problem.
        :param board: List of strings, each string represent a row of the game board
        """
        super().__init__(board)

    def _get_player_pos(_,state: List[str]) -> Tuple:
        """gets the player position """
        for i, line in enumerate(state):
            pos = line.find("P")
            if pos == -1:
                continue
            return i,pos
    @staticmethod
    def sgn(x: int) -> int:
        if x == 0:
            return 0
        elif x < 0:
            return -1
        else:
            return 1
    def _valid_action(self,state,action,pos) -> bool:
        change_pos = tuple(map(sum,pos,action))
        char_at_pos = state[change_pos[0]][change_pos[1]]
        if char_at_pos == "%":
            return False
        elif change_pos.lower() == "b":
            return self._valid_action(self,state,tuple(map(lambda x: x + 1*Sokoban.sgn(x),action)),pos)
        else:
            return True
        

    def actions(self, state: List[str]) -> Set[tuple]:
        """Returns the list of valid actions from the current state."""
        player_pos = self._get_player_pos(state)
        possible_actions = [(-1,0),(0,1),(1,0),(0,-1)]
        playable_actions = []
        for delta in possible_actions:
            if self._valid_action(state,delta,player_pos):
                playable_actions.append(delta)
        return playable_actions

        

    def result(self, state, action):
        """Returns the resulting state after applying the action."""
        raise NotImplementedError

    def is_goal(self, state):
        """Checks if all boxes are on goal positions."""
        assert isinstance(state,str), "type is not a str"
        for line in state:
            if "." in line:
                return False
        return True
    
    def h(self, state):
        """Heuristic function for the problem. This should return a
        non-negative estimate of the cost to reach the goal from the
        given state."""
        score = 0
        for line in state:
            score+= line.count(".")
        return score
