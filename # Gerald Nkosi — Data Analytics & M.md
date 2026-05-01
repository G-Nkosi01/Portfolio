# Gerald Nkosi — Data Analytics & Machine Learning Portfolio

Driven, analytical structural engineer with a growing interest in data science. This portfolio explores real-world questions through data, focusing on insight extraction, visualisation and developing skills in modelling and data-driven decision making.

---

## Projects

---

### 🔹  Credit Risk Prediction Using Logistic Regression

**Task:** Analyse historical Lending Club loan data to build a predictive machine learning model that forecasts whether a borrower will default on their loan. The model evaluates borrower-specific financial metrics — such as interest rate, debt-to-income ratio, revolving credit utilisation, and employment length — to classify loans as either **"Fully Paid"** or **"Defaulted."** Focus on identifying the key financial signals that distinguish high-risk borrowers from low-risk ones, using a dataset of over 1 million real loan records to build and evaluate a logistic regression classifier.

**Skills:** Exploratory Data Analytics, Feature Engineering, Predictive Modelling, Model Evaluation, Data Visualisation (Seaborn/Matplotlib)

**Tools:** Python, Pandas, NumPy, Scikit-learn, Seaborn/Matplotlib

***Features to consider***

Interest rate assigned to the loan — higher rates signal that Lending Club already assessed the borrower as risky.

Debt-to-income ratio per borrower — measures existing financial pressure relative to income.

Revolving credit utilisation — how much of a borrower's available credit they are actively using before taking the loan.

Loan grade and sub-grade assigned by Lending Club — encodes the platform’s internal risk assessment (A through G).

Loan purpose — whether the borrower is consolidating debt, funding a small business, or covering personal expenses affects default likelihood.

Employment length — provides additional context around borrower stability.

***Modelling approach***

Treat as a binary classification problem predicting **Defaulted (1)** vs **Fully Paid (0).**

Account for class imbalance (~80/20 split) using `class_weight='balanced'` in logistic regression to avoid the model simply predicting **"Fully Paid"** for every loan.

Optionally extend to probability-based scoring rather than hard classifications, allowing a lender to set their own risk threshold based on business tolerance.

Evaluate using **ROC-AUC** as the primary metric rather than accuracy, since accuracy is misleading on imbalanced datasets.

Use confusion matrices and precision-recall analysis for deeper performance interpretation.

***Visualizations***

Default rate by loan grade (A through G) — shows how Lending Club’s own risk ratings align with actual outcomes.

Interest rate distribution by loan outcome — one of the clearest visual separators between defaulters and fully paid borrowers.

Debt-to-income and revolving utilisation boxplots by outcome — highlights financial pressure signals present before default.

Feature coefficient chart from the logistic regression model — shows which variables most strongly push a borrower toward or away from default.

ROC curve and confusion matrix visualisations to assess classifier performance.

---

### 🔹 The Cost of Utilities

**Task**: Analyse data set sourced from Deutsche Bank between 2020-2025 which includes the monthly costs (USD) of basic utilities such as electricity, heating, cooling, water and waste removal. Present the results of the capital cities of the different continents (Europe, Middle East, Asia, N.America, S.America, Oceania and Africa), answer questions that arise from the visualised data, e.g. what is driving the increase/decrease (is it inline with inflation)?

**Skills**: Exploratory Data Analytics, Data Visualisation (Seaborn/Matplotlib), NumPy
**Tools**: Python, Pandas, Seaborn/Matplotlib

---
### 🔹 🏎️ F1 10th Place Cup Predictor

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

Feature importance charts from the predictive model to understand which factors influence the 10th place outcome the most.
---


## 📞 Contact

[LinkedIn](https://www.linkedin.com/in/gerald-nkosi-571392221/)
