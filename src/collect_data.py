import time
import click
from sokoban import Sokoban
from search import astar_search, ucs_search
from utils import display_solution
from tqdm import tqdm
import json


def main(input_files):
    report = {
        "A Star": {},
        "Uniform Cost Search": {},
    }
    for input_file in tqdm(input_files):
        board = []
        with open(input_file, "r") as f:
            for l in f:
                if l:
                    board.append(l)

        # board is a list of strings containing rows in the input file, you need to parse it into your state representation.
        problem = Sokoban(board)


        start_time = time.time()
        astar_sub_report = {"nodes_expanded": None,"frontier": None}
        ucs_sub_report = {"nodes_expanded": None,"frontier": None}
        result_a_star = astar_search(problem,report = astar_sub_report)
        astar_sub_report["time"] = time.time() - start_time
        start_time = time.time()
        result_ucs = ucs_search(problem,report = ucs_sub_report)
        ucs_sub_report["time"] = time.time() - start_time
        
        soln_a_star = result_a_star.solution()
        soln_ucs = result_ucs.solution()
        move_to_str = {
            (-1, 0): "U",
            ( 0, 1): "R",
            ( 1, 0): "D",
            ( 0,-1): "L",
        }
        soln_a_star = list(map(lambda x: move_to_str[x],soln_a_star))
        soln_a_star = "".join(soln_a_star)
        soln_ucs = list(map(lambda x: move_to_str[x],soln_ucs))
        soln_ucs = "".join(soln_ucs)

        astar_sub_report["output"] = soln_a_star
        astar_sub_report["output length"] = len(soln_a_star)
        ucs_sub_report ["output"] = soln_ucs
        ucs_sub_report["output length"] = len(soln_a_star)

        report["A Star"][input_file] = astar_sub_report
        report["Uniform Cost Search"][input_file] = ucs_sub_report

    with open("results.json", "w") as f:
        json.dump(report, f)
            
        


if __name__ == "__main__":
    files = [
        "boards/sokoban_simple.txt",
        "boards/sokoban_mid.txt",
        "boards/sokoban_hard.txt",
        ]
    main(files)
