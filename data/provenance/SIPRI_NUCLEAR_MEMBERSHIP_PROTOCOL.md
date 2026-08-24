# SIPRI Nuclear Membership Reconstruction Protocol

## Baseline object

The Sword component is a time-varying binary membership panel:

nuclear_member_i(t) in {0,1}.

A value of 1 means that the entity is classified as nuclear-armed under the registered SIPRI reconstruction for that year.

## Evidence layers

1. SIPRI Yearbook editions and World Nuclear Forces pages.
2. SIPRI methodology and source-assessment documentation.
3. Versioned historical onset table used only to generate years for which the reconstruction rule is explicitly supported.

## No unsupported backfill

Rows are not generated merely because a state is nuclear-armed today. Every onset date must have an evidence identifier and a stated interpretation.

## Baseline versus uncertainty

Where public-source evidence supports a range or ambiguity, the baseline panel records the selected convention and the uncertainty is retained in notes. Alternative onset conventions must be generated as separate robustness panels.

## Current seed

The initial reconstruction begins with the nine SIPRI nuclear-armed states identified in the 2026 SIPRI Yearbook. The historical onset table is a seed requiring source-by-source extension before claiming a complete annual historical panel.
