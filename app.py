import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Dark Glassmorphism Dashboard (No scroll)
st.markdown("""
<style>
    /* Hide Streamlit default footer */
    footer {visibility: hidden;}

    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(46, 52, 64, 1), transparent 50%),
                    radial-gradient(circle at 85% 30%, rgba(34, 53, 40, 1), transparent 50%),
                    radial-gradient(circle at 50% 80%, rgba(60, 36, 21, 1), transparent 50%);
        background-color: #12141c;
        /* Try to prevent scroll */
        overflow-y: hidden !important; 
    }
    
    /* Main container styling (fit to screen) */
    .block-container {
        background: rgba(30, 32, 40, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 2.5rem 3rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
        max-width: 90% !important;
        width: 100% !important;
        
        /* Perfect Centering */
        position: absolute !important;
        top: 53% !important; /* 53% accounts for the top navbar space */
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }

    /* Headings and text */
    h1, h2, h3, p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    h1 {
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px !important;
        padding-bottom: 5px !important;
        background: -webkit-linear-gradient(#f9a826, #f37335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Input widgets (Dark frosted glass) */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: rgba(20, 22, 30, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
        color: white !important;
        height: 38px !important;
        min-height: 38px !important;
    }
    
    input, select {
        color: white !important;
        font-size: 14px !important;
    }

    /* Button styling */
    .stButton>button {
        background: rgba(249, 168, 38, 0.85);
        color: #12141c !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        height: 100%;
    }
    
    .stButton>button:hover {
        background: rgba(249, 168, 38, 1);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(249, 168, 38, 0.4);
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

# Layout: 4 columns for inputs
col1, col2, col3, col4 = st.columns(4)

with col1:
    study_hours = st.number_input("Study Hours (daily)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    internal_exam = st.number_input("Internal Exam", min_value=0.0, max_value=100.0, value=78.0, step=1.0)

with col2:
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    sleep_hours = st.number_input("Sleep (nightly)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)

with col3:
    previous_marks = st.number_input("Previous Marks", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
    internet_usage = st.number_input("Internet (hours)", min_value=0.0, max_value=24.0, value=3.0, step=0.5)

with col4:
    assignment_score = st.number_input("Assignment Score", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
    extracurricular = st.selectbox("Extracurricular", ["Yes", "No"])

st.write("") # small spacing

@st.dialog("Prediction Results")
def show_result(prediction, status, color):
    st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 16px; color: #a0a0a0; margin-bottom: 5px;">Predicted Score</p>
            <h1 style="color: #f9a826; font-size: 50px; margin-top: 0; margin-bottom: 10px;">{prediction:.2f}%</h1>
            <h3 style="color: {color}; font-size: 24px; margin-top: 0;">{status}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Awesome!", use_container_width=True):
        st.rerun()

st.write("") # small spacing

# Layout: Button centered
res_col1, res_col2, res_col3 = st.columns([1, 2, 1])

with res_col2:
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
    
    prediction = max(0, min(100, model.predict(input_data)[0]))
    
    if prediction >= 80:
        status = "🌟 Excellent Performance"
        color = "#4CAF50"
    elif prediction >= 60:
        status = "👍 Good Performance"
        color = "#2196F3"
    elif prediction >= 40:
        status = "⚠️ Average Performance"
        color = "#FF9800"
    else:
        status = "❗ Needs Improvement"
        color = "#F44336"
        
    show_result(prediction, status, color)