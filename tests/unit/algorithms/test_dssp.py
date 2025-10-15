import pytest

from struct_draw.algorithms import DSSP


@pytest.fixture(scope="session")
def make_line():
    def _make_line(res_idx, ins=" ", chain="A", aa="G", ss_code="H", make_space_for_dash=False):
        buf = [" "] * 80
        s = f"{res_idx:5d}"
        buf[5:10] = list(s)
        buf[10] = ins
        buf[11] = chain
        buf[13] = aa
        if make_space_for_dash:
            pass
        else:
            buf[16] = ss_code 
        return "".join(buf)
    
    return _make_line


class TestDSSP:
    class TestProcess():
        @pytest.mark.parametrize(
             "lines, header, expected_len",
             [
                 pytest.param(
                     [(1, " ", "A", "A", "H"),
                     (2, " ", "A", "V", "E"),
                     (3, " ", "B", "G", "H", True)],
                     "XXX RESIDUE AA STRUCTURE XXX\n",
                     3,
                      id='good_data+good_header',
                 ),
                 pytest.param(
                     [(1, " ", "A", "A", "H"),
                     (2, " ", "A", "V", "E"),
                     (3, " ", "B", "G", "H", True)],
                     "garbage header\n",
                     0,
                     id='good_data+bad_header',
                 ),
                 pytest.param(
                     [],
                     "XXX RESIDUE AA STRUCTURE XXX\n",
                     0,
                     id='bad_data+bad_header',
                 )
             ]
            
        )
        def test_process_data_basic(self, make_algorithm, make_line, lines, header, expected_len):
            dssp = make_algorithm(DSSP, "dssp", None)
            body = "\n".join(make_line(*args) for args in lines)
            algorithm_out = header + body + "\n"
            arr = dssp.process_data(algorithm_out)
            assert len(arr) == expected_len
            assert arr.dtype.names == ("residue_index", "insertion_code", "chain_id", "AA", "SS", "SS_code")
            if expected_len:
                assert arr["residue_index"][0] == lines[0][0]
                assert arr["chain_id"][0] == lines[0][2]
                assert arr["AA"][0] == lines[0][3]
                codes = arr["SS_code"].tolist()
                if any(t[-1] is True for t in lines):
                    assert "-" in codes
                    idx = codes.index("-")
                    assert arr["SS"][idx] == "Other"
                    
        def test_process_custom_dict(self, make_algorithm, make_line, ss_custom):
            dssp = make_algorithm(DSSP, "dssp", ss_custom)
            header = "XXX RESIDUE AA STRUCTURE XXX\n"
            line = make_line(1, " ", "A", "A", "H")  # SS_code=H
            # by default H should be translated as 'Helix', but with custom it has to be 'Other'
            
            arr = dssp.process_data(header + line + "\n")
            assert len(arr) == 1
            assert arr["SS_code"][0] == "H"
            assert arr["SS"][0] == "Other"
            
        def test_process_data_unknown_code_falls_back_to_other(self, make_algorithm, make_line):
            dssp = make_algorithm(DSSP, "dssp", None)  # default table
            header = "XXX RESIDUE AA STRUCTURE XXX\n"
            line = make_line(2, " ", "A", "G", "X")  # There is no 'X' in deault table
            arr = dssp.process_data(header + line + "\n")
            assert arr["SS_code"][0] == "X"
            assert arr["SS"][0] == "Other"
            
        def test_custom_translation_not_mutated(self, make_algorithm, default_table_dssp):
            """A function that should check whether the table is mutated during the function's execution."""
            mapping = default_table_dssp # default table
            dssp = make_algorithm(DSSP, "dssp", mapping)
            _ = dssp.SS_TRANSLATION['H'] 
            assert mapping['H'] == 'Helix'