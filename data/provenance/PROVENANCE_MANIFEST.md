# Data Acquisition and Provenance Manifest

## Principle

Every empirical observation must be traceable to:

source -> retrieval date -> raw artifact -> checksum where available -> transformation -> derived variable.

## Source hierarchy

1. Primary official or archival source.
2. Authoritative international database.
3. Peer-reviewed or curated historical dataset.
4. Secondary reconstruction, explicitly labelled.

## Required metadata

For every source record:

- source_id
- provider
- title or series name
- canonical access location
- retrieval date
- coverage
- license or access terms where available
- raw filename
- checksum where practical
- transformation script
- output dataset version

## Reproducibility rule

Raw data are not overwritten. Transformations are deterministic and version controlled.

## Historical power-count protocol

N_powers cannot be inferred retrospectively from the theory's desired result. A power classification rule must be fixed before crisis-outcome estimation.

The baseline and robustness classifications will be stored separately.

## Crisis protocol

A crisis event must have:

- event identifier;
- start year;
- end year where applicable;
- geographic/system scope;
- inclusion rationale;
- source citation.

The five-year outcome is generated mechanically from the preregistered event table.
