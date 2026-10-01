from scripts.backtest_v4 import strikes_for_entry

def test_v4_strikes():
    assert strikes_for_entry(24486.3)=={
        'ce16':25300,'ce17':25350,'pe16':23700,'pe17':23650
    }

def test_four_trading_day_offset():
    dates=['2025-08-20','2025-08-21','2025-08-22','2025-08-25','2025-08-26']
    prev=[d for d in dates if d<'2025-08-26']
    assert prev[-4]=='2025-08-20'
