# **Causal Inference from Simulated Data: Separating Prognostic and Predictive Contributions**

## **1. Introduction**
This project demonstrates how to estimate treatment effects and decompose them into **prognostic** and **predictive** components, using a fully simulated dataset where the true treatment effect is known.  

Such an approach is relevant in contexts like:
- **Clinical trials** → identifying patient characteristics that influence baseline risk vs. treatment response
- **Marketing campaigns** → finding customer attributes that predict higher responsiveness to promotions
- **Policy interventions** → uncovering factors that shape heterogeneous policy impacts

We combine **meta-learners** for treatment effect estimation with **function separation** to interpret the drivers of both baseline outcomes and treatment effect heterogeneity.

---

## **2. Data**
We simulate a dataset containing:
- **Features**: `x0`–`x9`
- **Treatment indicator**: `treatment` (binary)
- **Observed outcome**: `outcome`
- **Ground truth potential outcomes**: `mu0` (control), `mu1` (treated)
- **True treatment effect**: `tau` = `mu1` − `mu0`

**Why simulation?**  
It allows benchmarking model performance against known truth (**true ATE**, **true ITE**).

---

## **3. Methods**
We follow a structured pipeline:

1. **Covariate Balance Check**  
   - Standardized Mean Differences (SMD) by treatment group for each feature.

2. **ATE Estimation (Doubly Robust)**  
   - Augmented Inverse Probability Weighting (AIPW) to check baseline bias.

3. **Meta-Learners for ITE/CATE**  
   - **T-Learner**: separate models for treated and control outcomes.  
   - **X-Learner**: more efficient for unbalanced data.

4. **Evaluation Metrics**  
   - **ATE** error (absolute difference from truth)  
   - **PEHE** (Precision in Estimating Heterogeneous Effects)

5. **Feature Attribution for Heterogeneity**  
   - Gain importance, permutation importance, and SHAP values for ITE models.

6. **Prognostic vs Predictive Decomposition**  
   - Model:  
     \[
     Y = g(X) + T \cdot f(X) + \varepsilon
     \]  
     where:  
       - `g(X)`: baseline outcome (**prognostic function**)  
       - `f(X)`: treatment effect modifier (**predictive function**)  

---

## **4. Results**

### **Key Metrics**
| Model / Step | ATE (est.) | True ATE | PEHE | Notes |
|--------------|------------|----------|------|-------|
| AIPW         | 0.8698     | 1.0054   | —    | Slight underestimation |
| T-Learner    | 0.9190     | 1.0054   | 1.1066 | Captures ATE, noisier ITE |
| X-Learner    | 0.9281     | 1.0054   | 0.7116 | Best ITE performance |
| f(X) model   | 0.5629     | 1.0054   | Corr(f̂, τ) = 0.457 | Predictive function underestimates ATE |

---

### **Insights**
- **x0** is consistently the strongest **predictive** feature (effect modifier) across all methods.
- **Prognostic** features (affecting baseline outcome) differ — `x9` and `x2` are top drivers.
- Predictive model explains ~45% of variation in true treatment effects but underestimates their magnitude.
- Meta-learners recover ATE reasonably well; **X-Learner** performs best for heterogeneous effects.

---

## **5. Visual Highlights**
- **Covariate balance plots** (SMD) before modeling
- **Estimated vs True ITE scatter** (X-Learner)
- **Prognostic vs Predictive feature importance** (gain, permutation, SHAP)
- **SHAP beeswarm plots** for `g(X)` and `f(X)`

---

## **6. Conclusions**
1. **Meta-learners** effectively estimate both ATE and ITE, with the X-Learner showing superior precision for heterogeneity.  
2. **Function separation** reveals different drivers for baseline outcomes vs. treatment response, improving interpretability.  
3. **x0** is a key treatment effect modifier, while **x9** and **x2** dominate baseline risk.  
4. Predictive modeling of heterogeneity can guide targeting in real-world interventions.

---

## **7. Next Steps**
- Implement **doubly robust learners** (R-Learner, DR-Learner)
- Test on **real-world** datasets (clinical or marketing)
- Explore **non-linear interaction models** (causal forests, neural nets)
- Perform **uncertainty quantification** (bootstrap CIs for ITE/ATE)

---


## How to Run
Start with the exploratory notebook:
notebooks/01_explore_data.ipynb

Then move on to:
notebooks/02_modeling.ipynb

---

## References
Hill, J. (2011). Bayesian nonparametric modeling for causal inference. Journal of Computational and Graphical Statistics

Benchmark data: https://www.fredjo.com

## 📦 Setup Instructions
```bash
## Steps to correctly install the dependent libraries on local machine
git clone https://github.com/yotamdery/causal-inference-treatment-effect.git

python3.12 -m venv .venv ( The python version used for this project)

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

For convenience (not mandatory) - create .vscode/settings.json with the following: 
{ "python.terminal.activateEnvironment": true, 
"python.defaultInterpreterPath": ".venv/bin/python3" }