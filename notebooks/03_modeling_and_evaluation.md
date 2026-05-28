# 03 Modeling and Evaluation

Run:

```bash
python src/train_model.py --input dataset/processed/churn_clean.csv
```

Review:

- `outputs/reports/model_metrics.csv`
- `outputs/reports/confusion_matrices.json`
- `outputs/reports/feature_importance.csv`

Important metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

For churn, focus on recall and precision. A business usually wants to find churn customers early, but it also wants retention campaigns to be cost-effective.

