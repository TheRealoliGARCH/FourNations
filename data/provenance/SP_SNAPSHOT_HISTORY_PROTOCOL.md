# S&P Snapshot History Protocol

The initial S&P history consists of source-supported year-level snapshots, not a complete event history.

For this seed, event_date is the canonical annual observation date (31 December of the source year) used for panel indexing. It is not asserted to be the publication date or the date of a rating action.

The source publication date is retained only when explicitly known. Empty publication-date fields mean the exact publication date was not established during this ingestion pass.

No result generated from these sparse snapshots may be described as a complete continuous S&P rating history. Continuous-state reconstruction requires dated upgrades, downgrades, affirmations, or periodic observations with sufficient temporal density.
