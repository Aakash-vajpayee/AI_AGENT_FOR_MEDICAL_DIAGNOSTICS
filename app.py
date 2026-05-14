import os
import time
import streamlit as st
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(
    page_title="MediAI Diagnostics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #020818 0%, #0a1628 40%, #051020 100%); }
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 20% 20%, rgba(0,212,255,0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0,255,136,0.05) 0%, transparent 50%);
    pointer-events: none; z-index: 0;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,255,136,0.15));
    border: 1px solid rgba(0,212,255,0.3);
    color: #00d4ff; padding: 6px 20px; border-radius: 50px;
    font-size: 12px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
    animation: fadeInDown 0.8s ease;
}
.hero-title {
    font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #00ff88 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1.2; margin: 16px 0; animation: fadeInUp 0.8s ease 0.2s both;
}
.hero-subtitle { color: rgba(255,255,255,0.5); font-size: 17px; font-weight: 300; animation: fadeInUp 0.8s ease 0.4s both; }
.stats-row { display: flex; justify-content: center; gap: 20px; margin: 30px 0; flex-wrap: wrap; }
.stat-item {
    text-align: center; padding: 16px 28px;
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; transition: all 0.3s ease;
}
.stat-item:hover { background: rgba(0,212,255,0.08); border-color: rgba(0,212,255,0.3); transform: translateY(-3px); }
.stat-number {
    font-size: 28px; font-weight: 700;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 11px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.custom-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent); margin: 30px 0; }
.upload-box {
    background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(0,255,136,0.03));
    border: 1px solid rgba(0,212,255,0.15); border-radius: 24px; padding: 36px; margin: 20px 0;
}
.result-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 28px; margin: 14px 0; transition: all 0.3s ease;
}
.result-card:hover { border-color: rgba(0,212,255,0.3); box-shadow: 0 8px 32px rgba(0,212,255,0.1); }
.result-title { font-size: 17px; font-weight: 600; color: #ffffff; margin-bottom: 14px; }
.result-body { color: rgba(255,255,255,0.7); font-size: 14px; line-height: 1.7; border-left: 2px solid rgba(0,212,255,0.3); padding-left: 16px; }
.final-box {
    background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(0,255,136,0.05));
    border: 1px solid rgba(0,212,255,0.3); border-radius: 24px; padding: 40px;
    animation: glowPulse 3s ease-in-out infinite;
}
.final-title {
    font-family: 'Playfair Display', serif; font-size: 26px;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 20px;
}
.final-content { color: rgba(255,255,255,0.85); font-size: 15px; line-height: 1.8; }
.status-dot { width: 8px; height: 8px; background: #00ff88; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; margin-right: 8px; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #050e1f 0%, #020810 100%) !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #00ff88) !important; color: #000 !important;
    font-weight: 700 !important; font-size: 16px !important; padding: 16px !important;
    border-radius: 50px !important; border: none !important;
    box-shadow: 0 8px 32px rgba(0,212,255,0.3) !important; width: 100% !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 40px rgba(0,212,255,0.5) !important; }
.stTextArea textarea { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 16px !important; color: rgba(255,255,255,0.8) !important; }
p, li { color: rgba(255,255,255,0.7) !important; }
h1, h2, h3 { color: #ffffff !important; }
label { color: rgba(255,255,255,0.6) !important; }
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.4; transform:scale(1.4); } }
@keyframes glowPulse { 0%,100% { box-shadow: 0 0 20px rgba(0,212,255,0.1); } 50% { box-shadow: 0 0 40px rgba(0,212,255,0.25); } }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 20px;">
        <div style="font-size:52px; margin-bottom:8px;">🧬</div>
        <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:700;
                    background:linear-gradient(135deg,#00d4ff,#00ff88);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            MediAI
        </div>
        <div style="font-size:10px; color:rgba(255,255,255,0.3); letter-spacing:3px; text-transform:uppercase;">
            Diagnostics System
        </div>
    </div>
    """, unsafe_allow_html=True)

    load_dotenv(dotenv_path='apikey.env')
    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:
        st.markdown('<div style="background:rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.25); border-radius:12px; padding:12px 16px; margin:8px 0;"><span class="status-dot"></span><span style="color:#00ff88; font-size:13px; font-weight:500;">Gemini API Connected</span></div>', unsafe_allow_html=True)
    else:
        st.error("❌ API Key missing!")
        st.stop()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px; font-weight:600; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:1px;">AI Specialists</p>', unsafe_allow_html=True)

    for icon, name, desc, color in [
        ("🫀", "Cardiologist", "Heart & cardiovascular", "#ff6b6b"),
        ("🧠", "Psychologist", "Mental health evaluation", "#a855f7"),
        ("🫁", "Pulmonologist", "Respiratory analysis", "#00d4ff"),
    ]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                    border-radius:14px; padding:14px 16px; margin:8px 0; border-left:3px solid {color};">
            <div style="font-size:18px; margin-bottom:4px;">{icon} <span style="color:#fff; font-size:14px; font-weight:600;">{name}</span></div>
            <div style="font-size:12px; color:rgba(255,255,255,0.4);">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,170,0,0.06); border:1px solid rgba(255,170,0,0.2); border-radius:12px; padding:14px;">
        <div style="font-size:11px; color:rgba(255,200,0,0.7); line-height:1.6;">
            ⚠️ <strong>Disclaimer</strong><br>
            For research & educational purposes only. Not intended for clinical use.
        </div>
    </div>
    """, unsafe_allow_html=True)

# HERO
st.markdown("""
<div style="text-align:center; padding: 50px 20px 30px;">
    <div class="hero-badge">🧬 Powered by Google Gemini AI</div>
    <div class="hero-title">AI Medical Diagnostics</div>
    <div class="hero-subtitle">Multi-specialist AI analysis for comprehensive medical assessment</div>
</div>
<div class="stats-row">
    <div class="stat-item"><div class="stat-number">3</div><div class="stat-label">AI Specialists</div></div>
    <div class="stat-item"><div class="stat-number">10+</div><div class="stat-label">Sample Reports</div></div>
    <div class="stat-item"><div class="stat-number">AI</div><div class="stat-label">Powered</div></div>
    <div class="stat-item"><div class="stat-number">Free</div><div class="stat-label">Gemini API</div></div>
</div>
<div class="custom-divider"></div>
""", unsafe_allow_html=True)

# UPLOAD
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
st.markdown("### 📋 Upload Medical Report")
st.markdown('<p style="color:rgba(255,255,255,0.4); font-size:14px; margin-top:-10px;">Upload a .txt file or paste report text manually</p>', unsafe_allow_html=True)

input_method = st.radio("", ["📁 File Upload (.txt)", "✏️ Paste Text Manually"], horizontal=True, label_visibility="collapsed")

medical_report = ""
if input_method == "📁 File Upload (.txt)":
    uploaded_file = st.file_uploader("", type=["txt"], label_visibility="collapsed")
    if uploaded_file:
        medical_report = uploaded_file.read().decode("utf-8")
        st.success(f"✅ **{uploaded_file.name}** loaded!")
        with st.expander("👁️ Preview"):
            st.text(medical_report[:500] + "..." if len(medical_report) > 500 else medical_report)
else:
    medical_report = st.text_area("", height=180, placeholder="Paste medical report content here...", label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# RUN
if st.button("🚀 Run AI Diagnosis", use_container_width=True):
    if not medical_report.strip():
        st.warning("⚠️ Please upload or paste a medical report first!")
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=api_key)

        def run_agent(agent, name, retries=3, wait=60):
            agent.llm = llm
            for _ in range(retries):
                try:
                    r = agent.run()
                    if r: return r
                except: time.sleep(wait)
            return "Analysis incomplete — API quota reached. Please retry later."

        responses = {}
        st.markdown("### 🔬 Specialist Analysis Running...")
        c1, c2, c3 = st.columns(3)

        with c1:
            with st.spinner("🫀 Cardiologist..."): responses["Cardiologist"] = run_agent(Cardiologist(medical_report), "Cardiologist")
            st.success("🫀 Done!")
        with c2:
            time.sleep(30)
            with st.spinner("🧠 Psychologist..."): responses["Psychologist"] = run_agent(Psychologist(medical_report), "Psychologist")
            st.success("🧠 Done!")
        with c3:
            time.sleep(30)
            with st.spinner("🫁 Pulmonologist..."): responses["Pulmonologist"] = run_agent(Pulmonologist(medical_report), "Pulmonologist")
            st.success("🫁 Done!")

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 Specialist Reports")

        for icon, key in [("🫀", "Cardiologist"), ("🧠", "Psychologist"), ("🫁", "Pulmonologist")]:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">{icon} {key} Report</div>
                <div class="result-body">{responses.get(key, "No data")}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        time.sleep(30)
        with st.spinner("👥 Preparing Final Diagnosis..."):
            team = MultidisciplinaryTeam(
                cardiologist_report=responses.get("Cardiologist", "No data"),
                psychologist_report=responses.get("Psychologist", "No data"),
                pulmonologist_report=responses.get("Pulmonologist", "No data")
            )
            team.llm = llm
            final = run_agent(team, "MultidisciplinaryTeam")

        st.markdown(f"""
        <div class="final-box">
            <div class="final-title">⚕️ Final Multidisciplinary Diagnosis</div>
            <div class="final-content">{final}</div>
        </div>
        """, unsafe_allow_html=True)

        os.makedirs("results", exist_ok=True)
        with open("results/final_diagnosis.txt", "w", encoding="utf-8") as f:
            f.write("SPECIALIST REPORTS\n\n" + "\n\n".join([f"{k}:\n{v}" for k,v in responses.items()]) + f"\n\nFINAL DIAGNOSIS:\n{final}")

        st.download_button("⬇️ Download Full Report", data=open("results/final_diagnosis.txt").read(), file_name="diagnosis_report.txt", mime="text/plain")
        st.balloons()
