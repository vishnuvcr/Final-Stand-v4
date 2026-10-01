import pandas as pd

def next_execution_timestamp(times, observed):
    t=pd.Timestamp(observed)
    xs=pd.Series(pd.to_datetime(times)).sort_values()
    y=xs[xs>t]
    return None if y.empty else y.iloc[0]

def recenter_otm8(current_spot, side, strike_step=50):
    atm=int((float(current_spot)/strike_step+0.5)//1*strike_step)
    return atm + 8*strike_step if side=="CE" else atm - 8*strike_step
