import pytest

from spatial_continuum_translational.gist import (
    GistFeatures,
    score_gist_research_profile,
)


def test_score_is_bounded_and_transparent():
    score = score_gist_research_profile(
        GistFeatures(5, "gastric", False, "kit_exon11", 8)
    )

    assert 0 <= score.score <= 1
    assert score.mitotic_component == pytest.approx(0.25)
    assert score.rupture_component == 0


def test_rupture_and_high_mitotic_rate_increase_score():
    baseline = score_gist_research_profile(
        GistFeatures(2, "gastric", False, "kit_exon11", 5)
    )
    higher_risk = score_gist_research_profile(
        GistFeatures(20, "jejunal_ileal", True, "kit_exon9", 20)
    )

    assert higher_risk.score > baseline.score


def test_invalid_features_are_rejected():
    with pytest.raises(ValueError):
        score_gist_research_profile(
            GistFeatures(-1, "gastric", False, "kit_exon11", 5)
        )
    with pytest.raises(ValueError):
        score_gist_research_profile(
            GistFeatures(1, "gastric", False, "kit_exon11", 0)
        )
