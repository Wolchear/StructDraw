from typing import Dict, Optional

from .algorithms.dssp import DSSP
from .algorithms.stride import Stride

ALGORITHMS = { "dssp": DSSP,
               "mkdssp": DSSP,
               "stride": Stride }
               
def get_algorithm(algorithm_name: str,
                  ss_translation: Optional[Dict[str,str]] = None):
    """
    Factory for secondary‐structure prediction algorithms.

    Parameters
    ----------
    algorithm_name : str
        Case‐insensitive key of the algorithm to instantiate
        ('dssp', 'mkdssp', 'stride').
    ss_translation : dict of {str: str}, optional
        Mapping from SS codes to human‐readable labels. If None,
        algorithms may use their own default mapping.

    Returns
    -------
    BaseAlgorithm
        An instance of the requested algorithm class, initialized
        with (algorithm_name, ss_translation).

    Raises
    ------
    ValueError
        If `algorithm_name` is not one of the supported keys.
    """
    algorithm_key = algorithm_name.lower()
    if algorithm_key in ALGORITHMS:
        return ALGORITHMS[algorithm_key](algorithm_name, ss_translation)
    raise ValueError(f"Algorithm {algorithm_name} is not supported!")
