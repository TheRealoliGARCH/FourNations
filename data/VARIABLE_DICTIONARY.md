# FourNations Variable Dictionary

## Version

V1.1 — Genuine Nation operationalization.

## Historical system panel

Each row represents one system-year.

| Variable | Definition | Type |
|---|---|---|
| system_id | Stable identifier for a historical international system | string |
| year | Calendar year | integer |
| N_powers | Number of entities classified as Genuine Nations under the preregistered historical rule | integer |
| crisis_5y | 1 if a preregistered systemic crisis begins within the next five years; otherwise 0 | binary |
| Q | Phase coherence under the selected operationalization | continuous [0,1] |
| phi_1 | Largest geopolitical angular gap under the selected power-angle mapping | continuous |
| source_set | Identifier for underlying source records | string |

## Genuine Nation membership

The baseline empirical unit is the Genuine Nation, not the conventionally recognized sovereign state.

For a given year t:

G_t = N_t union C_t,

where:

- N_t: entities possessing an operational nuclear arsenal;
- C_t: entities satisfying the preregistered AAA sovereign-credit criterion.

Baseline count:

N_powers(t) = |G_t|.

The membership indicator for entity i is:

g_i(t) = 1{i in N_t or i in C_t}.

Thus every genuine nation is counted and no additional conventional-state relevance filter is applied.

## Rating specifications

Because AAA membership depends on rating-agency convention, the following are separate specifications:

- Conservative: designated primary-agency AAA criterion.
- Extended: AAA qualification under any preregistered major agency.

Results must report the classification convention and never pool them silently.

## Historical reconstruction

For years before modern sovereign credit ratings, C_t must not be backfilled by analogy without an explicitly documented historical proxy. Nuclear membership and fiscal/financial capacity series therefore require separate provenance and may have different historical coverage.

The baseline historical panel records coverage explicitly rather than pretending that the modern 2026 classification can be mechanically projected to 1648.

## Monetary panel

| Variable | Definition |
|---|---|
| asset_return | Nominal or real return under documented convention |
| risk_free_rate | Matching risk-free benchmark |
| expected_inflation | Ex ante inflation expectation |
| pi_irp | asset_return - risk_free_rate - expected_inflation |
| consumption_growth | Consumption growth used in CCAPM tests |
| consumption_beta | Estimated covariance-based beta |
| consumption_variance | Estimated variance of consumption growth |

## Labor and luxury panel

The paper specifies theoretical variables f and L. Historical proxies are not assumed equivalent to those theoretical objects.

Every proxy must therefore record:

1. exact observable series;
2. transformation;
3. temporal coverage;
4. geographic coverage;
5. conceptual limitations.

## Missingness

Missing values are never silently imputed in the baseline dataset. Any imputation creates a separate, versioned derived dataset.
