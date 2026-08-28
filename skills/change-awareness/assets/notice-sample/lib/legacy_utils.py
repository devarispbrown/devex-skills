"""Legacy utilities kept for the 2.x compatibility window."""

import warnings


def legacy_transform(data):
    """@deprecated use transform() from core.api.

    Kept functional until 3.0. See the migration notice.
    """
    warnings.warn(
        "legacy_transform is deprecated; use transform() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return data.upper()


def legacy_normalize(value):
    """@deprecated use core.api.normalize()."""
    return value.strip().lower()


# TODO: remove this module in 3.0, after the deprecation window closes
