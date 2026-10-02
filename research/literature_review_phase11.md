# Phase 11 Literature Review — Option-Premium Information and Return Predictability

## Purpose

The proposed NIFTY predictor is a bespoke linear combination of OTM call and put premiums. The literature does not, from the initial search, establish this exact formula as a known predictor. The relevant literature instead motivates testing whether information embedded in option prices, volatility spreads, skewness, and option-implied distributions can contain information about subsequent underlying returns.

## Evidence base identified so far

### 1. Option-market information can predict subsequent stock returns

Lin and Lu (2015) report that option-implied volatility contains predictive information about future stock returns and find stronger predictive power around analyst-related events, consistent with informed trading as one mechanism. This supports testing option-derived predictors without assuming that every option statistic is purely a risk premium. [Journal of Banking & Finance](https://doi.org/10.1016/j.jbankfin.2014.11.008)

Hu (2014) studies option-induced stock order imbalance and reports that the imbalance induced by option transactions significantly predicts future stock returns, consistent with information transmission from options to the stock market. [Journal of Financial Economics](https://doi.org/10.1016/j.jfineco.2013.12.004)

### 2. Option-implied skewness and higher moments are linked to later returns

Conrad, Dittmar and Ghysels (2013) use option prices to estimate ex-ante risk-neutral higher moments and report relations between volatility, skewness, kurtosis and subsequent returns. [Journal of Finance](https://doi.org/10.1111/j.1540-6261.2012.01795.x)

Stilger, Kostakis and Poon (2016/2017 publication versions) document a relationship between risk-neutral skewness and subsequent realized stock returns, and report that strongly negative skewness can be associated with subsequent underperformance. [Management Science](https://doi.org/10.1287/mnsc.2015.2379)

Kim and Park (2018) find that the relation between option-implied skewness and subsequent returns varies with market state. This directly motivates regime-conditioned robustness testing in the NIFTY study. [Journal of Futures Markets](https://doi.org/10.1002/fut.21921)

### 3. Call-put option information has predictive content in some settings

The literature includes evidence on call-put implied-volatility spreads and option-implied asymmetry as predictors of later returns. Cao, Simin and Xiao report predictive content in call-put implied-volatility spreads for the U.S. equity premium at horizons up to six months. [Journal of Financial Markets](https://doi.org/10.1016/j.finmar.2019.100531)

Huang and Li (2019) study implied variance asymmetry extracted from OTM options and report a positive relation with subsequent stock returns in their cross-sectional setting. [Journal of Banking & Finance](https://doi.org/10.1016/j.jbankfin.2019.02.001)

### 4. Predictability can have multiple economic explanations

A 2025 Journal of Financial Economics study revisits option-implied volatility-spread/skew predictability and argues that some of the apparent relation can be explained by stock borrow fees embedded in option prices when calculations assume zero borrow costs. This is an important warning against interpreting an observed premium asymmetry as a pure forecast of investor expectations. [Journal of Financial Economics](https://doi.org/10.1016/j.jfineco.2025.104153)

Bali et al. (2017) derive option-return moments under the risk-neutral distribution and document systematic differences in volatility, skewness and kurtosis across option moneyness. This motivates careful normalization and moneyness controls when comparing OTM6/7/8 premiums. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2902209)

## Relevance to the Phase 11 hypothesis

The user's feature is not simply an implied-volatility skew. It is a finite-difference-like premium combination across three OTM distances for calls and puts, followed by a call-side versus put-side comparison.

This creates several plausible interpretations that the empirical study should distinguish rather than assume:

1. **Directional information hypothesis:** the premium spread contains information about the subsequent sign of the NIFTY move.
2. **Volatility/convexity hypothesis:** the spread mostly reflects the shape of the option-price curve with respect to moneyness rather than direction.
3. **Liquidity/market-making hypothesis:** the signal may be affected by bid/ask spreads, stale quotes, or differential demand for OTM tails.
4. **Regime hypothesis:** the relation may change with volatility, sentiment, or market state.
5. **Structural-change hypothesis:** NIFTY expiry rules and strike conventions changed over time, so a pooled estimate may hide regime differences.

## Research gap

The initial literature search did not identify a peer-reviewed study testing this exact NIFTY weekly 4-DTE:

**(OTM7 + OTM8 − OTM6)_call versus (OTM7 + OTM8 − OTM6)_put**

directional classifier through the weekly expiry.

Therefore, the empirical contribution of Phase 11 is framed as a reproducible hypothesis test rather than as a claim that the formula is already academically established.

## Literature implications for methodology

- Use continuous signal values in addition to the binary rule.
- Test market-state interactions.
- Separate statistical and economic significance.
- Use out-of-sample validation.
- Control for liquidity and quote quality.
- Treat the September 2025 NIFTY expiry-day change as a structural break.
- Avoid attributing predictive power automatically to “sentiment” without testing alternative mechanisms.
