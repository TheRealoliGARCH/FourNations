# Provisional Genuine Panel Protocol

This output is a provisional empirical construction:

G_t^seed = N_t^seed union C_t^(S&P)

The nuclear component is generated mechanically from `data/raw/nuclear_onsets_seed.csv`. Every nuclear observation therefore carries `nuclear_source_status = seed`.

The Shield component retains its existing three-state semantics:

- `1`: observed year-end S&P AAA membership;
- `0`: observed year-end non-AAA status;
- `NA`: no observed rating history on or before the relevant year-end.

The union is evaluated without imputing missing Shield history:

- if nuclear membership is `1`, `genuine_member = 1`;
- otherwise, an observed Shield value determines `genuine_member`;
- otherwise, `genuine_member = NA`.

This is not a fully validated historical nuclear panel. Israel, India, and Pakistan retain documented alternative-onset sensitivity issues in the seed source. Any substantive result using the provisional panel must therefore be accompanied by onset-year sensitivity analysis before being treated as a FourNations equilibrium finding.
