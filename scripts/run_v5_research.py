import os, subprocess, sys
from pathlib import Path
import pandas as pd

ROOT=Path('.')
env0=os.environ.copy()
stop_grid=['0','0.50','0.75','1.00','1.25','1.50']
target_grid=['0.85','0.90','0.95','1.00']

def run_case(target,stop,out_name,tag_key,tag_value):
    env=env0.copy(); env['TARGET_FRAC']=target; env['STOP_MULT']=stop
    subprocess.run([sys.executable,'scripts/backtest_v5_credit_selected.py'],env=env,check=True)
    df=pd.read_csv('results/strategy_v5_trades.csv')
    df[tag_key]=float(tag_value)
    path=ROOT/'results'/out_name
    df.to_csv(path,index=False,mode='a' if path.exists() else 'w',header=not path.exists())

Path('results').mkdir(exist_ok=True)
for p in ['results/strategy_v5_trades_grid.csv','results/strategy_v5_target_grid.csv']:
    Path(p).unlink(missing_ok=True)

for stop in stop_grid:
    run_case('0.90',stop,'strategy_v5_trades_grid.csv','stop_multiple',stop)

for target in target_grid:
    run_case(target,'0','strategy_v5_target_grid.csv','target_fraction',target)

subprocess.run([sys.executable,'scripts/select_v5_stop_and_analyze.py'],env=env0,check=True)
print('Phase 9 research wrapper complete')