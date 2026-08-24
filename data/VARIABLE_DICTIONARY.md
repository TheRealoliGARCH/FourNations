# FourNations Variable Dictionary

## Version

V1.0 — preregistered before empirical estimation.

## Historical system panel

Each row represents one system-year.

| Variable | Definition | Type |
|---|---|---|
| system_id | Stable identifier for a historical international system | string |
| year | Calendar year | integer |
| N_powers | Number of powers satisfying the preregistered power rule | integer |
| crisis_5y | 1 if a preregistered systemic crisis begins within the next five years; otherwise 0 | binary |
| Q | Phase coherence under the selected operationalization | continuous [0,1] |
| phi_1 | Largest geopolitical angular gap under the selected power-angle mapping | continuous |
| source_set | Identifier for underlying source records | string |

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
