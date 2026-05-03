# Drug Response Prediction (GDSC)

## Overview
This project builds machine learning models to predict drug response (LN_IC50) using genomic data. The goal is to understand how different cancer cell lines respond to various drugs, a key task in bioinformatics and personalized medicine.

## Dataset
- GDSC (Genomics of Drug Sensitivity in Cancer)
- Contains cancer cell line data and drug response measurements

## Methods
- Ridge Regression
- HistGradientBoosting Regressor
- Feature engineering using genomic and biological variables
- GroupShuffleSplit to prevent data leakage across related samples

## Process
1. Cleaned and prepared large-scale biological dataset (~240,000+ samples)
2. Selected relevant genomic features (e.g., TCGA_DESC, TARGET_PATHWAY)
3. Trained regression models to predict LN_IC50
4. Evaluated model performance using:
   - RMSE
   - MAE
   - R²

## Results
- Achieved:
  - R² ≈ 0.74
  - RMSE ≈ 1.4
- Demonstrated strong predictive performance on drug sensitivity

## Tools Used
- Python
- pandas
- NumPy
- scikit-learn

## Notes
Due to dataset size, only a sample or reference link may be included. Full dataset available at:
https://www.cancerrxgene.org/
