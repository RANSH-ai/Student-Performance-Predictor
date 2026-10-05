import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    /* Add some padding at the top */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Style the main title */
    .main-title {
        color: #1E3A8A;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        margin-bottom: 0;
    }
    
    /* Style the subtitle */
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #4B5563;
        margin-top: 10px;
        margin-bottom: 30px;
    }

    /* Style the predict button */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: scale(1.02);
    }
    
    /* Headers for sections */
    .section-header {
        color: #374151;
        font-weight: 600;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load trained model efficiently
@st.cache_resource
def load_model():
    return joblib.load("student_performance_model.pkl")

model = load_model()

# Title
st.markdown("<h1 class='main-title'>🎓 Student Performance Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Enter the student's academic and lifestyle details to predict the final examination marks.</p>", unsafe_allow_html=True)

st.divider()

# Create columns for better layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h3 class='section-header'>📚 Academic Details</h3>", unsafe_allow_html=True)
    
    study_hours = st.slider(
        "Study Hours (per day)", 
        min_value=0.0, max_value=24.0, value=7.0, step=0.5, 
        help="How many hours does the student study daily?"
    )
    
    attendance = st.slider(
        "Attendance (%)", 
        min_value=0.0, max_value=100.0, value=85.0, step=1.0, 
        help="Student's overall attendance percentage."
    )
    
    previous_marks = st.number_input(
        "📊 Previous Marks", 
        min_value=0.0, max_value=100.0, value=75.0, step=1.0
    )
    
    assignment_score = st.number_input(
        "📝 Assignment Score", 
        min_value=0.0, max_value=100.0, value=80.0, step=1.0
    )
    
    internal_exam = st.number_input(
        "📖 Internal Exam Score", 
        min_value=0.0, max_value=100.0, value=78.0, step=1.0
    )

with col2:
    st.markdown("<h3 class='section-header'>🌱 Lifestyle Details</h3>", unsafe_allow_html=True)
    
    sleep_hours = st.slider(
        "Sleep Hours (per night)", 
        min_value=0.0, max_value=24.0, value=7.0, step=0.5, 
        help="Average hours of sleep per night."
    )
    
    internet_usage = st.slider(
        "Internet Usage Hours", 
        min_value=0.0, max_value=24.0, value=3.0, step=0.5, 
        help="Daily hours spent on the internet."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    extracurricular = st.radio(
        "🏆 Extracurricular Activities", 
        ["Yes", "No"], 
        horizontal=True, 
        help="Does the student participate in extracurricular activities?"
    )

st.divider()

# Prediction button centered
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_btn = st.button("🎯 Predict Final Marks", use_container_width=True)

if predict_btn:
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

    with st.spinner('Analyzing student data...'):
        # Prediction
        prediction = model.predict(input_data)[0]
        # Keep prediction within marks range
        prediction = max(0, min(100, prediction))

    # Display result in a nice metric box
    res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
    with res_col2:
        st.success("✨ Prediction completed successfully!")
        
        delta_val = prediction - previous_marks
        delta_color = "normal" if delta_val >= 0 else "inverse"
        
        st.metric(
            label="🎯 Predicted Final Exam Marks", 
            value=f"{prediction:.2f}%", 
            delta=f"{delta_val:.2f}% from previous marks",
            delta_color=delta_color
        )

        # Performance category with progress bar
        st.progress(int(prediction) / 100)
        
        if prediction >= 80:
            st.success("🌟 **Excellent Performance!** Keep it up!")
        elif prediction >= 60:
            st.info("👍 **Good Performance.** Room for a little improvement.")
        elif prediction >= 40:
            st.warning("⚠️ **Average Performance.** Needs more focus and hard work.")
        else:
            st.error("❗ **Needs Improvement.** Critical attention required.")