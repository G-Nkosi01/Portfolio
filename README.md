# Gerald Nkosi — Data Analytics & Machine Learning Portfolio

Driven, analytical structural engineer with a growing interest in data science. This portfolio explores real-world questions through data, focusing on insight extraction, visualisation and developing skills in modelling and data-driven decision making.

---

## Projects

---

### 🔹 The Cost of Utilities (Ongoing)

**Task**: Analyse data set sourced from Deutsche Bank between 2020-2025 which includes the monthly costs (USD) of basic utilities such as electricity, heating, cooling, water and waste removal. Present the results of the capital cities of the different continents (Europe, Middle East, Asia, N.America, S.America, Oceania and Africa), answer questions that arise from the visualised data, e.g. what is driving the increase/decrease (is it inline with inflation)?

**Skills**: Exploratory Data Analytics, Data Visualisation (Seaborn/Matplotlib), NumPy
**Tools**: Python, Pandas, Seaborn/Matplotlib

---
### 🔹 🏎️ F1 10th Place Cup Predictor (Ongoing)

**Task**: Analyse historical Formula 1 race data to build a predictive machine learning model that forecasts which driver will finish in 10th position for each race weekend. The game allows users to select three drivers: the main “magical 10th place pick” and two additional drivers for 9th and 11th positions (the exact order for these two is not critical). Focus on driver-specific performance metrics, such as average finishing position per race, trends over multiple seasons, and performance in specific race tracks or conditions, to create accurate predictions for the remainder of the 2025 season and potentially for 2026.

**Skills**: Exploratory Data Analytics, Feature Engineering, Predictive Modelling, Model Evaluation, Data Visualisation (Seaborn/Matplotlib)

**Tools**: Python, Pandas, NumPy, Scikit-learn, Seaborn/Matplotlib

***Extra Project Notes / Tips***:

***Features to consider***:

Average finishing position per driver per race.

Track-specific driver trends (e.g., driver consistently performs better on street circuits vs traditional tracks).

Temporal trends (e.g., improvement or decline across the season or era).

Weather conditions for each race weekend (if available).

***Modelling approach***:

Treat it as a classification problem to predict the driver finishing 10th.

Optionally, consider predicting positions 9–11 as a multi-class problem, but only the 10th place prediction counts toward scoring.

Evaluate models using accuracy, F1-score, or a custom scoring function aligned with the game rules.

***Visualizations***:

Driver performance trends over time.

Average finishing positions per track or race type.

### Feature importance charts from the predictive model to understand which factors influence the 10th place outcome the most.
---
# Credit Risk Prediction Using Logistic Regression
---
## Business Problem

Banks face financial losses when borrowers default on loans. Accurately identifying high-risk borrowers before issuing loans is therefore critical for effective risk management.

This project develops a predictive model to estimate the probability of loan default using borrower characteristics. The goal is to help lenders make better lending decisions and reduce potential credit losses.

---

## Dataset

The dataset used in this project is the Lending Club Loan Dataset, sourced from Kaggle.
It contains historical loan application data including borrower financial information, credit history, and loan performance.

---

## Project Objective

The objective of this project is to build a predictive model that estimates the probability of borrower default and demonstrate how data-driven credit risk assessment can support better lending decisions.

---

## Approach

The analysis focuses on borrower characteristics that influence default risk.

Key variables include:

- **Income** – borrower income level  
- **Age** – grouped into bins (18–25, 26–35, 36–50, 50+)  
- **Employment Length** – total years of employment  
- **Loan Amount** – amount requested or issued  
- **Credit History** – borrower credit record  
- **Debt-to-Income Ratio** – borrower debt relative to income  

These variables help explain borrower repayment behaviour and creditworthiness.

---

## Methodology

This project follows a typical credit risk modelling workflow used in banking and fintech.

### 1. Data Cleaning
- Remove duplicates
- Standardize variable formats

### 2. Missing Value Handling
- Identify missing values
- Apply appropriate imputation strategies

### 3. Variable Binning
Continuous variables are grouped into categories to:

- Improve model stability
- Capture nonlinear relationships
- Improve interpretability

### 4. Weight of Evidence (WOE) Transformation

WOE encoding transforms categorical variables to measure the strength of the relationship between predictor variables and default outcomes.

### 5. Information Value (IV) Feature Selection

Information Value measures the predictive power of each variable and helps identify the most informative features (for example: credit score, loan amount, or debt ratio).

### 6. Logistic Regression Modelling

Logistic regression is used to estimate the probability of default because it offers:

- High interpretability
- Probability-based predictions
- Strong suitability for credit risk modelling
---

## Model Evaluation

The model will be evaluated using standard classification metrics:

- Accuracy
- ROC Curve
- Area Under the Curve (ROC-AUC)
- Confusion Matrix

These metrics help assess how well the model distinguishes between defaulting and non-defaulting borrowers.

---

## Key Findings

This section will summarize insights discovered during the analysis, such as:

- Which borrower characteristics most strongly influence default risk
- Patterns in loan defaults across income levels or debt ratios
- Segments of borrowers with higher probability of default

---

## Business Impact

This model helps lenders identify high-risk borrowers before loan approval.

By incorporating default probability into lending decisions, financial institutions can:

- Reduce loan default rates
- Improve portfolio risk management
- Minimize financial losses

Even a small reduction in default rates can lead to significant cost savings for lenders issuing large volumes of loans.

---

## 📞 Contact

[LinkedIn](https://www.linkedin.com/in/gerald-nkosi-571392221/)

