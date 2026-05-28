# Problem Statement: Customer Churn Prediction

## What Is Customer Churn?

Customer churn happens when an existing customer stops using a company's product or service. In subscription businesses, churn usually means a customer cancels their plan, does not renew, or moves to a competitor.

## Why Customers Leave

Common reasons include:

- High monthly charges or poor perceived value
- Short-term contracts with no loyalty lock-in
- Poor customer service experience
- Better offers from competitors
- Low product usage or lack of engagement
- Billing issues or payment friction
- Product features that do not match customer needs

## Business Impact

Churn directly affects revenue, growth, and customer lifetime value. Predicting churn helps a business:

- Identify high-risk customers early
- Prioritize retention campaigns
- Reduce revenue leakage
- Improve customer experience
- Allocate sales and support resources more efficiently

## Machine Learning Framing

This is a binary classification problem.

- Input: customer demographic, subscription, billing, and usage features
- Target: churn status
- Output: churn prediction and churn probability

The model predicts whether a customer belongs to one of two classes:

- `0`: No Churn
- `1`: Churn

## Objective

Build a machine learning system that predicts customer churn and explains key churn drivers so the business can take targeted retention actions.

## Success Metrics

Primary metrics:

- Recall: finds as many churn customers as possible
- Precision: ensures retention campaigns target genuinely risky customers
- F1 score: balances precision and recall
- ROC-AUC: measures ranking quality of churn probabilities

Accuracy is useful, but it should not be the only metric because churn datasets are often imbalanced.

