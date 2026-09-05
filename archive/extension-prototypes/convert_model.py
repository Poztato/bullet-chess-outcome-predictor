"""
Convert the trained Random Forest model from .pkl to JSON format
for use in the Chrome extension's browser-based inference engine.
"""

import json
import joblib
import numpy as np
import os

def convert_rf_to_json(pkl_path, output_path):
    """Convert a scikit-learn RandomForestClassifier to JSON."""
    model = joblib.load(pkl_path)

    trees_json = []
    for tree in model.estimators_:
        t = tree.tree_
        trees_json.append({
            "feature": t.feature.tolist(),
            "threshold": [round(float(x), 6) for x in t.threshold],
            "children_left": t.children_left.tolist(),
            "children_right": t.children_right.tolist(),
            "value": [[int(v) for v in node[0]] for node in t.value]
        })

    model_json = {
        "feature_names": ["is_white", "avg_pr", "sesh_cnt", "elo_diff", "streak"],
        "classes": [str(c) for c in model.classes_],
        "n_trees": len(model.estimators_),
        "trees": trees_json
    }

    with open(output_path, "w") as f:
        json.dump(model_json, f)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Saved model.json ({size_mb:.2f} MB) with {len(trees_json)} trees")
    print(f"Classes: {model_json['classes']}")
    print(f"Features: {model_json['feature_names']}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(script_dir, "chessica_random_forest.pkl")
    output_path = os.path.join(script_dir, "..", "Chess Scraper", "model.json")

    if not os.path.exists(pkl_path):
        print(f"Error: {pkl_path} not found")
        exit(1)

    convert_rf_to_json(pkl_path, output_path)
    print(f"Output: {os.path.abspath(output_path)}")
