import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

r=pd.read_csv("results/trades.csv")
for side,g in r.sort_values("expiry").groupby("side"):
    eq=g.net_pnl.cumsum()
    plt.figure(figsize=(10,5))
    plt.plot(pd.to_datetime(g.expiry),eq,marker="o")
    plt.xlabel("Expiry")
    plt.ylabel("Cumulative net P&L (INR)")
    plt.title(f"{side} cumulative net P&L")
    plt.tight_layout()
    plt.savefig(f"results/equity_{side}.png",dpi=160)
    plt.close()

plt.figure(figsize=(8,5))
for side,g in r.groupby("side"):
    plt.hist(g.net_pnl,bins=15,alpha=.5,label=side)
plt.xlabel("Net P&L per trade (INR)")
plt.ylabel("Frequency")
plt.title("Call vs Put trade P&L distribution")
plt.legend()
plt.tight_layout()
plt.savefig("results/pnl_distribution.png",dpi=160)
plt.close()
