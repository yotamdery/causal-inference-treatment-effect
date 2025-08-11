import numpy as np
import pandas as pd
from scipy.special import expit  # Sigmoid
import matplotlib.pyplot as plt

def simulate_causal_data(n=1000, p=10, seed=42, hetero_effect=False):
    np.random.seed(seed)

    # 1. Covariates
    X = np.random.normal(0, 1, size=(n, p))
    X_df = pd.DataFrame(X, columns=[f'x{i}' for i in range(p)])

    # 2. True propensity scores
    beta_prop = np.random.uniform(-0.5, 0.5, size=p)
    logits = X @ beta_prop
    e_X = expit(logits)  # propensity scores

    # 3. Treatment assignment
    T = np.random.binomial(1, e_X)

    # 4. Outcome model
    beta_mu0 = np.random.uniform(-1, 1, size=p)
    mu0 = X @ beta_mu0

    if hetero_effect:
        tau = 1 + 0.5 * X[:, 0]  # treatment effect depends on x0
    else:
        tau = 2.0  # constant treatment effect

    Y0 = mu0 + np.random.normal(0, 1, size=n)
    Y1 = mu0 + tau + np.random.normal(0, 1, size=n)

    # Observed outcome
    Y = Y0 * (1 - T) + Y1 * T

    df = X_df.copy()
    df['treatment'] = T
    df['outcome'] = Y
    df['mu0'] = mu0
    df['mu1'] = mu0 + tau
    df['tau'] = tau
    df['counterfactual'] = Y1 * (1 - T) + Y0 * T  # what would have happened
    df['propensity_score'] = e_X

    return df

# Example usage
df = simulate_causal_data(n=1000, p=10, hetero_effect=True)
# Save to CSV or pickle to reuse
df.to_csv("data/simulated_data.csv", index=False)