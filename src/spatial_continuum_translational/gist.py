"""Exploratory GIST extension built on documented recurrence features.

This module is a research phenotype score, not a validated clinical predictor.
The inputs are intentionally explicit so future calibration can be audited.
"""

from dataclasses import dataclass
from typing import Literal


Site = Literal["gastric", "duodenal", "jejunal_ileal", "rectal", "other"]
Mutation = Literal["kit_exon11", "kit_exon9", "pdgfra", "wild_type", "other"]


@dataclass(frozen=True)
class GistFeatures:
    """Inputs used by the exploratory GIST recurrence profile."""

    mitoses_per_50_hpf: float
    site: Site
    tumor_rupture: bool
    mutation: Mutation
    tumor_size_cm: float


@dataclass(frozen=True)
class GistResearchScore:
    """Transparent, unitless research score and its component values."""

    score: float
    mitotic_component: float
    site_component: float
    rupture_component: float
    mutation_component: float
    size_component: float


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_gist_research_profile(features: GistFeatures) -> GistResearchScore:
    """Calculate an uncalibrated recurrence-risk research profile.

    The score is a transparent engineering scaffold, not a probability and not
    a treatment recommendation. Components are normalized to [0, 1] and are
    kept separate so they can be replaced by a fitted model after validation.
    """
    if features.mitoses_per_50_hpf < 0:
        raise ValueError("mitoses_per_50_hpf must be non-negative")
    if features.tumor_size_cm <= 0:
        raise ValueError("tumor_size_cm must be positive")

    mitotic = _bounded(features.mitoses_per_50_hpf / 20.0)
    site = {
        "gastric": 0.0,
        "duodenal": 0.65,
        "jejunal_ileal": 0.8,
        "rectal": 0.8,
        "other": 0.5,
    }[features.site]
    rupture = 1.0 if features.tumor_rupture else 0.0
    mutation = {
        "kit_exon11": 0.55,
        "kit_exon9": 0.75,
        "pdgfra": 0.25,
        "wild_type": 0.4,
        "other": 0.5,
    }[features.mutation]
    size = _bounded(features.tumor_size_cm / 15.0)

    score = (
        0.35 * mitotic
        + 0.15 * site
        + 0.25 * rupture
        + 0.10 * mutation
        + 0.15 * size
    )
    return GistResearchScore(
        score=round(score, 6),
        mitotic_component=round(mitotic, 6),
        site_component=round(site, 6),
        rupture_component=round(rupture, 6),
        mutation_component=round(mutation, 6),
        size_component=round(size, 6),
    )
