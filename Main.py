import os
import time
from dotenv import load_dotenv
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from langchain_google_genai import ChatGoogleGenerativeAI

# Loading API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    load_dotenv(dotenv_path='apikey.env')
    api_key = os.getenv("GOOGLE_API_KEY")

# Gemini Model Setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", google_api_key=api_key)

# Read the medical report
try:
    with open("Medical Reports/Medical Rerort - Michael Johnson - Panic Attack Disorder.txt", "r") as file:
        medical_report = file.read()
except FileNotFoundError:
    print("Error: Medical report file nahi mili. Path check karein.")
    exit()

# Function to run agent with retry
def run_agent_with_retry(agent, name, retries=3, wait=60):
    agent.llm = llm
    for attempt in range(retries):
        try:
            print(f"{name} is running... (attempt {attempt+1})")
            response = agent.run()
            if response:
                print(f"{name} ne report taiyar kar li hai.")
                return response
        except Exception as e:
            print(f"{name} error: quota limit - {wait} second wait kar raha hoon...")
            time.sleep(wait)
    return f"{name}: Analysis fail ho gayi quota ki wajah se."

# Run agents ONE BY ONE with delay
print("Agents processing shuru ho gayi hai...")
responses = {}

responses["Cardiologist"] = run_agent_with_retry(Cardiologist(medical_report), "Cardiologist")
time.sleep(30)

responses["Psychologist"] = run_agent_with_retry(Psychologist(medical_report), "Psychologist")
time.sleep(30)

responses["Pulmonologist"] = run_agent_with_retry(Pulmonologist(medical_report), "Pulmonologist")
time.sleep(30)

# Multidisciplinary Team
print("Final diagnosis banayi ja rahi hai...")
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses.get("Cardiologist", "No data"),
    psychologist_report=responses.get("Psychologist", "No data"),
    pulmonologist_report=responses.get("Pulmonologist", "No data")
)
team_agent.llm = llm
final_diagnosis = run_agent_with_retry(team_agent, "MultidisciplinaryTeam")

if not final_diagnosis:
    final_diagnosis = "Error: AI response generate nahi ho paya."

# Save result
final_diagnosis_text = "### Final Diagnosis:\n\n" + str(final_diagnosis)
txt_output_path = "results/final_diagnosis.txt"
os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)

with open(txt_output_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(final_diagnosis_text)

print(f"\nSuccess! Final diagnosis save ho gayi hai: {txt_output_path}")
