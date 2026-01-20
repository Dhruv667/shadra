import streamlit as st
import streamlit.components.v1 as components
import joblib
import numpy as np
import time

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Student Report Card",
    page_icon="🎓",
    layout="centered"
)

# ---------------------------
# CSS (Modern + Responsive)
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

* { font-family: 'Poppins', sans-serif; }

.block-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
}

.header-container {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
}

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
    margin: 0;
}

.subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    margin-top: 0.35rem;
    font-weight: 300;
}

.step-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    color: white;
    padding: 0.45rem 1.2rem;
    border-radius: 999px;
    font-weight: 600;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(10px);
}

.card {
    background: white;
    border-radius: 16px;
    padding: 1.6rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid rgba(102, 126, 234, 0.10);
}

.section-title {
    font-size: 1.55rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.25rem;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.25);
    width: 100%;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 25px rgba(102, 126, 234, 0.32);
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin-top: 0.5rem;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 22px rgba(102, 126, 234, 0.25);
}

.metric-label { font-size: 0.85rem; opacity: 0.9; }
.metric-value { font-size: 1.6rem; font-weight: 800; margin-top: 0.2rem; }

.report-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.6rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin: 1.2rem 0;
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.25);
}

.grade-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    font-weight: 900;
    background: white;
    color: #667eea;
    width: 92px;
    height: 92px;
    border-radius: 999px;
    margin: 0.6rem auto;
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}

.result-badge {
    display: inline-block;
    padding: 0.85rem 1.4rem;
    border-radius: 999px;
    font-size: 1.2rem;
    font-weight: 900;
    margin: 0.6rem auto;
}

.pass-badge {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
}

.fail-badge {
    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    color: white;
}

.chart-container {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 10px 22px rgba(0,0,0,0.08);
}

.bar-chart {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    height: 280px;
    padding: 1.2rem;
    gap: 0.8rem;
}

.bar-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.45rem;
}

.bar {
    width: 100%;
    border-radius: 10px 10px 0 0;
    position: relative;
    box-shadow: 0 -8px 18px rgba(102, 126, 234, 0.20);
    animation: growBar 0.9s ease-out;
}

@keyframes growBar { from { height: 0; } }

.bar-value {
    position: absolute;
    top: -28px;
    left: 50%;
    transform: translateX(-50%);
    font-weight: 800;
    color: #667eea;
    font-size: 0.95rem;
}

.bar-label {
    font-size: 0.82rem;
    color: #555;
    text-align: center;
    font-weight: 700;
    max-width: 100%;
}

.donut-chart {
    width: 180px;
    height: 180px;
    margin: 0.5rem auto;
    border-radius: 50%;
    background: conic-gradient(#667eea 0deg var(--percentage), #f0f0f0 var(--percentage) 360deg);
    display: flex;
    align-items: center;
    justify-content: center;
}

.donut-inner {
    width: 128px;
    height: 128px;
    background: white;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.donut-grade {
    font-size: 2.2rem;
    font-weight: 900;
    color: #667eea;
    line-height: 1;
}

.donut-percent {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.25rem;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

@media (max-width: 768px) {
    .main-title { font-size: 1.8rem; }
    .metric-row { grid-template-columns: 1fr; }
    .bar-chart { height: 240px; padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load Model
# ---------------------------
model = joblib.load("student_report_model.pkl")

# ---------------------------
# Session State Initialization
# ---------------------------
defaults = {
    "step": 1,
    "name": "",
    "roll_no": "",
    "section": "1",
    "standard": "10th",
    "subjects": [],
    "subject_names": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class='header-container'>
    <h1 class='main-title'>🎓 Student Report Card Generator</h1>
    <p class='subtitle'>sanket kumar giri</p>
</div>
""", unsafe_allow_html=True)

st.progress(st.session_state.step / 3)

# ---------------------------
# STEP 1
# ---------------------------
if st.session_state.step == 1:
    st.markdown("<div class='step-badge'>STEP 1 / 3</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>🧾 Student Details</h2>", unsafe_allow_html=True)

    name = st.text_input("👤 Student Name", value=st.session_state.name)
    roll_no = st.text_input("🆔 Roll Number", value=st.session_state.roll_no)

    c1, c2 = st.columns(2)
    with c1:
        section = st.selectbox("📌 Section", ["1", "2", "3"], index=["1", "2", "3"].index(st.session_state.section))
    with c2:
        standard = st.selectbox("🏫 Standard", ["10th", "12th"], index=["10th", "12th"].index(st.session_state.standard))

    st.write("")
    if st.button("➡️ Next: Enter Marks"):
        if name.strip() == "" or roll_no.strip() == "":
            st.warning("⚠️ Please enter Student Name and Roll Number.")
        else:
            st.session_state.name = name
            st.session_state.roll_no = roll_no
            st.session_state.section = section
            st.session_state.standard = standard
            st.session_state.step = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# STEP 2
# ---------------------------
elif st.session_state.step == 2:
    st.markdown("<div class='step-badge'>STEP 2 / 3</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>📚 Enter Subject Marks</h2>", unsafe_allow_html=True)

    standard = st.session_state.standard

    if standard == "10th":
        col1, col2 = st.columns(2)
        with col1:
            english = st.number_input("📖 English", 0, 100, key="english_10")
            hindi = st.number_input("📕 Hindi", 0, 100, key="hindi_10")
            Python = st.number_input("📘 Python", 0, 100, key="Python_10")
        with col2:
            maths = st.number_input("🔢 Mathematics", 0, 100, key="maths_10")
            science = st.number_input("🔬 Science", 0, 100, key="science_10")

        subjects = [english, hindi, Python, maths, science]
        subject_names = ["English", "Hindi", "Python", "Mathematics", "Science"]

    else:
        col1, col2 = st.columns(2)
        with col1:
            physics = st.number_input("⚛️ Physics", 0, 100, key="physics_12")
            chemistry = st.number_input("🧪 Chemistry", 0, 100, key="chemistry_12")
            maths = st.number_input("🔢 Mathematics", 0, 100, key="maths_12")
        with col2:
            biology = st.number_input("🧬 Biology", 0, 100, key="biology_12")
            english = st.number_input("📖 English", 0, 100, key="english_12")

        subjects = [physics, chemistry, maths, biology, english]
        subject_names = ["Physics", "Chemistry", "Mathematics", "Biology", "English"]

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Back to Details"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("➡️ Next: Generate Report"):
            st.session_state.subjects = subjects
            st.session_state.subject_names = subject_names
            st.session_state.step = 3
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# STEP 3
# ---------------------------
elif st.session_state.step == 3:
    st.markdown("<div class='step-badge'>STEP 3 / 3</div>", unsafe_allow_html=True)

    name = st.session_state.name
    roll_no = st.session_state.roll_no
    section = st.session_state.section
    standard = st.session_state.standard
    subjects = st.session_state.subjects
    subject_names = st.session_state.subject_names

    total_preview = sum(subjects)
    percent_preview = (total_preview / 500) * 100

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">Total Marks</div>
            <div class="metric-value">{total_preview}/500</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Percentage</div>
            <div class="metric-value">{percent_preview:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Section</div>
            <div class="metric-value">{section}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    generate = st.button("✨ Generate Complete Report Card")

    if generate:
        with st.spinner("🎨 Generating your report card..."):
            time.sleep(1.2)

        total_marks = sum(subjects)
        percentage = (total_marks / 500) * 100
        average_marks = total_marks / 5

        if percentage > 90:
            grade = "A+"
        elif percentage >= 75:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 35:
            grade = "D"
        else:
            grade = "F"

        input_data = np.array([[average_marks, percentage]])
        prediction = model.predict(input_data)

        if any(mark < 35 for mark in subjects):
            result = "FAIL"
        else:
            result = "PASS" if prediction[0] == 1 else "FAIL"

        st.markdown(f"""
        <div class='report-header'>
            <h2 style='margin:0;'>📋 Final Report Card</h2>
            <p style='margin: 0.35rem 0 0 0; opacity: 0.92;'>
                {name} • Roll No: {roll_no} • {standard} • Section {section}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="grade-badge">{grade}</div>
                <div style="font-weight:800; color:#667eea;">GRADE</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            percentage_deg = percentage * 3.6
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="donut-chart" style="--percentage:{percentage_deg}deg;">
                    <div class="donut-inner">
                        <div class="donut-grade">{percentage:.1f}</div>
                        <div class="donut-percent">%</div>
                    </div>
                </div>
                <div style="font-weight:800; color:#667eea;">PERCENTAGE</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            badge_class = "pass-badge" if result == "PASS" else "fail-badge"
            icon = "✅" if result == "PASS" else "❌"
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="result-badge {badge_class}">{icon} {result}</div>
                <div style="font-weight:800; color:#667eea;">RESULT</div>
            </div>
            """, unsafe_allow_html=True)

        # ---------------------------
        # SUBJECT BAR CHART (PERMANENT FIX)
        # ---------------------------
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; color:#667eea; margin-bottom:1.2rem;'>📊 Subject-wise Performance</h3>", unsafe_allow_html=True)

        bars_html = "<div class='bar-chart'>"
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']

        for i, (subject, mark) in enumerate(zip(subject_names, subjects)):
            height_percent = (mark / 100) * 100
            color = colors[i % len(colors)]
            bars_html += f"""
            <div class='bar-item'>
                <div class='bar' style='height:{height_percent}%; background:linear-gradient(180deg, {color} 0%, {color}dd 100%);'>
                    <div class='bar-value'>{mark}</div>
                </div>
                <div class='bar-label'>{subject}</div>
            </div>
            """

        bars_html += "</div>"

        # IMPORTANT: Using components.html stops the black popup forever
        components.html(bars_html, height=340, scrolling=False)

        st.markdown("</div>", unsafe_allow_html=True)

        if result == "PASS":
            st.success("✅ Result: PASS")
            st.balloons()
        else:
            st.error("❌ Result: FAIL")
            st.info("Tip: Minimum 35 marks required in each subject.")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Back to Marks"):
            st.session_state.step = 2
            st.rerun()
    with c2:
        if st.button("🔁 Start New Report"):
            st.session_state.step = 1
            st.session_state.subjects = []
            st.session_state.subject_names = []
            st.rerun()
