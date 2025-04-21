import numpy as np
import pandas as pd
import streamlit as st
import requests
import random

st.set_page_config(page_title="Fitness Companion", page_icon="💪", layout="wide")

# Manual Calories Calculator from Code 1
def calories_calculator(weight, height, age, gender, heart_rate, minutes, workout_type):
    # BMI-based calorie calculation
    workout_factors = {
        "None": 0,
        "Yoga": 1,
        "Dancing": 2,
        "Cardio": 3,
        "HIIT": 4
    }
    workout_factor = workout_factors.get(workout_type, 0)
    calories_per_min = (heart_rate * weight * 0.0007) + (age * 0.01) + workout_factor
    calories_total = calories_per_min * minutes
    bmi = weight / ((height / 100) ** 2)
    return round(calories_total, 2), calories_per_min, bmi

# Generate workout plan using the calorie calculator
def generate_workout_plan(age, gender, height, weight, workout_duration, workout_days, heart_rate, workout_type):
    calories_burned, _, _ = calories_calculator(weight, height, age, gender, heart_rate, workout_duration, workout_type)

    strength_score = random.uniform(0.3, 0.7)
    endurance_score = random.uniform(0.3, 0.7)
    flexibility_score = random.uniform(0.3, 0.7)

    workout_types = ["Cycling", "Running", "Swimming", "Weight Training"]
    recommended_workout = random.choice(workout_types)

    def get_exercise_details(muscle_group):
        try:
            response = requests.get(
                f"https://v2.exercisedb.io/api/exercises/target/{muscle_group}?limit=10"
            )
            exercises = response.json()
            return random.choice(exercises) if exercises else None
        except Exception as e:
            st.error(f"Error fetching exercises: {e}")
            return None

    workout_plan = []
    muscle_groups = ["hamstrings", "quadriceps", "chest", "back", "shoulders"]
    for day in range(1, workout_days + 1):
        exercise = get_exercise_details(random.choice(muscle_groups))
        if exercise:
            workout_plan.append({
                "day": day,
                "name": exercise.get("name", "Unknown Exercise"),
                "muscle_group": f"({exercise.get('target', 'unknown')})",
                "body_part": exercise.get("bodyPart", "Unknown"),
                "equipment": exercise.get("equipment", "None"),
                "image_url": exercise.get("gifUrl", "")
            })

    return {
        "strength_score": strength_score,
        "endurance_score": endurance_score,
        "flexibility_score": flexibility_score,
        "recommended_workout": recommended_workout,
        "workout_plan": workout_plan,
        "calories_burned": calories_burned
    }

# Header
st.markdown(
    f'<img src="https://images-platform.99static.com/8QVhsq0xUI9KAGH6WZXUmnWohwI=/0x0:1574x1574/500x500/top/smart/99designs-contests-attachments/97/97489/attachment_97489210" width="150" style="display: block; margin: 0 auto;">',
    unsafe_allow_html=True
)

st.title("Fitness Companion")

# Tool selection
app_selection = st.radio("Choose a Fitness Tool", 
    ["Calories Calculator", "Recommended Workout", "Workout Plan"]
)

# Sidebar user inputs
with st.sidebar:
    st.header("Personal Details")
    age = st.number_input("Age", min_value=5, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
    height = st.number_input("Height (cm)", min_value=50, max_value=300, value=170)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
    heart_rate = st.number_input("Heart Rate", min_value=60, max_value=200, value=120)
    workout_duration = st.number_input("Workout Duration (mins)", min_value=10, max_value=180, value=45)
    workout_days = st.number_input("Workout Days", min_value=1, max_value=7, value=3)
    workout_type = st.selectbox("Workout Type", ["None", "Yoga", "Dancing", "Cardio", "HIIT"])

# Calories calculator section
if app_selection == "Calories Calculator":
    st.header("Calories Burned Calculator")
    if st.button("Calculate Calories"):
        calories, per_min, bmi = calories_calculator(weight, height, age, gender, heart_rate, workout_duration, workout_type)
        st.metric("Calories Burned", f"{calories:.0f} cal")
        st.metric("Calories per Minute", f"{per_min:.2f} kcal/min")
        st.metric("BMI", f"{bmi:.1f}")

# Recommended workout section
if app_selection == "Recommended Workout":
    st.header("Recommended Workout")
    if st.button("Get Recommended Workout"):
        result = generate_workout_plan(age, gender, height, weight, workout_duration, workout_days, heart_rate, workout_type)
        col1, col2, col3 = st.columns(3)
        col1.metric("Strength", f"{result['strength_score']:.2f}")
        col2.metric("Endurance", f"{result['endurance_score']:.2f}")
        col3.metric("Flexibility", f"{result['flexibility_score']:.2f}")
        st.markdown(f"✅ **Recommended Workout Type:** {result['recommended_workout']}")

# Workout plan section
if app_selection == "Workout Plan":
    st.header("Personalized Workout Plan")
    if st.button("Generate Workout Plan"):
        result = generate_workout_plan(age, gender, height, weight, workout_duration, workout_days, heart_rate, workout_type)
        st.metric("Calories Burned", f"{result['calories_burned']:.0f} cal")
        st.markdown(f"✅ **Recommended Workout Type:** {result['recommended_workout']}")
        st.markdown("### 💪 Workout Plan")
        for workout in result['workout_plan']:
            st.markdown(f"**Day {workout['day']}:** {workout['name']} {workout['muscle_group']}")
            st.markdown(f"• Body Part: {workout['body_part']}")
            st.markdown(f"• Equipment: {workout['equipment']}")
            if workout['image_url']:
                st.image(workout['image_url'], width=200)



if __name__ == "__main__":
    pass
