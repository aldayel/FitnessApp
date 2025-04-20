import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="Fitness Recommendation Dashboard", layout="wide")

# --- Sidebar: Data Upload & Page Selection ---
st.sidebar.header("📂 Load Data & Navigate")
# CSV uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload cleaned_workout_data.csv", type=["csv"]
)
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.error("Please upload 'cleaned_workout_data.csv' to proceed.")
    st.stop()

# --- Initialize session state for profile ---
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False
if "age" not in st.session_state:
    st.session_state.age = 30
if "height_cm" not in st.session_state:
    st.session_state.height_cm = 170
if "weight_kg" not in st.session_state:
    st.session_state.weight_kg = 70

# --- Sidebar: Page Selection ---
def get_pages():
    pages = ["Profile"]
    if st.session_state.profile_complete:
        pages += [
            "Goals & Mood",
            "🔢 Calculators",
            "🔥 Estimate Calories",
            "💡 Workout Recommender",
            "📅 Weight‑Loss Planner",
            "😊 Mood Booster",
        ]
    return pages

page = st.sidebar.selectbox("Page", get_pages())

# --- Page 1: Profile ---
if page == "Profile":
    st.header("👤 Profile Setup")
    age = st.slider("Age", min_value=5, max_value=120, value=st.session_state.age)
    height_cm = st.slider("Height (cm)", min_value=50, max_value=300, value=st.session_state.height_cm)
    weight_kg = st.slider("Weight (kg)", min_value=20, max_value=300, value=st.session_state.weight_kg)
    if st.button("Continue"):
        st.session_state.age = age
        st.session_state.height_cm = height_cm
        st.session_state.weight_kg = weight_kg
        st.session_state.profile_complete = True
        st.experimental_rerun()

# Retrieve stored profile values
age = st.session_state.age
height_cm = st.session_state.height_cm
weight_kg = st.session_state.weight_kg

# --- Shared inputs default definitions ---
if st.session_state.profile_complete:
    if "gender" not in st.session_state:
        st.session_state.gender = "Prefer not to say"
    if "fitness_goal" not in st.session_state:
        st.session_state.fitness_goal = "Maintain weight"
    if "mood" not in st.session_state:
        st.session_state.mood = "Neutral"
    if "target_cal" not in st.session_state:
        st.session_state.target_cal = 0
    if "desired_weight" not in st.session_state:
        st.session_state.desired_weight = 0.0

# --- Page 2: Goals & Mood ---
if page == "Goals & Mood":
    st.header("🎯 Goals & Mood")
    st.session_state.gender = st.selectbox(
        "Gender", ["Female", "Male", "Prefer not to say"],
        index=["Female","Male","Prefer not to say"].index(st.session_state.gender)
    )
    st.session_state.fitness_goal = st.selectbox(
        "Fitness Goal", ["Lose weight", "Maintain weight", "Gain muscle"],
        index=["Lose weight","Maintain weight","Gain muscle"].index(st.session_state.fitness_goal)
    )
    st.session_state.mood = st.selectbox(
        "Current Mood", ["Stressed", "Energetic", "Tired", "Neutral"],
        index=["Stressed","Energetic","Tired","Neutral"].index(st.session_state.mood)
    )
    st.session_state.target_cal = st.number_input(
        "Target Calories to Burn (optional)", min_value=0, value=st.session_state.target_cal
    )
    st.session_state.desired_weight = st.number_input(
        "Desired Weight Change (kg) (optional)", value=st.session_state.desired_weight
    )

# --- Page 3: Calculators ---
if page == "🔢 Calculators":
    st.header("🔢 Health Calculators")
    bmi = weight_kg / ((height_cm / 100) ** 2)
    st.metric("BMI", f"{bmi:.1f}")
    if st.session_state.gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif st.session_state.gender == "Female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    st.metric("BMR (kcal/day)", f"{bmr:.0f}")
    max_hr = 220 - age
    zone_low, zone_high = int(0.5 * max_hr), int(0.85 * max_hr)
    st.write(f"**Max HR:** {max_hr} bpm")
    st.write(f"**Target Zone (50-85%):** {zone_low}-{zone_high} bpm")

# --- Page 4: Estimate Calories ---
if page == "🔥 Estimate Calories":
    st.header("🔥 Estimate Calories Burned")
    exercise = st.selectbox("Select Exercise", df['activityType'].unique())
    duration = st.slider("Duration (minutes)", 10, 180, 30)
    avg_cal_pm = df.loc[df['activityType'] == exercise, 'avg_cal_per_min'].iloc[0]
    est_cal = avg_cal_pm * duration
    c1, c2 = st.columns(2)
    c1.metric("Exercise", exercise)
    c2.metric("Est. Calories", f"{est_cal:.0f}")

# --- Page 5: Workout Recommender ---
if page == "💡 Workout Recommender":
    st.header("💡 Workout Recommendations")
    recs = []
    if st.session_state.fitness_goal == 'Lose weight':
        recs = [('Running', 30), ('Cycling', 30), ('HIIT', 20)]
    elif st.session_state.fitness_goal == 'Maintain weight':
        recs = [('Walking', 30), ('Strength Training', 30), ('Yoga', 30)]
    else:
        recs = [('Weight Lifting', 45), ('Resistance Bands', 30), ('Protein Workout', 30)]
    for ex, dur in recs:
        st.write(f"- {ex}: {dur} min")
    if st.session_state.target_cal > 0:
        first_ex = recs[0][0]
        avg_pm = df.loc[df['activityType'] == first_ex, 'avg_cal_per_min'].iloc[0]
        needed = st.session_state.target_cal / avg_pm
        st.info(f"To burn {st.session_state.target_cal} kcal with {first_ex}, do ~{needed:.0f} min.")

# --- Page 6: Weight-Loss Planner ---
if page == "📅 Weight‑Loss Planner":
    st.header("📅 Weight‑Loss Planner")
    if st.session_state.desired_weight > 0:
        total_deficit = st.session_state.desired_weight * 7700
        sessions = 5
        per_session = total_deficit / sessions
        st.write(f"To lose {st.session_state.desired_weight} kg → {total_deficit:.0f} kcal deficit")
        for i in range(1, sessions + 1):
            st.write(f"- Session {i}: ~{per_session:.0f} kcal")
    else:
        st.write('Enter desired weight change to see plan.')

# --- Page 7: Mood Booster ---
if page == "😊 Mood Booster":
    st.header("😊 Mood Booster")
    mood_map = {
        'Stressed': ('Yoga', 'A calming 20-min yoga session'),
        'Energetic': ('HIIT', 'A quick energizing HIIT'),
        'Tired': ('Walking', 'A 30-min brisk walk to revive'),
        'Neutral': ('Stretching', 'Try a full-body stretch routine')
    }
    ex, msg = mood_map.get(st.session_state.mood, ('', ''))
    if msg:
        st.subheader(msg)

# --- Footer ---
st.markdown('---')
st.write('Built with ❤️ and Streamlit')