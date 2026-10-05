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

# Custom CSS for Glassmorphism
st.markdown("""
<style>
    /* Gradient background for the whole page */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        background-attachment: fixed;
    }
    
    /* Glass card effect for the main container */
    .block-container {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 3rem !important;
        margin-top: 3rem !important;
        margin-bottom: 3rem !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }

    /* Text color for contrast */
    h1, h2, h3, p, label, .stMarkdown {
        color: #2d3748 !important;
    }
    
    /* Input fields glass styling */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px;
    }
    
    input, select {
        color: #2d3748 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: rgba(255, 255, 255, 0.5);
        color: #2d3748;
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.8);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Success Alert Styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(5px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

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