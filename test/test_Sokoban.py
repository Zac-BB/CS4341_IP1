import pytest
from sokoban import Sokoban
from utils import file_to_board

class TestSokoban:
    
    @pytest.fixture
    def setup_teardown(self):
        
        boards = { 
            "sokoban_hard": file_to_board("boards/sokoban_hard.txt"),
            "sokoban_mid": file_to_board("boards/sokoban_mid.txt"),
            "sokoban_simple": file_to_board("boards/sokoban_simple.txt"),
            "sokoban_trip_push": file_to_board("boards/sokoban_trip_push.txt"),
            "sokoban_solved": file_to_board("boards/sokoban_solved.txt"),
        }
        model = Sokoban(boards[list(boards.keys())[0]])
        return model,boards

    def test_get_player_pos(self,setup_teardown):
        model, boards = setup_teardown
        solution = {
            "sokoban_hard": (2,2),
            "sokoban_mid": (1,3),
            "sokoban_simple": (4,1),
            "sokoban_trip_push": (2,1), 

        }
        similar_boards = (set(solution.keys()).intersection(set(boards.keys())))

        assert len(similar_boards) > 0, "there are no similar board keys"
        for board_name in similar_boards:
            board = boards[board_name]
            calculated_pos = model._get_player_pos(board)
            print(calculated_pos)
            assert calculated_pos == solution[board_name]
    
    def test_valid_action(self,setup_teardown):
        model, boards = setup_teardown
        state = boards["sokoban_trip_push"]
        player_pos = model._get_player_pos(state)
        possible_actions = [(-1,0),(0,1),(1,0),(0,-1)]
        solutions = [False,True,True,False]
        for i,delta in enumerate(possible_actions):
            validity = model._valid_action(state,delta,player_pos)
            assert validity is solutions[i], f"validity: {validity}, solution: {solutions[i]}"
                
        

    def test_actions(self,setup_teardown):
        model, boards = setup_teardown
        solutions = {
            "sokoban_hard": [(0,-1),(0,1)],
            "sokoban_mid": [(0,1),(1,0)],
            "sokoban_simple": [(-1,0),(1,0)],
            "sokoban_trip_push": [(0,1),(1,0)], 
        }
        similar_boards = (set(solutions.keys()).intersection(set(boards.keys())))

        assert len(similar_boards) > 0, "there are no similar board keys"
        for board_name in similar_boards:
            solution = solutions[board_name]
            state = boards[board_name]
            moves  = model.actions(state)
            assert set(moves) == set(solution), f"returned moves: {moves}, true moves {solution}"


    def test_result(self):
        pass
    
    def test_is_goal(self,setup_teardown):
        model, boards = setup_teardown
        solutions = {
            "sokoban_hard": False,
            "sokoban_mid": False,
            "sokoban_simple": False,
            "sokoban_trip_push": False, 
            "sokoban_solved": True,
        }
        similar_boards = (set(solutions.keys()).intersection(set(boards.keys())))

        assert len(similar_boards) > 0, "there are no similar board keys"
        for board_name in similar_boards:
            board = boards[board_name]
            solution = solutions[board_name]
            result = model.is_goal(board)
            assert result == solution, f"failed on: {board_name} -> result: {result},solution {solution} "
        

    def test_h(self,setup_teardown):
        model, boards = setup_teardown
        for board_name,state in boards.items():
            result = model.h(state)
            assert result >= 0, f"the state evaluation is negative for {board_name}"