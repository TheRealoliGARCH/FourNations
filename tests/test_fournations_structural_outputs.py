from empirical.run_fournations_structural_outputs import run


def test_runner_generates_three_structural_outputs(tmp_path):
    repo = tmp_path / "repo"
    (repo / "data/raw").mkdir(parents=True)
    (repo / "results").mkdir()
    (repo / "data/raw/nuclear_onsets_seed.csv").write_text(
        "entity,onset_year\nUnited States,1945\nIsrael,1967\nIndia,1974\nPakistan,1998\n"
    )
    (repo / "data/raw/nuclear_onset_scenarios.csv").write_text(
        "scenario,entity,onset_year\nbaseline,Israel,1967\nbaseline,India,1974\nbaseline,Pakistan,1998\n"
        "india_overt_1998,Israel,1967\nindia_overt_1998,India,1998\nindia_overt_1998,Pakistan,1998\n"
    )
    (repo / "data/raw/sovereign_rating_events.csv").write_text(
        "entity,agency,event_date,rating,action,evidence_id\n"
        "Australia,S&P,1957-01-01,AAA,snapshot,TEST-EVIDENCE\n"
    )
    panel, diagnostic, changes = run(repo, start_year=1973, end_year=1999)
    assert not panel.empty
    assert not diagnostic.empty
    assert (repo / "results/genuine_panel_documented_scenarios.csv").exists()
    assert (repo / "results/fournations_cardinality_invariance.csv").exists()
    assert (repo / "results/fournations_classification_changes.csv").exists()
