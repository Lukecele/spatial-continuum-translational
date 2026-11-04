import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text())


def test_frozen_signature_contract():
    definition = load_json("data/resistance_signatures_v1.json")
    signatures = definition["signatures"]

    assert definition["version"] == "resistance-signatures-v1"
    assert len(signatures) == 6
    for signature in signatures.values():
        assert len(signature["genes"]) >= 3
        assert len(signature["genes"]) == len(set(signature["genes"]))


def test_xenium_panel_validation_is_complete():
    report = load_json("data/derived/resistance_signatures_v1_panel_validation.json")

    assert all(
        item["coverage_fraction"] == 1.0
        for item in report["signatures"].values()
    )


def test_primary_cohort_structural_gate_passes():
    report = load_json("data/derived/primary_cohort_validation.json")

    assert report["all_structural_checks_pass"] is True
    assert report["checks"]["five_complete_xenium_pairs"] is True
    assert report["checks"]["snrna_has_tn_mrd_pd"] is True


def test_resistance_statistics_keep_patient_level_units():
    report = load_json("data/derived/resistance_statistical_comparison.json")

    assert report["xenium_paired"]["pairs"] == 5
    assert report["snrna_state_comparison"]["states"] == {
        "MRD": 14,
        "PD": 31,
        "TN": 28,
    }
