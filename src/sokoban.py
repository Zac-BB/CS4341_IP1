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
        self.bsf_calls = 0
        board = self.pre_process_board(board)
        super().__init__(board)

    def pre_process_board(self,board):
        new_board = [None]*len(board)
        for i,line in enumerate(board):
            line = line.replace("\n","")
            new_board[i] = list(line)
        i,j = self._get_player_pos(new_board)
        new_board[i][j] = "p"
        new_board = tuple(tuple(row) for row in new_board)
        return new_board
    
    def _get_player_pos(_,state: List[str]) -> Tuple:
        """gets the player position """
        for i, line in enumerate(state):
            for j in range(len(line)):
                char = line[j]
                if char in "pP":
                    return i,j
        return None,None
    
    def _valid_action(self,state,action,pos) -> bool:
        change_pos = (pos[0] + action[0],pos[1] + action[1])
        char_at_pos = state[change_pos[0]][change_pos[1]]
        if char_at_pos.lower() == "b":
            change_pos = (change_pos[0] + action[0],change_pos[1] + action[1])
            char_at_pos = state[change_pos[0]][change_pos[1]]
        if char_at_pos in " .":
            return True
        else:
            return False

        

    def actions(self, state: tuple[tuple[str]]) -> Set[tuple]:
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
        state = list(list(row) for row in state)
        player_pos = self._get_player_pos(state)
        assert self._valid_action(state,action,player_pos)
        def move(state,position,action,fill,layer = 0):
            
            change_pos = (position[0] + action[0],position[1] + action[1])
            char_at_pos = state[change_pos[0]][change_pos[1]]
            fill = fill.upper() if (char_at_pos.isupper() or char_at_pos == ".") else fill.lower()
            state[change_pos[0]][change_pos[1]] = fill
            if char_at_pos in "Bb":
                state = move(state,change_pos,action,char_at_pos,layer+1)
            return state

        put = " "
        if state[player_pos[0]][player_pos[1]].isupper():
            put = "."
        state[player_pos[0]][player_pos[1]] = put
        state = move(state,player_pos,action,"p")
        
        state = tuple(tuple(row) for row in state)
        return state

    def is_goal(self, state):
        """Checks if all boxes are on goal positions."""
        for line in state:
            if "b" in line:
                return False
        return True
    
    def h(self, state):
        """Heuristic function for the problem. This should return a
        non-negative estimate of the cost to reach the goal from the
        given state."""

        """
        Ideas: 
        -dist to the goal
        -if there is a block that is on the wall that cant be recovered 
        -make sure that the blocks dont overlap on dist to goal
        """
        
        def neighbors_of_4(pos):
            deltas = [(-1,0),(0,1),(1,0),(0,-1)]
            valid = []
            for delta in deltas:
                new_pos = (pos[0]+delta[0],pos[1]+delta[1])
                if state[new_pos[0]][new_pos[1]] in " .BbpP":
                    valid.append(new_pos)
            return valid
        def add_vecs(a,b):
            return a[0]+b[0],a[1]+b[1]
        def cooked():
            for i,line in enumerate(state):
                for j, char in enumerate(line):
                    if char == "b":
                        deltas = [(-1,0),(0,1),(1,0),(0,-1)]
                        sum = [0,0]
                        accepted = []
                        for delta in deltas:
                            result = add_vecs([i,j],delta)
                            if state[result[0]][result[1]] != "%":
                                accepted.append(delta)
                                sum = add_vecs(sum,delta)
                        if abs(sum[0]) == 1 and abs(sum[1]) == 1:
                            return float('inf')
            return 0

        def bsf(start):
            from collections import deque
            queue = deque()
            queue.append((start,0))
            visited = set()

            while queue:
                pos,score = queue.popleft()
                char = state[pos[0]][pos[1]]
                is_dot = state[pos[0]][pos[1]] == "."
                is_on_dot = state[pos[0]][pos[1]].isupper()
                if is_dot or is_on_dot:
                    return score
                children = neighbors_of_4(pos)

                for child in children:
                    if child not in visited:
                        queue.append((child,score+1))
                        visited.add(child)
            

        bsf_score = 0
        for i,line in enumerate(state):
            for j, char in enumerate(line):
                if char == "b":
                    bsf_score= bsf((i,j))
                
        is_cooked = cooked()
        self.bsf_calls +=1
        # print(f"{self.bsf_calls}: {type(bsf_score)}")
        # print)
        
        return max(is_cooked,bsf_score)
