import time
import click
from sokoban import Sokoban
from search import astar_search, ucs_search
from utils import display_solution


def main(input_files):
    for input_file in input_files:
        board = []
        with open(input_file, "r") as f:
            for l in f:
                if l:
                    board.append(l)

        # board is a list of strings containing rows in the input file, you need to parse it into your state representation.
        problem = Sokoban(board)

        

        start_time = time.time()
        # result = astar_search(problem)
        result = ucs_search(problem)
        print("Search completed in {:.2f} seconds.".format(time.time() - start_time))

        if not result:
            print("No solution found.")
            soln = []
        else:
            # Depending on your Sokoban formulation, you may need to convert your solution format to fulfill the output requirement.
            soln = result.solution()
            display_solution(problem,soln)
            move_to_str = {
                (-1, 0): "U",
                ( 0, 1): "R",
                ( 1, 0): "D",
                ( 0,-1): "L",
            }
            soln = list(map(lambda x: move_to_str[x],soln))
            soln = "".join(soln)
            
            print("Solution found with {} moves.".format(len(soln)))
        print("".join(soln))
        with open("solution.txt", "w") as f:
            f.write("".join(soln))


if __name__ == "__main__":
    main()
