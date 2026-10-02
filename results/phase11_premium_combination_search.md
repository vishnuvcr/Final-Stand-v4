# Phase 11 Premium Combination Search

- Development events: 101
- 2026 chronological holdout: 20
- Candidate engineered features: 78
- Threshold models: 156
- All non-empty raw-premium subsets: 63

## Selection rule
Models are selected using development-period 5-fold cross-validation only. The 2026 holdout is not used for feature/formula selection.

## Best threshold candidate
- Feature: logratio__ce_otm6__ce_otm7
- Mapping: high_bull
- Development accuracy: 0.5941
- 2026 holdout accuracy: 0.6000

## Best raw-premium subset logistic model
- Features: ce_otm6+ce_otm7+pe_otm7
- Development CV accuracy: 0.5038
- Development fitted accuracy: 0.5743
- 2026 holdout accuracy: 0.6000

## Multiple-testing diagnostic
- Permutation p-value for maximum threshold accuracy across the entire engineered feature library: 0.511800

The holdout result is the relevant out-of-sample result. No candidate is promoted to a trading strategy merely because it ranked highly during development.
