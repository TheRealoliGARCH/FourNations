# Five-Year Systemic Crisis Label Protocol

## Outcome

For a system-year t:

crisis_5y(t) = 1

if a preregistered systemic crisis begins in:

(t, t + 5].

Otherwise:

crisis_5y(t) = 0.

The current year is excluded to preserve the forward-looking interpretation.

## Event table

Each event must record:

- event_id;
- system_id;
- start_year;
- end_year where applicable;
- inclusion rationale;
- evidence_id.

## No retrospective tuning

Crisis inclusion cannot be changed after inspecting the four-nation test result without creating a new dataset version and rerunning the analysis.

## Coverage

The repository currently contains the event schema and deterministic label generator, not yet a completed 1648–2026 crisis chronology.
