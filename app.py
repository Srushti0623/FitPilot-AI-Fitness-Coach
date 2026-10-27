import streamlit as st
import pandas as pd

from services.workout_generator import generate_workout
from services.workout_history import save_workout, get_workout_history
from services.ml_recommender import recommend_workout_focus
from services.chatbot import get_fitness_reply


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="FitPilot | AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CUSTOM CSS: MODERN FITNESS DASHBOARD
# ==================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #13B8A6;
        --primary-dark: #0F9488;
        --background: #F4F7FB;
        --card: #FFFFFF;
        --text: #172033;
        --muted: #68758A;
        --border: #E4EAF2;
    }

    .stApp {
        background: var(--background);
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.9);
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263244;
    }

    [data-testid="stSidebar"] * {
        color: #E5EAF2;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #CBD5E1;
    }

    [data-testid="stSidebar"] [data-testid="stForm"] {
        background: #1B2535;
        padding: 16px;
        border: 1px solid #2B394D;
        border-radius: 16px;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #263244;
        border-color: #3A4960;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif;
        color: #172033;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
    }

    h2 {
        font-weight: 750 !important;
    }

    p, label, li {
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 16px rgba(23, 32, 51, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.9rem;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #172033;
        font-weight: 800;
    }

    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid var(--primary);
        background: var(--primary);
        color: white;
        font-weight: 700;
        min-height: 42px;
        transition: 0.2s ease;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
        color: white;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 42px;
    }

    [data-testid="stForm"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: var(--primary);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stVegaLiteChart"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 8px;
    }

    .brand-mark {
        font-family: 'Manrope', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 2px;
    }

    .brand-mark span {
        color: #2DD4BF;
    }

    .sidebar-caption {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 18px;
    }

    .hero-card {
        background: linear-gradient(125deg, #102A43 0%, #164E63 55%, #0F766E 100%);
        color: white;
        border-radius: 22px;
        padding: 28px 30px;
        margin: 8px 0 22px 0;
        box-shadow: 0 12px 28px rgba(15, 118, 110, 0.15);
    }

    .hero-eyebrow {
        color: #99F6E4;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-title {
        color: white;
        font-family: 'Manrope', sans-serif;
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 10px;
    }

    .hero-copy {
        color: #D5E8EF;
        font-size: 0.98rem;
        max-width: 650px;
        line-height: 1.6;
    }

    .section-label {
        color: #68758A;
        text-transform: uppercase;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin: 8px 0 12px 0;
    }

    .info-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 4px 16px rgba(23, 32, 51, 0.025);
    }

    .info-card-title {
        color: #172033;
        font-size: 1.04rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .info-card-copy {
        color: #68758A;
        line-height: 1.55;
        font-size: 0.92rem;
    }

    .tag {
        display: inline-block;
        padding: 5px 10px;
        background: #CCFBF1;
        color: #115E59;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 800;
        margin: 2px 0 10px 0;
    }

    .footer-note {
        color: #8290A5;
        font-size: 0.8rem;
        text-align: center;
        padding: 18px 0 8px 0;
    }

    hr {
        border-color: #E4EAF2;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }

        .hero-card {
            padding: 22px;
        }

        .hero-title {
            font-size: 1.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "current_workout": None,
    "predicted_focus": None,
    "model_confidence": None,
    "saved_workout_key": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# BMI AND FITNESS INSIGHT FUNCTIONS
# ==================================================

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100

    if height_m <= 0:
        return None

    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Below the usual adult BMI range"
    elif bmi < 25:
        return "Usual adult BMI range"
    elif bmi < 30:
        return "Above the usual adult BMI range"
    return "High adult BMI range"


def get_fitness_insights(profile, bmi, bmi_category):
    insights = []

    goal = profile["goal"]
    level = profile["level"]
    duration = profile["duration"]
    environment = profile["environment"]

    if goal == "Fat loss":
        insights.append(
            "Build sustainable habits with regular activity, strength "
            "training, and a balanced eating pattern. Avoid crash diets."
        )
    elif goal == "Muscle building":
        insights.append(
            "Focus on progressive strength training, proper technique, "
            "adequate nutrition, and recovery between demanding sessions."
        )
    elif goal == "Endurance":
        insights.append(
            "Build aerobic fitness gradually. Alternate manageable sessions "
            "with appropriate recovery as your stamina improves."
        )
    elif goal == "Flexibility":
        insights.append(
            "Practice gentle mobility work regularly. Avoid forcing stretches "
            "or continuing through sharp pain."
        )
    else:
        insights.append(
            "Aim for a balanced routine with aerobic activity, strength work, "
            "mobility, and sufficient recovery."
        )

    if level == "Beginner":
        insights.append(
            "Start at a comfortable intensity, learn correct technique, "
            "and increase the difficulty gradually."
        )
    elif level == "Intermediate":
        insights.append(
            "Track consistency and progress gradually through repetitions, "
            "resistance, or duration when your current routine feels manageable."
        )
    else:
        insights.append(
            "Track your training load and recovery. Add easier sessions "
            "when fatigue begins to accumulate."
        )

    if duration <= 20:
        insights.append(
            "For a short session, prioritize a warm-up, a few key exercises, "
            "and a brief cool-down."
        )
    elif duration <= 30:
        insights.append(
            "Plan your exercises in advance so your 20–30 minute session "
            "can remain focused and manageable."
        )
    else:
        insights.append(
            "For longer sessions, pace yourself, take appropriate rest breaks, "
            "and drink water as needed."
        )

    if environment == "At home":
        insights.append(
            "Choose a clear, non-slip exercise space and select movements "
            "that suit your available equipment."
        )
    else:
        insights.append(
            "Use gym equipment with proper technique. Ask a qualified trainer "
            "for help if you are unsure how to use a machine."
        )

    if bmi_category == "Below the usual adult BMI range":
        insights.append(
            "Your BMI is below the usual adult range. If this is unexpected "
            "or you have concerns about nutrition or weight, consider speaking "
            "with a healthcare professional."
        )
    elif bmi_category == "Above the usual adult BMI range":
        insights.append(
            "BMI is above the usual adult range. It does not distinguish "
            "muscle from fat, so interpret it alongside your overall health "
            "and individual goals."
        )
    elif bmi_category == "High adult BMI range":
        insights.append(
            "BMI falls in a higher adult screening category. A healthcare "
            "professional can help interpret it alongside other health measures."
        )
    else:
        insights.append(
            "BMI falls within the usual adult screening range. Continue "
            "building strength, stamina, recovery, and consistency."
        )

    return insights


# ==================================================
# SIDEBAR BRANDING AND PROFILE
# ==================================================

st.sidebar.markdown(
    """
    <div class="brand-mark">Fit<span>Pilot</span></div>
    <div class="sidebar-caption">YOUR PERSONAL AI FITNESS COACH</div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Your profile")

with st.sidebar.form("fitness_profile_form"):
    user_name = st.text_input("Name", value="User")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=21,
        step=1,
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=250.0,
        value=60.0,
        step=0.5,
    )

    height_cm = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=230.0,
        value=160.0,
        step=1.0,
    )

    goal = st.selectbox(
        "Fitness goal",
        [
            "Fat loss",
            "Muscle building",
            "General fitness",
            "Endurance",
            "Flexibility",
        ],
    )

    level = st.selectbox(
        "Experience level",
        ["Beginner", "Intermediate", "Advanced"],
    )

    environment = st.selectbox(
        "Workout location",
        ["At home", "At the gym"],
    )

    duration = st.selectbox(
        "Session duration",
        [20, 30, 45, 60],
        format_func=lambda minutes: f"{minutes} minutes",
    )

    profile_submitted = st.form_submit_button(
        "Update profile",
        use_container_width=True,
    )

profile = {
    "name": user_name.strip() or "User",
    "age": int(age),
    "weight": float(weight),
    "height_cm": float(height_cm),
    "goal": goal,
    "level": level,
    "environment": environment,
    "duration": int(duration),
}

bmi = calculate_bmi(profile["weight"], profile["height_cm"])
bmi_category = get_bmi_category(bmi)

if profile_submitted:
    st.sidebar.success("Profile updated!")


# ==================================================
# NAVIGATION
# ==================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### Workspace")

page = st.sidebar.radio(
    "Choose a page",
    [
        "My Workout",
        "BMI & Fitness Insights",
        "Fitness Dashboard",
        "Workout History",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("FitPilot · AI Fitness Coaching")
st.sidebar.caption("Build consistency, one session at a time.")


# ==================================================
# REUSABLE UI HELPERS
# ==================================================

def show_hero(eyebrow, title, description):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_history_dataframe(name):
    history = get_workout_history(name)

    if history is None:
        return pd.DataFrame()

    if isinstance(history, pd.DataFrame):
        return history.copy()

    if isinstance(history, list):
        records = [
            dict(row) if not isinstance(row, dict) else row
            for row in history
        ]
        return pd.DataFrame(records)

    try:
        return pd.DataFrame(history)
    except (TypeError, ValueError):
        return pd.DataFrame()


def prepare_history(history_df):
    """Ensure expected numeric columns exist before plotting."""
    df = history_df.copy()

    expected = [
        "duration",
        "calories_estimate",
        "completed_exercises",
        "total_exercises",
    ]

    for column in expected:
        if column not in df.columns:
            df[column] = 0

        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)

    denominator = df["total_exercises"].replace(0, float("nan"))

    df["completion_rate"] = (
        df["completed_exercises"] / denominator * 100
    ).fillna(0)

    return df


# ==================================================
# PAGE 1: MY WORKOUT
# ==================================================

if page == "My Workout":

    show_hero(
        "YOUR TRAINING SPACE",
        f"Let's get stronger, {profile['name']}.",
        "Generate your workout, discover your AI-recommended training "
        "focus, and track every completed exercise.",
    )

    st.markdown("### Your training overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Today's goal", profile["goal"])
    col2.metric("Session length", f"{profile['duration']} min")
    col3.metric("Experience", profile["level"])

    st.markdown("---")
    st.markdown("### 🧠 AI workout recommendation")

    st.markdown(
        '<div class="info-card">'
        '<div class="info-card-title">Random Forest Coach</div>'
        '<div class="info-card-copy">Get a predicted workout focus from '
        'your fitness profile using your saved machine-learning model.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "✨ Get my ML recommendation",
        key="ml_recommendation_button",
    ):
        try:
            result = recommend_workout_focus(profile)

            st.session_state["predicted_focus"] = result["focus"]
            st.session_state["model_confidence"] = result["confidence"]

        except Exception as error:
            st.error(f"Unable to get a recommendation: {error}")

    if st.session_state["predicted_focus"]:
        st.success(
            f"Recommended focus: **{st.session_state['predicted_focus']}**"
        )

        confidence = st.session_state["model_confidence"]

        if confidence is not None:
            st.caption(
                f"Predicted-class probability: {confidence:.1%}. "
                "This is not a measure of workout safety or effectiveness."
            )

    st.markdown("---")
    st.markdown("### 🏋️ Your workout plan")

    if st.button(
        "Generate workout",
        type="primary",
        key="generate_workout_button",
    ):
        try:
            workout = generate_workout(
                goal=profile["goal"],
                level=profile["level"],
                environment=profile["environment"],
                duration=profile["duration"],
            )

            st.session_state["current_workout"] = workout
            st.session_state["saved_workout_key"] = None

        except Exception as error:
            st.error(f"Unable to generate workout: {error}")

    workout = st.session_state["current_workout"]

    if workout is not None:

        st.markdown(f"#### {workout['goal']}")

        a, b, c = st.columns(3)

        a.metric("Total time", f"{workout['duration']} min")
        b.metric("Warm-up", f"{workout['warmup_minutes']} min")
        c.metric("Cool-down", f"{workout['cooldown_minutes']} min")

        st.info(
            f"**Location:** {workout['environment']} · "
            f"**Level:** {workout['level']} · "
            f"**Main workout:** {workout['main_minutes']} min"
        )

        exercises = workout.get("exercises", [])

        if not exercises:
            st.warning("No exercises were generated for this selection.")

        else:
            st.markdown("#### Exercise checklist")

            completed_count = 0
            total_exercises = len(exercises)

            for index, exercise in enumerate(exercises):

                if isinstance(exercise, dict):
                    name = exercise.get("name", f"Exercise {index + 1}")
                    sets = exercise.get("sets", "—")
                    reps = exercise.get("reps", "—")
                    rest = exercise.get("rest", "—")
                else:
                    name = str(exercise)
                    sets = "—"
                    reps = "—"
                    rest = "—"

                completed = st.checkbox(
                    f"{name}  ·  Sets: {sets}  ·  Reps: {reps}  ·  Rest: {rest}",
                    key=f"workout_check_{index}_{name}",
                )

                if completed:
                    completed_count += 1

            progress = completed_count / total_exercises

            st.markdown("#### Session progress")

            st.progress(progress)

            st.write(
                f"**{completed_count} of {total_exercises} exercises complete** "
                f"({progress:.0%})"
            )

            estimated_calories = int(
                profile["weight"] * workout["duration"] * 0.06
            )

            cal_col1, cal_col2 = st.columns(2)

            cal_col1.metric(
                "Estimated energy use",
                f"~{estimated_calories} kcal",
            )

            cal_col2.metric(
                "Completion",
                f"{progress:.0%}",
            )

            st.caption(
                "Calorie values are rough estimates, not measurements."
            )

            if st.button(
                "Save session to history",
                key="save_workout_button",
            ):
                try:
                    save_key = (
                        f"{profile['name']}_{workout['goal']}_"
                        f"{workout['duration']}_{completed_count}_"
                        f"{total_exercises}"
                    )

                    if st.session_state["saved_workout_key"] == save_key:
                        st.warning("This session appears to be saved already.")
                    else:
                        save_workout(
                            user_name=profile["name"],
                            goal=workout["goal"],
                            duration=workout["duration"],
                            completed_exercises=completed_count,
                            total_exercises=total_exercises,
                            calories_estimate=estimated_calories,
                        )

                        st.session_state["saved_workout_key"] = save_key
                        st.success("Your workout was saved!")

                except Exception as error:
                    st.error(f"Unable to save your workout: {error}")

# ---------------- FITNESS AI CHATBOT ----------------

st.markdown("---")
st.subheader("💬 FitPilot AI Fitness Coach")
st.write(
    "Ask questions about workouts, recovery, fitness goals "
    "or healthy habits."
)

# Store chat messages during the current Streamlit session.
if "fitness_chat_messages" not in st.session_state:
    st.session_state.fitness_chat_messages = []

# Use the profile details already collected by your app.
chatbot_profile = {
    "age": age,
    "weight": weight,
    "goal": goal,
    "level": level,
    "environment": environment,
    "duration": duration,
}

# Display the previous messages.
for message in st.session_state.fitness_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show the message input.
user_message = st.chat_input(
    "Ask your fitness coach a question..."
)

if user_message:
    # Save and display the user's message.
    st.session_state.fitness_chat_messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Call the AI model.
    with st.chat_message("assistant"):
        with st.spinner("FitPilot is thinking..."):
            api_key = st.secrets.get("GEMINI_API_KEY", "")

            reply = get_fitness_reply(
                api_key=api_key,
                messages=st.session_state.fitness_chat_messages,
                profile=chatbot_profile,
            )

            st.markdown(reply)

    # Save the answer so it remains visible after reruns.
    st.session_state.fitness_chat_messages.append(
        {"role": "assistant", "content": reply}
    )

if st.button("Clear chatbot conversation"):
    st.session_state.fitness_chat_messages = []
    st.rerun()



# ==================================================
# PAGE 2: BMI AND FITNESS INSIGHTS
# ==================================================

elif page == "BMI & Fitness Insights":

    show_hero(
        "HEALTH AND WELLNESS",
        "Understand your fitness profile.",
        "Review your BMI screening result and get general suggestions "
        "based on your selected goals, experience, and training routine.",
    )

    st.markdown("### Your body metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Height", f"{profile['height_cm']:.0f} cm")
    col2.metric("Weight", f"{profile['weight']:.1f} kg")
    col3.metric("BMI", f"{bmi:.1f}")

    st.markdown("### BMI screening result")

    st.info(f"**{bmi_category}**")

    st.caption(
        "BMI is a screening measure, not a diagnosis. It does not distinguish "
        "muscle from fat and should be interpreted in context."
    )

    with st.expander("View adult BMI reference ranges"):
        bmi_reference = pd.DataFrame({
            "Category": [
                "Below usual range",
                "Usual range",
                "Above usual range",
                "High range",
            ],
            "Adult BMI": [
                "Below 18.5",
                "18.5 to below 25",
                "25 to below 30",
                "30 or above",
            ],
        })

        st.dataframe(
            bmi_reference,
            hide_index=True,
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("### 🎯 Your personal fitness insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div class="info-card">'
            f'<div class="tag">YOUR GOAL</div>'
            f'<div class="info-card-title">{profile["goal"]}</div>'
            f'<div class="info-card-copy">Your selected goal guides the '
            f'general suggestions shown below.</div></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f'<div class="info-card">'
            f'<div class="tag">YOUR ROUTINE</div>'
            f'<div class="info-card-title">{profile["duration"]} minutes</div>'
            f'<div class="info-card-copy">{profile["level"]} · '
            f'{profile["environment"]}</div></div>',
            unsafe_allow_html=True,
        )

    insights = get_fitness_insights(profile, bmi, bmi_category)

    for index, insight in enumerate(insights, start=1):
        with st.container(border=True):
            st.markdown(f"**Insight {index}**")
            st.write(insight)

    st.warning(
        "These suggestions are for general education, not medical advice. "
        "Consult a healthcare professional if you have health concerns or "
        "need an individualized exercise plan."
    )


# ==================================================
# PAGE 3: FITNESS DASHBOARD
# ==================================================

elif page == "Fitness Dashboard":

    show_hero(
        "YOUR PROGRESS",
        "Small steps. Real consistency.",
        "Review your saved workout sessions, total training time, "
        "estimated energy use, and exercise completion.",
    )

    try:
        history_df = load_history_dataframe(profile["name"])
    except Exception as error:
        st.error(f"Unable to load workout history: {error}")
        history_df = pd.DataFrame()

    if history_df.empty:
        st.info(
            "No workout history was found for this name. "
            "Generate and save your first workout to populate the dashboard."
        )

    else:
        history_df = prepare_history(history_df)

        sessions = len(history_df)
        total_minutes = int(history_df["duration"].sum())
        total_calories = int(history_df["calories_estimate"].sum())
        average_completion = history_df["completion_rate"].mean()

        st.markdown("### At a glance")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        col1.metric("Sessions completed", sessions)
        col2.metric("Total training", f"{total_minutes} min")
        col3.metric("Estimated calories", f"{total_calories:,} kcal")
        col4.metric("Average completion", f"{average_completion:.1f}%")

        st.markdown("---")
        st.markdown("### 📈 Training trends")

        chart_left, chart_right = st.columns(2)

        with chart_left:
            st.markdown("#### Workout duration")

            duration_chart = history_df[["duration"]].reset_index(drop=True)
            duration_chart.index = duration_chart.index + 1
            duration_chart.index.name = "Session"

            st.line_chart(duration_chart)

        with chart_right:
            st.markdown("#### Estimated calories")

            calories_chart = history_df[
                ["calories_estimate"]
            ].reset_index(drop=True)

            calories_chart.index = calories_chart.index + 1
            calories_chart.index.name = "Session"

            st.bar_chart(calories_chart)

        st.markdown("#### Exercise completion")

        completion_chart = pd.DataFrame({
            "Completion (%)": history_df["completion_rate"].values
        })

        completion_chart.index = completion_chart.index + 1
        completion_chart.index.name = "Session"

        st.line_chart(completion_chart)


# ==================================================
# PAGE 4: WORKOUT HISTORY
# ==================================================

elif page == "Workout History":

    show_hero(
        "YOUR TRAINING LOG",
        "Every session counts.",
        "Review your saved workouts and export your records whenever you need them.",
    )

    try:
        history_df = load_history_dataframe(profile["name"])
    except Exception as error:
        st.error(f"Unable to load workout history: {error}")
        history_df = pd.DataFrame()

    if history_df.empty:
        st.info(
            "No saved workouts were found for this name. "
            "Complete and save a workout to see it here."
        )

    else:
        st.markdown("### Saved sessions")

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download workout history (CSV)",
            data=csv_data,
            file_name="fitness_workout_history.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer-note">
        FitPilot · AI Fitness Coaching · Built with Streamlit<br>
        Fitness suggestions and BMI are educational; model recommendations
        are a prototype and are not a substitute for professional advice.
    </div>
    """,
    unsafe_allow_html=True,
)
