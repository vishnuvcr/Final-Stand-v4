from scripts.backtest import atm, strike, otm8

def test_atm():
    assert atm(23205.2)==23200
    assert atm(23225.0)==23250

def test_initial_put_mapping():
    assert [strike(23205.2,'PE',n) for n in (6,7,8)] == [22900,22850,22800]

def test_initial_call_mapping():
    assert [strike(23205.2,'CE',n) for n in (6,7,8)] == [23500,23550,23600]

def test_dynamic_put_otm8():
    assert otm8(22740,'PE')==22350

def test_dynamic_call_otm8():
    assert otm8(23660,'CE')==24050
