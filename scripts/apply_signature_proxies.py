#!/usr/bin/env python3
"""Map frozen signatures to available metadata proxies without inventing scores."""

import json
from pathlib import Path

INPUT = Path("data/derived/resistance_metadata_analysis.json")
OUTPUT = Path("data/derived/resistance_signature_proxy_application.json")


def main() -> None:
    data = json.loads(INPUT.read_text())
    report = {
        "signature_version": "resistance-signatures-v1",
        "xenium": {
            "tumor_epithelial_identity": {
                "status": "proxy_applied",
                "proxy": "tumor_fraction",
                "values": {row["sample_id"]: row["tumor_fraction"] for row in data["xenium_by_sample"]},
            },
            "basal_plasticity": {
                "status": "proxy_applied",
                "proxy": "mean_basal_squamous_score_tumor",
                "values": {row["sample_id"]: row["mean_basal_squamous_score_tumor"] for row in data["xenium_by_sample"]},
            },
            "neuroendocrine_plasticity": {
                "status": "proxy_applied",
                "proxy": "mean_neuroendocrine_score_tumor",
                "values": {row["sample_id"]: row["mean_neuroendocrine_score_tumor"] for row in data["xenium_by_sample"]},
            },
            "egfr_mapk_resistance": {
                "status": "proxy_applied",
                "proxy": "c797s_cell_fraction",
                "values": {row["sample_id"]: row["c797s_cell_fraction"] for row in data["xenium_by_sample"]},
            },
            "hypoxia_stress": {"status": "not_calculated", "reason": "No gene-level counts in the downloaded metadata."},
            "vascular_access": {"status": "not_calculated", "reason": "No gene-level counts in the downloaded metadata."},
        },
        "snrna": {
            "tumor_epithelial_identity": {"status": "proxy_applied", "proxy": "tumor_fraction"},
            "basal_plasticity": {"status": "not_calculated", "reason": "Cell annotations are available, but gene-level counts are not downloaded."},
            "neuroendocrine_plasticity": {"status": "not_calculated", "reason": "Cell annotations are available, but gene-level counts are not downloaded."},
            "egfr_mapk_resistance": {"status": "not_calculated", "reason": "Cell annotations are available, but gene-level counts are not downloaded."},
            "hypoxia_stress": {"status": "not_calculated", "reason": "Gene-level counts are not downloaded."},
            "vascular_access": {"status": "not_calculated", "reason": "Gene-level counts are not downloaded."},
        },
        "interpretation": "Proxy values are exploratory metadata measures and are not equivalent to frozen gene-expression signature scores.",
    }
    report["snrna"]["tumor_epithelial_identity"]["values"] = {
        row["sample_id"]: row["tumor_fraction"] for row in data["snrna_by_sample"]
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"output": str(OUTPUT), "signature_version": report["signature_version"]}, indent=2))


if __name__ == "__main__":
    main()
