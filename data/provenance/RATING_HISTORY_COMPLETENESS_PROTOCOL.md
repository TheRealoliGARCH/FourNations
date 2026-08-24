# Rating History Completeness Protocol

## Three-state interpretation

The annual rating panel distinguishes:

- 1: AAA observed at the annual observation date;
- 0: observed rating state is non-AAA;
- missing: no registered rating history supports classification.

Missing values are not converted to zero.

## Extended specification

The extended AAA indicator is:

AAA_any(i,t) = 1

if at least one observed preregistered agency classifies entity i as AAA.

It equals 0 only when one or more agency observations exist and none are AAA.

It remains missing when no preregistered agency has observed coverage for the entity-year.

## Reporting

Every empirical result using the Shield component must report:

1. agencies included;
2. number of observed entities by year;
3. AAA entities by agency and year;
4. missing coverage;
5. the annual observation-date convention.

A change in agency coverage constitutes a dataset-version change.
