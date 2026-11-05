import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "software_strumenti_calcolo"))

from cri_calc import calculate_cri


def test_reference_cases_are_deterministic():
    assert calculate_cri("lepidic", "wt", "wt", "low")["CRI"] == 0.000
    assert calculate_cri("solid", "mut", "mut", "dense")["CRI"] == 1.000
    assert calculate_cri("acinar", "mut", "wt", "moderate")["CRI"] == 0.453


def test_unknown_inputs_are_rejected():
    try:
        calculate_cri("unclassified", "wt", "wt", "low")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown histology should not receive a silent default")
