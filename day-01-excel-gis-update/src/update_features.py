"""Day 01 — Excel to GIS update automation.

This module is intentionally incomplete during the tutorial.
We will build validation first, then GIS update logic.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
) -> bool:
    """Validate that all required columns exist in the input DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Incoming update table.
    required_columns : Iterable[str]
        Column names that must exist before processing can continue.

    Returns
    -------
    bool
        True when the schema is valid.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    # TODO: implement during the tutorial.
    raise NotImplementedError("Implement validate_required_columns()")
