cat > docs/DATA_PIPELINE.md <<'EOF'
# Data Pipeline Documentation

## Pipeline Stages

| Stage | Purpose | Input | Output |
|---|---|---|---|
| Collect | Obtain raw Iris data | sklearn Iris dataset | `iris_raw.csv` |
| Preprocess | Clean and prepare data | `iris_raw.csv` | `iris_preprocessed.csv` |
| Feature Engineering | Create useful features | `iris_preprocessed.csv` | `iris_features.csv` |
| Validate | Check schema, nulls and ranges | `iris_features.csv` | Validation result |

## Pipeline Flow

```text
Collect
   |
   v
Preprocess
   |
   v
Feature Engineering
   |
   v
Validate