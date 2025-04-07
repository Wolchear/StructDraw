from abc import ABC, abstractmethod

import numpy as np

class BaseAlgorithm(ABC):
    def __init__(self, algorithm_sub_name: str):
        self._algorithm_sub_name = algorithm_sub_name
	
    @abstractmethod	
    def run(self, pdb_file: str) -> str:
        pass
     
    @abstractmethod  
    def process_data(self, app_out: str) -> np.ndarray:
        pass
