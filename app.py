import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("student_performance_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# Title
st.title("🎓 Student Performance Predictor")
st.write(
    "Enter the student's academic and lifestyle details "
    "to predict the final examination marks."
)

st.divider()

# Input fields
study_hours = st.number_input(
    "📚 Study Hours",
    min_value=0.0,
    max_value=24.0,
    value=7.0,
    step=0.5
)

attendance = st.number_input(
    "📅 Attendance (%)",
    min_value=0.0,
    max_value=100.0,
    value=85.0,
    step=1.0
)

previous_marks = st.number_input(
    "📊 Previous Marks",
    min_value=0.0,
    max_value=100.0,
    value=75.0,
    step=1.0
)

assignment_score = st.number_input(
    "📝 Assignment Score",
    min_value=0.0,
    max_value=100.0,
    value=80.0,
    step=1.0
)

internal_exam = st.number_input(
    "📖 Internal Exam Score",
    min_value=0.0,
    max_value=100.0,
    value=78.0,
    step=1.0
)

sleep_hours = st.number_input(
    "😴 Sleep Hours",
    min_value=0.0,
    max_value=24.0,
    value=7.0,
    step=0.5
)

extracurricular = st.selectbox(
    "🏆 Extracurricular Activities",
    ["Yes", "No"]
)

internet_usage = st.number_input(
    "🌐 Internet Usage Hours",
    min_value=0.0,
    max_value=24.0,
    value=3.0,
    step=0.5
)

st.divider()

# Prediction button
if st.button("🎯 Predict Final Marks", use_container_width=True):

    # Convert Yes/No to 1/0
    extracurricular_value = 1 if extracurricular == "Yes" else 0

    # Create input DataFrame
    input_data = pd.DataFrame({
        "Study_Hours": [study_hours],
        "Attendance_Percent": [attendance],
        "Previous_Marks": [previous_marks],
        "Assignment_Score": [assignment_score],
        "Internal_Exam_Score": [internal_exam],
        "Sleep_Hours": [sleep_hours],
        "Extracurricular_Activities": [extracurricular_value],
        "Internet_Usage_Hours": [internet_usage]
    })

    # Prediction
    prediction = model.predict(input_data)[0]

    # Keep prediction within marks range
    prediction = max(0, min(100, prediction))

    st.success("Prediction completed!")

    st.metric(
        label="🎯 Predicted Final Exam Marks",
        value=f"{prediction:.2f}"
    )

    # Performance category
    if prediction >= 80:
        st.success("🌟 Excellent Performance")
    elif prediction >= 60:
        st.info("👍 Good Performance")
    elif prediction >= 40:
        st.warning("⚠️ Average Performance")
    else:
        st.error("❗ Needs Improvement")