import streamlit as st
import requests
import random

st.set_page_config(page_title="Workout Generator", page_icon="💪")

def generate_workout_plan(age, gender, height, weight, workout_duration, workout_days):
    # TODO: Implement actual scoring logic
    strength_score = random.uniform(0.3, 0.7)
    endurance_score = random.uniform(0.3, 0.7)
    flexibility_score = random.uniform(0.3, 0.7)

    # Simulated workout type selection
    workout_types = ["Cycling", "Running", "Swimming", "Weight Training"]
    recommended_workout = random.choice(workout_types)

    # Fetch exercises from ExerciseDB API
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

    # Generate workout plan
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
        "workout_plan": workout_plan
    }

st.title("Personalized Workout Generator")

# Sidebar inputs
with st.sidebar:
    st.header("Personal Details")
    age = st.number_input("Age", min_value=5, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=50, max_value=300, value=170)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
    workout_duration = st.number_input("Workout Duration (mins)", min_value=10, max_value=180, value=45)
    workout_days = st.number_input("Workout Days", min_value=1, max_value=7, value=3)

    generate_button = st.button("Generate Workout")

# Main area for results
if generate_button:
    with st.spinner("Generating your personalized workout..."):
        result = generate_workout_plan(age, gender, height, weight, workout_duration, workout_days)

        # Display weighted averages
        st.markdown("### Fitness Scores")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Strength", f"{result['strength_score']:.2f}")
        with col2:
            st.metric("Endurance", f"{result['endurance_score']:.2f}")
        with col3:
            st.metric("Flexibility", f"{result['flexibility_score']:.2f}")

        # Recommended Workout Type
        st.markdown(f"✅ **Recommended Workout Type:** {result['recommended_workout']}")

        # Workout Plan
        st.markdown("### 🔥 Workout Plan")
        for workout in result['workout_plan']:
            st.markdown(f"**Day {workout['day']}:** {workout['name']} {workout['muscle_group']}")
            st.markdown(f"• Body Part: {workout['body_part']}")
            st.markdown(f"• Equipment: {workout['equipment']}")
            if workout['image_url']:
                st.image(workout['image_url'], width=200)

if __name__ == "__main__":
    pass