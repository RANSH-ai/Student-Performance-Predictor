import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for Dark Glassmorphism Dashboard
st.markdown("""
<style>
    /* Background Gradient for the app (Dark mesh gradient) */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(46, 52, 64, 1), transparent 50%),
                    radial-gradient(circle at 85% 30%, rgba(34, 53, 40, 1), transparent 50%),
                    radial-gradient(circle at 50% 80%, rgba(60, 36, 21, 1), transparent 50%);
        background-color: #12141c;
        background-attachment: fixed;
    }
    
    /* Main block container (Glass panel) */
    .block-container {
        background: rgba(30, 32, 40, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 2rem 3rem !important;
        margin-top: 3rem !important;
        margin-bottom: 3rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
    }

    /* Headings and text */
    h1, h2, h3, p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    h1 {
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        background: -webkit-linear-gradient(#f9a826, #f37335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Input widgets (Dark frosted glass) */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: rgba(20, 22, 30, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        color: white !important;
    }
    
    input, select {
        color: white !important;
    }

    /* Button styling (Orange accent) */
    .stButton>button {
        background: rgba(249, 168, 38, 0.85);
        color: #12141c !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    
    .stButton>button:hover {
        background: rgba(249, 168, 38, 1);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(249, 168, 38, 0.4);
    }
    
    /* Dividers */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #f9a826 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load trained model
@st.cache_resource
def load_model():
    return joblib.load("student_performance_model.pkl")

model = load_model()

# Title
st.markdown("<h1>🎓 Student Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0a0 !important; font-size: 1.1rem; margin-bottom: 30px;'>Enter the student's details to predict their final examination marks.</p>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📚 Academic Details")
    study_hours = st.number_input("Study Hours (daily)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    previous_marks = st.number_input("Previous Marks", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
    assignment_score = st.number_input("Assignment Score", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
    internal_exam = st.number_input("Internal Exam Score", min_value=0.0, max_value=100.0, value=78.0, step=1.0)

with col2:
    st.subheader("🌱 Lifestyle Details")
    sleep_hours = st.number_input("Sleep Hours (nightly)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    internet_usage = st.number_input("Internet Usage Hours", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
    st.markdown("<br>", unsafe_allow_html=True)
    extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"])

st.divider()

# Prediction button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_btn = st.button("🎯 Predict Final Marks", use_container_width=True)

if predict_btn:
    extracurricular_value = 1 if extracurricular == "Yes" else 0
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
    
    with st.spinner('Analyzing...'):
        prediction = max(0, min(100, model.predict(input_data)[0]))
    
    st.success("Analysis Complete!")
    
    res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
    with res_col2:
        st.metric(label="Predicted Final Exam Marks", value=f"{prediction:.2f}%")
        
        if prediction >= 80:
            st.info("🌟 Excellent Performance")
        elif prediction >= 60:
            st.info("👍 Good Performance")
        elif prediction >= 40:
            st.warning("⚠️ Average Performance")
        else:
            st.error("❗ Needs Improvement")