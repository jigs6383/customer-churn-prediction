# Business Insights Template

Use this document after running EDA and model evaluation.

## Key Churn Drivers

Document the strongest churn indicators from:

- EDA charts
- Correlation analysis
- Feature importance
- Model coefficients

Example insights:

- Customers on month-to-month contracts churn more than customers on long-term contracts.
- Customers with high monthly charges and low tenure are a high-risk group.
- Customers using fewer services may be less engaged and more likely to leave.

## High-Risk Customer Segments

Describe the segments that need retention action:

- New customers in the first 6 months
- Month-to-month contract users
- Customers with high monthly charges
- Customers with low service count

## Recommended Business Actions

- Offer retention discounts to high-probability churn customers.
- Promote annual contracts to month-to-month customers.
- Improve onboarding for new customers.
- Create service bundles for low-engagement customers.
- Trigger support outreach when churn probability crosses a chosen threshold.

## Revenue Loss Estimation

Estimate potential revenue at risk:

```text
Revenue at risk = Sum monthly charges of high-risk customers
Annualized risk = Revenue at risk * 12
```

## Decision Scientist Summary

This project translates model outputs into business decisions by identifying who is likely to churn, why they may churn, and what action the business can take.

