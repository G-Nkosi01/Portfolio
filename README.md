\# Credit Risk Prediction Using Logistic Regression



\---



\## Business Problem



Banks face financial losses when borrowers default on loans. Accurately identifying high-risk borrowers before issuing loans is therefore critical for effective risk management.



This project develops a predictive model to estimate the probability of loan default using borrower characteristics. The goal is to help lenders make better lending decisions and reduce potential credit losses.



\---



\## Dataset



The dataset used in this project is the Lending Club Loan Dataset, sourced from Kaggle.



It contains historical loan application data including borrower financial information, credit history, and loan performance.



\---



\## Project Objective



The objective of this project is to build a predictive model that estimates the probability of borrower default and demonstrate how data-driven credit risk assessment can support better lending decisions.



\---



\## Approach



The analysis focuses on borrower characteristics that influence default risk.



Key variables include:



\- \*\*Income\*\* – borrower income level  

\- \*\*Age\*\* – grouped into bins (18–25, 26–35, 36–50, 50+)  

\- \*\*Employment Length\*\* – total years of employment  

\- \*\*Loan Amount\*\* – amount requested or issued  

\- \*\*Credit History\*\* – borrower credit record  

\- \*\*Debt-to-Income Ratio\*\* – borrower debt relative to income  



These variables help explain borrower repayment behaviour and creditworthiness.



\---



\## Methodology



This project follows a typical credit risk modelling workflow used in banking and fintech.



\### 1. Data Cleaning

\- Remove duplicates

\- Standardize variable formats



\### 2. Missing Value Handling

\- Identify missing values

\- Apply appropriate imputation strategies



\### 3. Variable Binning

Continuous variables are grouped into categories to:



\- Improve model stability

\- Capture nonlinear relationships

\- Improve interpretability



\### 4. Weight of Evidence (WOE) Transformation



WOE encoding transforms categorical variables to measure the strength of the relationship between predictor variables and default outcomes.



\### 5. Information Value (IV) Feature Selection



Information Value measures the predictive power of each variable and helps identify the most informative features (for example: credit score, loan amount, or debt ratio).



\### 6. Logistic Regression Modelling



Logistic regression is used to estimate the probability of default because it offers:



\- High interpretability

\- Probability-based predictions

\- Strong suitability for credit risk modelling



\---



\## Model Evaluation



The model will be evaluated using standard classification metrics:



\- Accuracy

\- ROC Curve

\- Area Under the Curve (ROC-AUC)

\- Confusion Matrix



These metrics help assess how well the model distinguishes between defaulting and non-defaulting borrowers.



\---



\## Key Findings



This section will summarize insights discovered during the analysis, such as:



\- Which borrower characteristics most strongly influence default risk

\- Patterns in loan defaults across income levels or debt ratios

\- Segments of borrowers with higher probability of default



\---



\## Business Impact



This model helps lenders identify high-risk borrowers before loan approval.



By incorporating default probability into lending decisions, financial institutions can:



\- Reduce loan default rates

\- Improve portfolio risk management

\- Minimize financial losses



Even a small reduction in default rates can lead to significant cost savings for lenders issuing large volumes of loans.



\---

Link to similar analysis:

https://www.kaggle.com/code/sunnyboyngobeni/crm-credit-risk-modelling-and-analysis

