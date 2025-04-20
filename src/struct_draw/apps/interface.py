from typing import Dict, Optional

from .algorithms.dssp import DSSP
from .algorithms.stride import Stride

ALGORITHMS = { "dssp": DSSP,
               "mkdssp": DSSP,
               "stride": Stride }
               
def get_algorithm(algorithm_name: str, ss_translation: Optional[Dict[str,str]] = None):
    algorithm_key = algorithm_name.lower()
    if algorithm_key in ALGORITHMS:
        return ALGORITHMS[algorithm_key](algorithm_name, ss_translation)
    raise ValueError(f"Algorithm {algorithm_name} is not supported!")
