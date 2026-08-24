# Genuine Nation Classification Protocol

## Governing rule

For every year t:

G_t = N_t union C_t.

An entity is counted if and only if it satisfies at least one preregistered criterion:

1. operational nuclear arsenal; or
2. AAA sovereign credit status under the selected rating specification.

All members of G_t are relevant powers by definition.

## Membership fields

The source dataset must contain:

- entity
- year
- nuclear_member
- aaa_primary_member
- aaa_any_agency_member
- genuine_primary
- genuine_extended
- evidence_id
- notes

where:

genuine_primary = nuclear_member OR aaa_primary_member

genuine_extended = nuclear_member OR aaa_any_agency_member

## Historical rule

Membership is time-varying. A 2026 classification cannot be projected backward without evidence.

For periods lacking a defensible credit-rating measure, the dataset records the coverage limitation and uses a separately versioned historical-capacity specification rather than silently substituting modern AAA status.

## Robustness

The four-nation hypothesis must be tested under both the primary and extended rating conventions where data permit.

No entity is excluded because it is geographically small, diplomatically peripheral, economically small, or politically inconvenient once it satisfies the Genuine Nation criterion.
