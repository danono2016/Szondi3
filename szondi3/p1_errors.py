"""Typed exceptions for expected deterministic P1 fail-closed states."""


class P1UnresolvedError(ValueError):
    """A source-defined or explicitly preserved P1 state cannot be resolved.

    The class derives from ``ValueError`` for backward compatibility with existing
    public callers and tests, while allowing orchestration code to distinguish an
    expected fail-closed clinical-calculation boundary from an accidental generic
    ``ValueError`` raised by a programming defect.
    """

