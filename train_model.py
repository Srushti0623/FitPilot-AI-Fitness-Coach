from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

DATASET_PATH = DATA_DIR / "workout_recommendations.csv"
MODEL_PATH = MODEL_DIR / "workout_random_forest.joblib"
REPORT_PATH = MODEL_DIR / "model_evaluation.txt"
MATRIX_PATH = MODEL_DIR / "confusion_matrix.png"

RANDOM_SEED = 42

FEATURES = [
    "age",
    "weight",
    "goal",
    "level",
    "environment",
    "duration",
]

CATEGORICAL_FEATURES = ["goal", "level", "environment"]
NUMERIC_FEATURES = ["age", "weight", "duration"]

GOALS = [
    "Fat loss",
    "Muscle building",
    "General fitness",
    "Endurance",
    "Flexibility",
]

LEVELS = ["Beginner", "Intermediate", "Advanced"]
ENVIRONMENTS = ["At home", "At the gym"]
DURATIONS = [20, 30, 45, 60]


def assign_demo_focus(row):
    """Assign a demonstration label using an explicit training rule."""
    goal = row["goal"]
    level = row["level"]
    duration = row["duration"]

    if goal == "Muscle building":
        return "Strength training"

    if goal == "Flexibility":
        return "Mobility and flexibility"

    if goal == "Endurance":
        return "Endurance training"

    if goal == "Fat loss":
        if level == "Advanced" and duration >= 45:
            return "Endurance training"
        return "Low-impact cardio"

    return "Balanced full-body"


def create_demo_dataset(number_of_rows=1800):
    """Create repeatable example data for testing the ML pipeline."""
    rng = np.random.default_rng(RANDOM_SEED)

    data = pd.DataFrame({
        "age": rng.integers(18, 61, size=number_of_rows),
        "weight": np.round(rng.uniform(45, 120, size=number_of_rows), 1),
        "goal": rng.choice(GOALS, size=number_of_rows),
        "level": rng.choice(LEVELS, size=number_of_rows),
        "environment": rng.choice(
            ENVIRONMENTS, size=number_of_rows
        ),
        "duration": rng.choice(DURATIONS, size=number_of_rows),
    })

    data["focus"] = data.apply(assign_demo_focus, axis=1)
    data.to_csv(DATASET_PATH, index=False)

    print(f"Demo dataset created: {DATASET_PATH}")
    print(f"Number of rows: {len(data)}")
    print("\nExample records:")
    print(data.head().to_string(index=False))

    return data


def train_and_evaluate():
    """Train, evaluate, save and report the Random Forest model."""
    data = create_demo_dataset()

    X = data[FEATURES]
    y = data["focus"]

    # Keep class proportions similar in both sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=12,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\nTraining Random Forest model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    print("\n========== MODEL EVALUATION ==========")
    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")
    print(f"Test accuracy: {accuracy:.2%}")
    print("\nClassification report:")
    print(report)

    # Save the complete pipeline, including preprocessing.
    joblib.dump(model, MODEL_PATH)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write("AI Fitness Coaching - Model Evaluation\n")
        file.write("Dataset: generated demonstration data\n")
        file.write("This score is not real-world validation.\n\n")
        file.write(f"Rows: {len(data)}\n")
        file.write(f"Training rows: {len(X_train)}\n")
        file.write(f"Testing rows: {len(X_test)}\n")
        file.write(f"Test accuracy: {accuracy:.2%}\n\n")
        file.write(report)

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        xticks_rotation=45,
    )
    plt.title("Random Forest - Demonstration Dataset")
    plt.tight_layout()
    plt.savefig(MATRIX_PATH, dpi=150)
    plt.close()

    print("\nFiles saved successfully:")
    print(f"Dataset: {DATASET_PATH}")
    print(f"Trained model: {MODEL_PATH}")
    print(f"Evaluation report: {REPORT_PATH}")
    print(f"Confusion matrix: {MATRIX_PATH}")


if __name__ == "__main__":
    train_and_evaluate()