from scripts.strategy_rules import next_execution_timestamp, recenter_otm8


def test_target_executes_next_minute_not_same_bar():
    assert str(next_execution_timestamp(['2026-01-01 10:00','2026-01-01 10:01','2026-01-01 10:02'], '2026-01-01 10:01')) == '2026-01-01 10:02:00'


def test_no_execution_after_last_bar():
    assert next_execution_timestamp(['2026-01-01 10:00'], '2026-01-01 10:00') is None


def test_recenter_put_from_current_spot():
    assert recenter_otm8(22740,'PE') == 22350


def test_recenter_call_from_current_spot():
    assert recenter_otm8(23660,'CE') == 24050


def test_recenter_is_not_fixed_otm12():
    assert recenter_otm8(22740,'PE') != 22600
