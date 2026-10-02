from scripts.backtest_v5_credit_selected import atm, strikes_for_entry, select_side, target_threshold, stop_threshold

def test_atm_rounds_nearest_and_tie_up():
    assert atm(23205.2) == 23200
    assert atm(23225.0) == 23250

def test_otm_strikes():
    assert strikes_for_entry(23205.2) == {'ce6':23500,'ce7':23550,'ce8':23600,'pe6':22900,'pe7':22850,'pe8':22800}

def test_credit_selection():
    puts=(100.0,60.0,30.0)  # pe6, pe7, pe8 -> credit -10
    calls=(50.0,35.0,30.0)  # ce6, ce7, ce8 -> credit +15
    side, credit, tie = select_side(puts[0],puts[1],puts[2],calls[0],calls[1],calls[2])
    assert side=='CALL' and round(credit,6)==15.0 and not tie

def test_target_and_stop_are_credit_multiples():
    assert target_threshold(900.0,0.90)==810.0
    assert stop_threshold(900.0,1.00)==-900.0