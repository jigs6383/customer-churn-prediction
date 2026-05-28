# 02 Preprocessing and EDA

Run:

```bash
python src/make_sample_data.py
python src/preprocess.py --input dataset/raw/customer_churn_sample.csv --output dataset/processed/churn_clean.csv
python src/eda.py --input dataset/processed/churn_clean.csv
```

Review charts in:

```text
outputs/figures/
```

Questions to answer:

- What percentage of customers churn?
- Which variables are most associated with churn?
- Are newer customers more likely to churn?
- Do high monthly charges increase churn risk?

