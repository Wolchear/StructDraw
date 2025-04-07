from .algorithms.dssp import DSSP

ALGORITHMS = { "dssp": DSSP,
               "mkdssp": DSSP }
               
def get_algorithm(algorithm_name: str):
    algorithm_key = algorithm_name.lower()
    if algorithm_key in ALGORITHMS:
        return ALGORITHMS[algorithm_key](algorithm_name)
    raise ValueError(f"Algorithm {algorithm_name} is not supported!")
