import streamlit as st  # <-- Sabse pehle ye hona chahiye
import os
import time
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Title aur Page Config (Optional par accha lagta hai)
st.set_page_config(page_title="MediAI Diagnostics", page_icon="🩺")

# 2. Loading API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    load_dotenv(dotenv_path='apikey.env')
    api_key = os.getenv("GOOGLE_API_KEY")

# 3. Gemini Model Setup
# Check karein ki api_key khali toh nahi hai
if not api_key:
    st.error("API Key nahi mili! Streamlit Secrets ya apikey.env check karein.")
    st.stop()

# ... (upar ka code same rahega)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=api_key)

# 4. Read the medical report
# --- Is section ko replace karein (Line 29-30) ---
import os
path_with_txt = "Medical Reports/Medical Rerort - Michael Johnson - Panic Attack Disorder.txt"
path_without_txt = "Medical Reports/Medical Rerort - Michael Johnson - Panic Attack Disorder"

if os.path.exists(path_with_txt):
    file_path = path_with_txt
elif os.path.exists(path_without_txt):
    file_path = path_without_txt
else:
    st.error(f"🚨 File nahi mili! Folder mein check karein.")
    st.write("Dhoondi gayi file: ", path_with_txt)
    st.stop()
# --- Replacement Khatam ---

try:
    with open(file_path, "r", encoding="utf-8") as file: # <--- 1 Tab space
        medical_report = file.read() # <--- 2 Tab spaces (with ke andar)
except Exception as e: # <--- try ke niche bilkul barabar
    st.error(f"Error reading file: {e}")
    st.stop()

# 5. Function to run agent with retry
def run_agent_with_retry(agent, name, retries=3, wait=60):
    agent.llm = llm
    for attempt in range(retries):
        try:
            # print() terminal mein dikhega, screen ke liye hum progress messages use karenge
            response = agent.run()
            if response:
                return response
        except Exception as e:
            st.warning(f"{name} error (Attempt {attempt+1}): Quota limit hit. {wait}s wait kar rahe hain...")
            time.sleep(wait)
    return f"{name}: Analysis fail ho gayi quota ki wajah se."

# 6. UI Header
st.title("🏥 MediAI Multi-Agent Diagnostic System")
st.markdown("---")

# 7. Agent Execution
responses = {}

# Cardiologist
with st.spinner("🩺 Cardiologist analysis kar raha hai..."):
    responses["Cardiologist"] = run_agent_with_retry(Cardiologist(medical_report), "Cardiologist")
    if "fail" not in responses["Cardiologist"]:
        st.success("✅ Cardiologist ne report taiyar kar li hai.")
    else:
        st.error("❌ Cardiologist analysis fail ho gayi.")

time.sleep(5)

# Psychologist
with st.spinner("🧠 Psychologist report check kar raha hai..."):
    responses["Psychologist"] = run_agent_with_retry(Psychologist(medical_report), "Psychologist")
    if "fail" not in responses["Psychologist"]:
        st.success("✅ Psychologist ne report taiyar kar li hai.")
    else:
        st.error("❌ Psychologist analysis fail ho gayi.")

time.sleep(5)

# Pulmonologist
with st.spinner("🫁 Pulmonologist lung health analyze kar raha hai..."):
    responses["Pulmonologist"] = run_agent_with_retry(Pulmonologist(medical_report), "Pulmonologist")
    if "fail" not in responses["Pulmonologist"]:
        st.success("✅ Pulmonologist ne report taiyar kar li hai.")
    else:
        st.error("❌ Pulmonologist analysis fail ho gayi.")

# 8. Final Diagnosis (Multidisciplinary Team)
st.divider()
st.subheader("👨‍⚕️ Final Consultation")

with st.spinner("Sare agents ki reports combine karke final diagnosis banayi ja rahi hai..."):
    team_agent = MultidisciplinaryTeam(
        cardiologist_report=responses.get("Cardiologist", "No data"),
        psychologist_report=responses.get("Psychologist", "No data"),
        pulmonologist_report=responses.get("Pulmonologist", "No data")
    )
    team_agent.llm = llm
    final_diagnosis = run_agent_with_retry(team_agent, "MultidisciplinaryTeam")

# 9. Display Final Result
if final_diagnosis and "fail" not in str(final_diagnosis):
    st.header("📋 Final Medical Analysis Report")
    st.markdown(final_diagnosis)
    st.balloons()
    
    # Save result
    final_diagnosis_text = "### Final Diagnosis:\n\n" + str(final_diagnosis)
    txt_output_path = "results/final_diagnosis.txt"
    os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)
    
    with open(txt_output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(final_diagnosis_text)
    
    st.sidebar.success(f"Report saved: {txt_output_path}")
    st.sidebar.caption("made with ❤️ by Aakash Vajpayee")
else:
    st.error("Error: AI response generate nahi ho paya. Quota check karein.")