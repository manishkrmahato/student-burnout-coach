import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Student Burnout Coach",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS (Premium UI Styling)
# -------------------------------------------------

st.markdown("""
<style>

/* ---------- GLOBAL TEXT COLORS ---------- */

.main-title{
font-size:40px;
font-weight:700;
color: var(--text-color);
}

.sub-title{
font-size:18px;
color: var(--text-color);
opacity:0.8;
}

/* ---------- CARDS ---------- */

.card{
background-color: var(--secondary-background-color);
padding:25px;
border-radius:14px;
box-shadow:0px 6px 20px rgba(0,0,0,0.08);
color: var(--text-color);
transition:0.3s;
}

.card:hover{
transform: translateY(-4px);
box-shadow:0px 10px 25px rgba(0,0,0,0.15);
}

/* ---------- METRIC CARD ---------- */

.metric-card{
background-color: var(--secondary-background-color);
padding:18px;
border-radius:12px;
text-align:center;
color: var(--text-color);
}

/* ---------- FOOTER ---------- */

.footer{
text-align:center;
padding:25px;
font-size:14px;
color: var(--text-color);
opacity:0.6;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def calculate_burnout_score(data):

    score = 0

    score += data["stress"] * 2.5
    score += data["exam_pressure"] * 2.0
    score += data["assignment_load"] * 1.8
    score += data["screen_time"] * 1.5

    score -= data["sleep"] * 1.7
    score -= data["physical_activity"] * 1.5
    score -= data["breaks"] * 1.2

    score = max(0, score)

    return score


def classify_risk(score):

    if score < 15:
        return "Low"
    elif score < 25:
        return "Moderate"
    else:
        return "High"


def generate_study_plan(data, risk):

    study_hours = data["study_hours"]
    stress = data["stress"]

    plan = []

    if risk == "High":

        plan.append("Light Study Session (1 hr)")
        plan.append("Break (30 min)")
        plan.append("Second Study Session (1 hr)")
        plan.append("Exercise (30 min)")
        plan.append("Relaxation / Meditation")
        plan.append("Sleep before 11 PM")

    elif risk == "Moderate":

        plan.append(f"Focused Study Session ({study_hours} hrs)")
        plan.append("Break (20 min)")
        plan.append("Revision (1 hr)")
        plan.append("Exercise (20 min)")
        plan.append("Sleep 7–8 hours")

    else:

        plan.append(f"Deep Study Session ({study_hours} hrs)")
        plan.append("Short Break")
        plan.append("Second Study Block")
        plan.append("Revision Session")
        plan.append("Exercise / Walk")
        plan.append("Maintain consistent sleep schedule")

    if stress > 7:
        plan.append("Add relaxation session due to high stress")

    return plan


def generate_lifestyle_tips(data):

    tips = []

    if data["sleep"] < 6:
        tips.append("Improve sleep to at least 7–8 hours")

    if data["screen_time"] > 6:
        tips.append("Reduce screen time before sleep")

    if data["stress"] > 7:
        tips.append("Practice breathing exercises or meditation")

    if data["physical_activity"] < 3:
        tips.append("Add 20–30 minutes of daily exercise")

    if data["water"] < 5:
        tips.append("Increase daily water intake")

    if data["social"] < 3:
        tips.append("Spend more time interacting with friends or family")

    if len(tips) == 0:
        tips.append("Your lifestyle looks balanced. Maintain your routine!")

    return tips


# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Student Input",
        "Burnout Analysis",
        "Lifestyle Insights",
        "Smart Study Plan",
        "Wellness Suggestions",
        "Final Report"
    ]
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.score = None
    st.session_state.risk = None

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if page == "Dashboard":

    st.markdown('<div class="main-title">AI-Powered Student Burnout Prevention & Smart Study Coach</div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">An intelligent platform to predict burnout, analyze lifestyle habits, and generate smart study strategies for students.</div>', unsafe_allow_html=True)

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="card">🧠 <b>Burnout Risk Prediction</b><br>Identify burnout risk using behavioral patterns.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">📊 Lifestyle Analysis<br>Understand habits affecting productivity.</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📚 Smart Study Plan<br>Get AI-generated personalized study schedules.</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">🌿 Wellness Suggestions<br>Improve sleep, focus, and mental balance.</div>', unsafe_allow_html=True)

    st.write("")
    st.write("Use the sidebar to begin your burnout analysis.")

# -------------------------------------------------
# STUDENT INPUT
# -------------------------------------------------

elif page == "Student Input":

    st.header("Student Lifestyle & Study Data")

    name = st.text_input("Student Name")

    age = st.slider("Age", 16, 30, 20)

    academic_level = st.selectbox("Academic Level", ["High School", "Undergraduate", "Postgraduate"])

    study_hours = st.slider("Study Hours Per Day", 0, 12, 4)

    sleep = st.slider("Sleep Hours Per Day", 0, 10, 6)

    stress = st.slider("Stress Level", 1, 10, 5)

    screen_time = st.slider("Screen Time (hours)", 0, 12, 5)

    physical_activity = st.slider("Physical Activity Level", 0, 10, 3)

    breaks = st.slider("Breaks During Study", 0, 10, 3)

    assignment_load = st.slider("Assignment Load", 1, 10, 5)

    exam_pressure = st.slider("Exam Pressure", 1, 10, 5)

    mood = st.slider("Mood Level", 1, 10, 6)

    motivation = st.slider("Motivation Level", 1, 10, 6)

    social = st.slider("Social Interaction", 1, 10, 5)

    water = st.slider("Water Intake (glasses/day)", 1, 10, 4)

    if st.button("Save Data"):

        data = {
            "name": name,
            "sleep": sleep,
            "stress": stress,
            "screen_time": screen_time,
            "physical_activity": physical_activity,
            "breaks": breaks,
            "assignment_load": assignment_load,
            "exam_pressure": exam_pressure,
            "water": water,
            "social": social,
            "study_hours": study_hours
        }

        score = calculate_burnout_score(data)
        risk = classify_risk(score)

        st.session_state.data = data
        st.session_state.score = score
        st.session_state.risk = risk

        st.success("Student data saved successfully.")

# -------------------------------------------------
# BURNOUT ANALYSIS
# -------------------------------------------------

elif page == "Burnout Analysis":

    st.header("Burnout Risk Analysis")

    if st.session_state.score is None:
        st.warning("Please enter student data first.")
    else:

        score = st.session_state.score
        risk = st.session_state.risk

        st.metric("Burnout Score", round(score, 2))
        st.metric("Risk Level", risk)

        st.progress(min(score / 40, 1.0))

# -------------------------------------------------
# LIFESTYLE INSIGHTS
# -------------------------------------------------

elif page == "Lifestyle Insights":

    st.header("Lifestyle Behavior Analysis")

    if st.session_state.data is None:
        st.warning("Enter student data first.")

    else:

        data = st.session_state.data

        df = pd.DataFrame({
            "Factor": [
                "Stress",
                "Screen Time",
                "Sleep Deficit",
                "Low Exercise"
            ],
            "Score": [
                data["stress"],
                data["screen_time"],
                10 - data["sleep"],
                10 - data["physical_activity"]
            ]
        })

        fig = px.bar(df, x="Factor", y="Score")

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# STUDY PLAN
# -------------------------------------------------

elif page == "Smart Study Plan":

    st.header("Personalized Smart Study Plan")

    if st.session_state.risk is None:
        st.warning("Enter student data first.")

    else:

        risk = st.session_state.risk
        data = st.session_state.data

        plan = generate_study_plan(data, risk)

        for p in plan:
            st.write("•", p)

# -------------------------------------------------
# WELLNESS
# -------------------------------------------------

elif page == "Wellness Suggestions":

    st.header("Lifestyle Improvement Suggestions")

    if st.session_state.data is None:
        st.warning("Enter student data first.")

    else:

        tips = generate_lifestyle_tips(st.session_state.data)

        for t in tips:
            st.write("•", t)

# -------------------------------------------------
# FINAL REPORT
# -------------------------------------------------

elif page == "Final Report":

    st.header("Final Student Burnout Summary")

    if st.session_state.data is None:
        st.warning("Enter student data first.")

    else:

        report = f"""
Student Burnout Report

Burnout Score: {round(st.session_state.score, 2)}
Risk Level: {st.session_state.risk}

Generated by AI Student Burnout Prevention System
"""

        st.text_area("Report", report, height=200)

        st.download_button(
            "Download Report",
            report,
            file_name="burnout_report.txt"
        )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("""
<div class="footer">
AI Student Burnout Prevention System • Educational Wellness Tool
<br>
Disclaimer: This tool provides supportive insights and is not a medical diagnosis system.
</div>
""", unsafe_allow_html=True)