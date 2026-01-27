import pytest
from sokoban import Sokoban
from utils import file_to_board
import copy


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
        for name,board in boards.items():
            boards[name] = model.pre_process_board(board)
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


    # def test_result(self,setup_teardown):
    #     model, boards = setup_teardown
    #     solutions = {
    #         "sokoban_hard": {(0,-1):[['%', '%', '%', '%', '%', '%', '%', '%'], 
    #                                   ['%', '%', '%', ' ', ' ', ' ', '%', '%'], 
    #                                   ['%', 'P', ' ', 'b', ' ', ' ', '%', '%'], 
    #                                   ['%', '%', '%', ' ', 'b', '.', '%', '%'], 
    #                                   ['%', '.', '%', '%', 'b', ' ', '%', '%'], 
    #                                   ['%', ' ', '%', ' ', '.', ' ', '%', '%'], 
    #                                   ['%', 'b', ' ', 'B', 'b', 'b', '.', '%'], 
    #                                   ['%', ' ', ' ', ' ', '.', ' ', ' ', '%'], 
    #                                   ['%', '%', '%', '%', '%', '%', '%', '%']],

    #                          (0,1):[  ['%', '%', '%', '%', '%', '%', '%', '%'], 
    #                                   ['%', '%', '%', ' ', ' ', ' ', '%', '%'], 
    #                                   ['%', '.', ' ', 'p', 'b', ' ', '%', '%'], 
    #                                   ['%', '%', '%', ' ', 'b', '.', '%', '%'], 
    #                                   ['%', '.', '%', '%', 'b', ' ', '%', '%'], 
    #                                   ['%', ' ', '%', ' ', '.', ' ', '%', '%'], 
    #                                   ['%', 'b', ' ', 'B', 'b', 'b', '.', '%'], 
    #                                   ['%', ' ', ' ', ' ', '.', ' ', ' ', '%'], 
    #                                   ['%', '%', '%', '%', '%', '%', '%', '%']]},
    #         # "sokoban_mid": {},
    #         # "sokoban_simple": {},
    #         # "sokoban_trip_push": {}, 
    #         # "sokoban_solved": {},
    #     }
    #     similar_boards = (set(solutions.keys()).intersection(set(boards.keys())))

    #     assert len(similar_boards) > 0, "there are no similar board keys"
    #     for board_name in similar_boards:
    #         board = boards[board_name]
    #         actions = model.actions(board)
    #         for action in actions:
    #             result = model.result(board,action)
    #             solution = solutions[board_name][action]
                
    #             assert result == solution, "solutions are not similar"

    def test_result(self, setup_teardown):
        model, boards = setup_teardown
        def board_to_string(board):
            return "\n".join("".join(row) for row in board)

        solutions = {
            "sokoban_hard": {
                (0, -1): [
                    ['%', '%', '%', '%', '%', '%', '%', '%'],
                    ['%', '%', '%', ' ', ' ', ' ', '%', '%'],
                    ['%', 'P', ' ', 'b', ' ', ' ', '%', '%'],
                    ['%', '%', '%', ' ', 'b', '.', '%', '%'],
                    ['%', '.', '%', '%', 'b', ' ', '%', '%'],
                    ['%', ' ', '%', ' ', '.', ' ', '%', '%'],
                    ['%', 'b', ' ', 'B', 'b', 'b', '.', '%'],
                    ['%', ' ', ' ', ' ', '.', ' ', ' ', '%'],
                    ['%', '%', '%', '%', '%', '%', '%', '%'],
                ],
                (0, 1): [
                    ['%', '%', '%', '%', '%', '%', '%', '%'],
                    ['%', '%', '%', ' ', ' ', ' ', '%', '%'],
                    ['%', '.', ' ', 'p', 'b', ' ', '%', '%'],
                    ['%', '%', '%', ' ', 'b', '.', '%', '%'],
                    ['%', '.', '%', '%', 'b', ' ', '%', '%'],
                    ['%', ' ', '%', ' ', '.', ' ', '%', '%'],
                    ['%', 'b', ' ', 'B', 'b', 'b', '.', '%'],
                    ['%', ' ', ' ', ' ', '.', ' ', ' ', '%'],
                    ['%', '%', '%', '%', '%', '%', '%', '%'],
                ],
            },
            "sokoban_mid": {
                (0,1):[['%', '%', '%', '%', '%', '%', '%'], 
                       ['%', '%', '%', ' ', 'p', '.', '%'], 
                       ['%', ' ', 'b', ' ', '%', '.', '%'], 
                       ['%', ' ', ' ', 'b', 'b', ' ', '%'], 
                       ['%', '.', ' ', ' ', '%', ' ', '%'], 
                       ['%', ' ', ' ', ' ', 'b', '.', '%'], 
                       ['%', '%', '%', '%', '%', '%', '%']],

                (1,0):[['%', '%', '%', '%', '%', '%', '%'], 
                       ['%', '%', '%', ' ', ' ', '.', '%'], 
                       ['%', ' ', 'b', 'p', '%', '.', '%'], 
                       ['%', ' ', ' ', 'b', 'b', ' ', '%'], 
                       ['%', '.', ' ', ' ', '%', ' ', '%'], 
                       ['%', ' ', ' ', ' ', 'b', '.', '%'], 
                       ['%', '%', '%', '%', '%', '%', '%']]},
            "sokoban_simple": {
                (-1,0): [['%', '%', '%', '%', '%', '%'], 
                         ['%', ' ', ' ', ' ', ' ', '%'], 
                         ['%', 'b', '%', ' ', ' ', '%'], 
                         ['%', 'P', 'b', ' ', '.', '%'], 
                         ['%', ' ', '%', '%', '%', '%'], 
                         ['%', ' ', '%', '%', '%', '%'], 
                         ['%', '%', '%', '%', '%', '%']],
                (1,0): [['%', '%', '%', '%', '%', '%'], 
                         ['%', ' ', ' ', ' ', ' ', '%'], 
                         ['%', ' ', '%', ' ', ' ', '%'], 
                         ['%', 'B', 'b', ' ', '.', '%'], 
                         ['%', ' ', '%', '%', '%', '%'], 
                         ['%', 'p', '%', '%', '%', '%'], 
                         ['%', '%', '%', '%', '%', '%']],
                },
            "sokoban_trip_push": {
                (0,1): [['%', '%', '%', '%', '%', '%'], 
                        ['%', 'b', ' ', ' ', '%', '%'], 
                        ['%', ' ', 'p', 'B', 'B', '%'], 
                        ['%', 'b', ' ', ' ', '%', '%'], 
                        ['%', ' ', ' ', ' ', ' ', '%'], 
                        ['%', '%', '%', '%', '%', '%']],
                (1,0):[['%', '%', '%', '%', '%', '%'], 
                        ['%', 'b', ' ', ' ', '%', '%'], 
                        ['%', ' ', 'b', 'B', '.', '%'], 
                        ['%', 'p', ' ', ' ', '%', '%'], 
                        ['%', 'b', ' ', ' ', ' ', '%'], 
                        ['%', '%', '%', '%', '%', '%']],
            }
        }

        similar_boards = set(solutions) & set(boards)
        assert similar_boards, "there are no similar board keys"

        with open("test_results.txt", "w") as f:
            for board_name in similar_boards:
                board = copy.deepcopy(boards[board_name])
                actions = model.actions(board)
                print(board)
                for action in actions:
                    board = copy.deepcopy(boards[board_name])
                    
                    # if action == (0,1):
                    #     continue
                    result = model.result(board, action)
                    solution = solutions[board_name][action]
                    if result != solution:
                        f.write(f"\n=== Board: {board_name} | Action: {action} ===\n")
                        f.write("\nBoard:\n")
                        f.write(board_to_string(board))
                        f.write("\nExpected:\n")
                        f.write(board_to_string(solution))
                        f.write("\n\nActual:\n")
                        f.write(board_to_string(result))
                        f.write("\n" + "=" * 40 + "\n")

                    assert result == solution, (
                        f"Mismatch for board {board_name}, action {action}. "
                        f"See test_results.txt for details."
                    )


    
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