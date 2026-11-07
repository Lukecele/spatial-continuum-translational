import json
from pathlib import Path

from spatial_continuum_translational.cli import main


def test_cli_writes_json(capsys):
    assert (
        main(
            [
                "--mitoses-per-50-hpf",
                "5",
                "--site",
                "gastric",
                "--mutation",
                "kit_exon11",
                "--tumor-size-cm",
                "8",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert payload["score"] == 0.2225
    assert payload["mitotic_component"] == 0.25
    assert payload["model_version"] == "gist-research-profile-v1"
    assert payload["research_only"] is True


def test_cli_writes_tsv(capsys):
    main(
        [
            "--mitoses-per-50-hpf",
            "5",
            "--site",
            "gastric",
            "--mutation",
            "kit_exon11",
            "--tumor-size-cm",
            "8",
            "--format",
            "tsv",
        ]
    )

    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("score\tmitotic_component")
    assert lines[1].startswith("0.2225\t0.25")


def test_cli_reproduces_annotated_tsv_input(tmp_path: Path, capsys):
    input_path = tmp_path / "cohort.tsv"
    input_path.write_text(
        "sample_id\tmitoses_per_50_hpf\tsite\ttumor_rupture\tmutation\ttumor_size_cm\n"
        "case-01\t5\tgastric\tfalse\tkit_exon11\t8\n",
        encoding="utf-8",
    )

    main(["--input", str(input_path), "--format", "tsv"])

    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("score\t")
    assert "case-01" in lines[1]
    assert "0.2225" in lines[1]


def test_cli_rejects_missing_input_fields(tmp_path: Path):
    input_path = tmp_path / "invalid.json"
    input_path.write_text(
        json.dumps({"site": "gastric", "mutation": "kit_exon11"}),
        encoding="utf-8",
    )

    try:
        main(["--input", str(input_path)])
    except ValueError as error:
        assert "missing required fields" in str(error)
    else:
        raise AssertionError("invalid input should be rejected")
