from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "workout_random_forest.joblib"


def load_model():
    """Load the previously trained Random Forest pipeline."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run 'python train_model.py' "
            "from the AIFitnessCoach project folder first."
        )

    return joblib.load(MODEL_PATH)


# Load the saved model once when the module is imported.
_model = load_model()


def recommend_workout_focus(profile):
    """Predict a workout focus from the user's fitness profile."""
    required_fields = [
        "age",
        "weight",
        "goal",
        "level",
        "environment",
        "duration",
    ]

    missing_fields = [
        field for field in required_fields if field not in profile
    ]

    if missing_fields:
        raise ValueError(
            "Missing profile fields: " + ", ".join(missing_fields)
        )

    input_data = pd.DataFrame([{
        "age": int(profile["age"]),
        "weight": float(profile["weight"]),
        "goal": str(profile["goal"]),
        "level": str(profile["level"]),
        "environment": str(profile["environment"]),
        "duration": int(profile["duration"]),
    }])

    prediction = _model.predict(input_data)[0]
    probabilities = _model.predict_proba(input_data)[0]
    confidence = float(max(probabilities))

    return {
        "focus": str(prediction),
        "confidence": confidence,
    }