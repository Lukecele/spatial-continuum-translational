"""Compatibility boundary for the unchanged spatial-continuum package."""


def legacy_cri(pattern: str, tp53: str = "wt", rb1: str = "wt", stroma: str = "moderate"):
    """Call the original package's CRI calculator without modifying it."""
    from spatial_continuum.cri_calc import calculate_cri

    return calculate_cri(pattern, tp53=tp53, rb1=rb1, stroma=stroma)
