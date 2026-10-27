
import random


EXERCISES = [
    {
        "name": "Marching in Place",
        "equipment": "None",
        "location": "Both",
        "goals": ["Fat loss", "General fitness", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 2,
        "reps": "60 seconds",
        "rest": 30,
        "impact": "low",
    },
    {
        "name": "Bodyweight Squats",
        "equipment": "None",
        "location": "Both",
        "goals": ["Fat loss", "Muscle building", "General fitness"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 3,
        "reps": "10-12",
        "rest": 60,
        "impact": "moderate",
    },
    {
        "name": "Wall Push-ups",
        "equipment": "None",
        "location": "Both",
        "goals": ["Muscle building", "General fitness"],
        "levels": ["Beginner", "Intermediate"],
        "sets": 3,
        "reps": "8-12",
        "rest": 45,
        "impact": "low",
    },
    {
        "name": "Glute Bridges",
        "equipment": "Mat",
        "location": "Both",
        "goals": ["Muscle building", "General fitness"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 3,
        "reps": "12-15",
        "rest": 45,
        "impact": "low",
    },
    {
        "name": "Standing Knee Raises",
        "equipment": "None",
        "location": "Both",
        "goals": ["Fat loss", "General fitness", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 2,
        "reps": "12 per side",
        "rest": 30,
        "impact": "low",
    },
    {
        "name": "Dumbbell Rows",
        "equipment": "Dumbbells",
        "location": "Both",
        "goals": ["Muscle building", "General fitness"],
        "levels": ["Intermediate", "Advanced"],
        "sets": 3,
        "reps": "10-12",
        "rest": 60,
        "impact": "moderate",
    },
    {
        "name": "Dumbbell Shoulder Press",
        "equipment": "Dumbbells",
        "location": "Both",
        "goals": ["Muscle building"],
        "levels": ["Intermediate", "Advanced"],
        "sets": 3,
        "reps": "8-10",
        "rest": 60,
        "impact": "moderate",
    },
    {
        "name": "Brisk Walking",
        "equipment": "None",
        "location": "Both",
        "goals": ["Fat loss", "General fitness", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 1,
        "reps": "5 minutes",
        "rest": 0,
        "impact": "low",
    },
    {
        "name": "Plank",
        "equipment": "Mat",
        "location": "Both",
        "goals": ["Fat loss", "Muscle building", "General fitness"],
        "levels": ["Intermediate", "Advanced"],
        "sets": 3,
        "reps": "20-30 seconds",
        "rest": 45,
        "impact": "moderate",
    },
    {
        "name": "Jumping Jacks",
        "equipment": "None",
        "location": "Both",
        "goals": ["Fat loss", "Endurance"],
        "levels": ["Intermediate", "Advanced"],
        "sets": 3,
        "reps": "30 seconds",
        "rest": 45,
        "impact": "high",
    },
    {
        "name": "Dumbbell Biceps Curls",
        "equipment": "Dumbbells",
        "location": "Both",
        "goals": ["Muscle building"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 3,
        "reps": "10-12",
        "rest": 45,
        "impact": "low",
    },
    {
        "name": "Calf Raises",
        "equipment": "None",
        "location": "Both",
        "goals": ["General fitness", "Muscle building", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 2,
        "reps": "12-15",
        "rest": 30,
        "impact": "low",
    },
    {
        "name": "Stationary Cycling",
        "equipment": "Exercise bike",
        "location": "Gym",
        "goals": ["Fat loss", "General fitness", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 1,
        "reps": "5 minutes",
        "rest": 0,
        "impact": "low",
    },
    {
        "name": "Treadmill Walking",
        "equipment": "Treadmill",
        "location": "Gym",
        "goals": ["Fat loss", "General fitness", "Endurance"],
        "levels": ["Beginner", "Intermediate", "Advanced"],
        "sets": 1,
        "reps": "5 minutes",
        "rest": 0,
        "impact": "low",
    },
]


def generate_workout(goal, level, environment, duration):
    """Generate a workout using local Python rules."""

    duration = int(duration)

    if duration < 10:
        raise ValueError("Choose a workout duration of at least 10 minutes.")

    location = "Gym" if environment == "At the gym" else "Home"

    candidates = [
        exercise
        for exercise in EXERCISES
        if goal in exercise["goals"]
        and level in exercise["levels"]
        and exercise["location"] in [location, "Both"]
    ]

    if not candidates:
        raise ValueError(
            "No suitable exercises found. Try another goal or experience level."
        )

    random.shuffle(candidates)

    warmup_minutes = max(3, min(5, duration // 6))
    cooldown_minutes = max(2, min(5, duration // 8))
    main_minutes = duration - warmup_minutes - cooldown_minutes

    selected = []
    estimated_minutes = 0

    # Approximate time for each exercise, including rest.
    for exercise in candidates:
        if len(selected) >= 6:
            break

        exercise_minutes = (
            3
            if exercise["sets"] <= 2
            else 4
        )

        if estimated_minutes + exercise_minutes <= main_minutes:
            selected.append(exercise)
            estimated_minutes += exercise_minutes

    if not selected:
        selected = [candidates[0]]

    return {
        "goal": goal,
        "level": level,
        "environment": environment,
        "duration": duration,
        "warmup_minutes": warmup_minutes,
        "cooldown_minutes": cooldown_minutes,
        "main_minutes": main_minutes,
        "exercises": selected,
    }
