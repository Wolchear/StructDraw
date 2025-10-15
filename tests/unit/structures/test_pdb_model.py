import pytest

import numpy as np

from struct_draw.algorithms.base_algorithm import BaseAlgorithm
from struct_draw.structures import PDB, PDBx, BaseModel

class TestShared:
    class DummyModel(BaseModel):
        def parse_b_factor(self):
            pass
        
    class FakeAlgorithm(BaseAlgorithm):
        def __init__(self):
            self._algorithm_sub_name = 'fake_algo'

        def run(self, pdb_path: str) -> str:
            return "fake_out"

        def process_data(self, algorithm_out: str) -> np.ndarray:
            recs = [
                (r["chain_id"], r["residue_index"], r["insertion_code"],
                 r["AA"], r["SS"], r["SS_code"])
                for r in algorithm_out
            ]
            dtype = [
                ("chain_id", "U2"),
                ("residue_index", "i4"),
                ("insertion_code", "U2"),
                ("AA", "U2"),
                ("SS", "U16"),
                ("SS_code", "U2"),
            ]
            return np.array(recs, dtype=dtype)
    @pytest.mark.parametrize(
        "include, ref_key_set",
        [
            pytest.param(
                None,
                {"A", "B"},
                id='include_all',
            ),
            pytest.param(
                ["A"],
                {"A"},
                id='include_only_A',
            ),
            pytest.param(
                ["B", "C"],
                {"B"},
                id='include_only_B_with_non_existing_C',
            )
        ]
    )
    def test_process_algorithm_data(self, fake_algorithm_rows: list[dict[str, str | int]], include, ref_key_set):
        fake_algorithm = self.FakeAlgorithm()
        dummy_model = self.DummyModel(algorithm=fake_algorithm, algorithm_out=fake_algorithm_rows,
                                      pdb_file='fake_file', include_only=include)
        
        chains = dummy_model.get_chain_list()
        
        assert all([chain.algorithm == 'fake_algo' for chain in chains.values()])
        assert all([chain.model_id == 'fake_file' for chain in chains.values()])
        assert set(chains.keys()) == ref_key_set            