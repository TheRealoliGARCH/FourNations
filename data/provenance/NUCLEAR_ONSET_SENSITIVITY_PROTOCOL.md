# Nuclear Onset Sensitivity Protocol

The repository baseline is `data/raw/nuclear_onsets_seed.csv`. It explicitly identifies Israel, India, and Pakistan as cases where alternative onset conventions may matter.

This sensitivity layer does not invent alternative dates. The scenario input currently records only the baseline values already present in the seed. Additional scenarios may be added only with an explicit onset convention, evidence identifier, and provenance note.

For every admissible scenario `s`, construct:

`N_i,t^(s) = 1{t >= onset_i^(s)}`.

Differences from the baseline are then measured year by year. Downstream Genuine-panel and equilibrium analysis may consume scenario panels only after the alternative onset inputs have documented evidence.
