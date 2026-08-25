# Scenario Propagation Protocol

For every evidence-supported nuclear-onset scenario `s`, construct an entity-year nuclear panel and merge it with the fixed S&P Shield reconstruction.

The baseline is never overwritten.

## Membership semantics

`genuine_member = 1` when nuclear membership is 1.

If nuclear membership is 0, an observed Shield state is propagated as 0 or 1.

If nuclear membership is 0 and the Shield state is unobserved, `genuine_member` remains `NA`.

## Invariance diagnostic

For each scenario and year, compute the annual Genuine count and compare it with the baseline:

`delta_s,t = count_s,t - count_baseline,t`.

A nonzero delta identifies the exact historical interval affected by the alternative onset convention. This is a sensitivity diagnostic, not by itself a substantive equilibrium test.
