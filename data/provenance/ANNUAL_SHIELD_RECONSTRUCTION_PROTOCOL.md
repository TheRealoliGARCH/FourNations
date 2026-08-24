# Annual Shield Reconstruction

This branch generates two reproducible empirical outputs:

- `annual_snp_shield_panel.csv`: entity-year S&P Shield states.
- `annual_snp_shield_diagnostics.csv`: annual counts of observed, missing, AAA, and observed non-AAA states.

The state space is strictly:

```
NA = no observed rating history on or before year-end
0  = observed non-AAA rating at year-end
1  = observed AAA rating at year-end
```

The diagnostics do not impute missing observations and do not claim a complete global sovereign universe. They summarize only the bounded 11-entity primary candidate universe.

The nuclear merge is intentionally deferred until the repository's canonical SIPRI-derived nuclear panel path/schema is identified and validated; no synthetic nuclear data are introduced here.
