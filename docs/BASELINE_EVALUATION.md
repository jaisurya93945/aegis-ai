# AegisAI Baseline Evaluation

## Overview

AegisAI currently uses a TF-IDF + Logistic Regression classifier as its machine-learning prompt injection baseline.

The model is evaluated using fixed validation and test splits from the Neuralchemy dataset.

## Model

- Feature extraction: TF-IDF
- N-grams: unigram + bigram
- Classifier: Logistic Regression
- Class weighting: balanced
- Random state: 42
- Decision threshold: 0.30

The threshold was selected through threshold analysis because it produced the strongest F1 score among the evaluated thresholds while maintaining high attack recall.

## Validation Results

| Metric | Result |
|---|---:|
| Samples | 941 |
| Accuracy | 94.47% |
| Precision | 94.14% |
| Recall | 96.25% |
| F1 | 95.19% |
| False Positive Rate | 7.86% |
| False Negative Rate | 3.75% |

### Validation Confusion Matrix

```text
[[375, 32],
 [20, 514]]
