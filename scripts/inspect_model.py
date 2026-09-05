"""Smoke check the recovered trusted model, without training or measuring accuracy."""

import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn


ROOT = Path(__file__).resolve().parents[1]


def main():
    metadata = json.loads((ROOT / 'models/baseline-metadata.json').read_text(encoding='utf-8'))
    path = ROOT / metadata['artifact']
    if hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']:
        raise ValueError('The model does not match the recovered trusted artifact')
    if sklearn.__version__ != metadata['sklearn_version_in_artifact']:
        raise RuntimeError('Use requirements-model.txt to match the artifact scikit-learn version')

    model = joblib.load(path)
    if list(model.feature_names_in_) != metadata['feature_names']:
        raise ValueError('Unexpected feature order')
    if model.classes_.tolist() != metadata['classes']:
        raise ValueError('Unexpected class order')
    if model.n_estimators != metadata['n_estimators']:
        raise ValueError('Unexpected tree count')
    dataset = pd.read_csv(ROOT / 'data/processed/final_dataset.csv')
    inputs = dataset[metadata['feature_names']].iloc[metadata['sample_row_indices']]
    probabilities = model.predict_proba(inputs)
    if not np.isfinite(probabilities).all() or (probabilities < 0).any() or (probabilities > 1).any():
        raise ValueError('Invalid probability values')
    np.testing.assert_allclose(probabilities.sum(axis=1), 1.0, atol=1e-12, rtol=0)
    np.testing.assert_allclose(probabilities, metadata['sample_probabilities'], atol=1e-12, rtol=0)
    print(f'PASS: {model.n_estimators} trees, expected features/classes, and five probability examples.')
    print('Class order:', ', '.join(model.classes_))
    print('No training performed. This check does not establish held-out or live accuracy.')


if __name__ == '__main__':
    main()
