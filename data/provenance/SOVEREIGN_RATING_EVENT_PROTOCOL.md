# Sovereign Rating Event Protocol

## Principle

Historical AAA membership is reconstructed from dated rating events, not inferred from present-day ratings.

Each event records:

- entity
- agency
- event_date
- rating
- action
- evidence_id
- source publication date
- source reference
- notes

## Annualization rule

For a calendar year y, AAA membership equals 1 if the registered rating state is AAA at the selected annual observation date.

Baseline observation date: 31 December.

If the rating state is unavailable at that date, membership is missing rather than assumed to be 0.

## Interval generation

Consecutive rating events are converted into intervals by a deterministic transformation. Generated intervals are derived artifacts and must retain the event-source version from which they were built.

## Agency specifications

Primary specification: S&P only.

Extended specification: any preregistered major agency represented in the event table. Agencies are reported separately before any union is computed.
