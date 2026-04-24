# Machine Learning Basics

## Supervised Learning
Supervised learning uses labeled data to train models. Common algorithms include:
- **Linear Regression**: For continuous target variables
- **Logistic Regression**: For binary classification
- **Decision Trees**: Non-linear, interpretable models
- **Random Forest**: Ensemble of decision trees, reduces overfitting
- **Neural Networks**: Deep learning for complex patterns

## Unsupervised Learning
No labels — the model discovers patterns:
- **K-Means Clustering**: Groups data into K clusters
- **PCA**: Dimensionality reduction preserving variance
- **DBSCAN**: Density-based clustering, handles noise

## Model Evaluation
- **Accuracy**: Correct predictions / total predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under the Receiver Operating Characteristic curve

## Overfitting vs Underfitting
- **Overfitting**: Model memorizes training data, poor generalization. Fix with regularization, dropout, more data, or simpler model.
- **Underfitting**: Model too simple to capture patterns. Fix with more features, complex model, or more training.

## Cross-Validation
Use k-fold cross-validation (typically k=5 or k=10) to evaluate model performance reliably. This prevents optimistic bias from a single train/test split.

## Feature Engineering
Good features are more important than complex models. Techniques include:
- Normalization/Standardization
- One-hot encoding for categorical variables
- Feature interaction terms
- Polynomial features
- Domain-specific transformations
