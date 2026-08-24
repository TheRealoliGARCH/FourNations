import pandas as pd

from empirical.genuine_nations import classify_genuine_nations


def test_all_qualifying_entities_are_counted():
    df = pd.DataFrame(
        {
            "entity": ["A", "B", "C", "D"],
            "nuclear_member": [1, 0, 0, 1],
            "aaa_primary_member": [0, 1, 0, 0],
            "aaa_any_agency_member": [0, 1, 1, 0],
        }
    )
    out = classify_genuine_nations(df)
    assert out["genuine_primary"].tolist() == [1, 1, 0, 1]
    assert out["genuine_extended"].tolist() == [1, 1, 1, 1]


def test_count_has_no_secondary_relevance_filter():
    df = pd.DataFrame(
        {
            "entity": ["A", "B"],
            "nuclear_member": [1, 0],
            "aaa_primary_member": [0, 1],
            "aaa_any_agency_member": [0, 1],
        }
    )
    out = classify_genuine_nations(df)
    assert int(out["genuine_primary"].sum()) == 2
