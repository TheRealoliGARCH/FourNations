# FourNations Structural Output Protocol

The structural output runner executes the documented nuclear-onset scenarios against the fixed annual S&P Shield reconstruction.

For each scenario `s` and year `t`, it constructs the entity-year Genuine panel and computes:

`K(s,t) = number of genuine_member == 1`.

The FourNations target is evaluated as `K(s,t) == 4`. Scenario invariance is assessed against the baseline classification for the same year.

The generated CSV files are execution artifacts. They do not replace source data, alter the baseline chronology, or constitute an equilibrium proof. Any substantive interpretation must distinguish panel cardinality from the paper's full equilibrium conditions.
