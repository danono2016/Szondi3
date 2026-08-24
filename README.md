# Szondi3

Szondi3 is the clean authoritative continuation of the Szondi project.

This repository is not a copy of Szondi2. It is a controlled restart built around one non-negotiable architectural distinction:

> **First preserve Szondi's doctrine faithfully. Only afterwards formalize what the software may do with that doctrine.**

## Authority

- `Szondi3` is the active authoritative development repository.
- `Szondi2` is the predecessor, audit trail, and source of components that may be migrated only after explicit review.
- Nothing from `Szondi2` is authoritative in `Szondi3` merely because it existed or passed tests there.

## Initial architecture

`Primary Sources -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

The Primary Doctrine Registry and the Executable Interpretation Layer are deliberately separate. A mistake in executable formalization must never require rewriting or losing the faithfully preserved Szondian doctrine.

## Migration rule

Migration from Szondi2 is whitelist-only. Every imported component must be classified and documented as one of:

- `TRANSFER_AS_IS`
- `TRANSFER_AFTER_REVALIDATION`
- `REDESIGN_FROM_ZERO`
- `ARCHIVE_ONLY`

See `docs/PROJECT_CONSTITUTION.md`, `docs/DOCTRINAL_FIDELITY_POLICY.md`, and `docs/MIGRATION_MANIFEST.md` before adding implementation code.
