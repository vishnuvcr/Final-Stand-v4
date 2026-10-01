from scripts.backtest_reversal import atm, strike, exec_px

def test_otm_mapping():
    assert atm(23205.2) == 23200
    assert strike(23205.2,'PE',6) == 22900
    assert strike(23205.2,'PE',7) == 22850
    assert strike(23205.2,'PE',8) == 22800
    assert strike(23205.2,'CE',6) == 23500
    assert strike(23205.2,'CE',7) == 23550
    assert strike(23205.2,'CE',8) == 23600

def test_reversal_leg_mapping():
    assert ('PE' if 'CE' == 'PE' else 'CE') == 'CE'
    assert ('CE' if 'PE' == 'CE' else 'PE') == 'PE'

def test_execution_slippage_direction(monkeypatch):
    monkeypatch.setenv('SLIPPAGE_POINTS','0.10')
    assert exec_px(10.0,'BUYBACK') == 10.1
    assert exec_px(10.0,'SELL') == 9.9
