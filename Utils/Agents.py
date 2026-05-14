from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        # Prompt initialize karein
        self.prompt_template = self.create_prompt_template()
        
        # GEMINI MODEL SETUP (OpenAI ki jagah)
        # Yahan hum Gemini use kar rahe hain jo free tier support karta hai
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite", # "-latest" lagane se hamesha updated version milega
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
            templates = f"""
                Act like a multidisciplinary team of healthcare professionals.
                Review the following reports and provide 3 possible health issues with reasons.
                
                Cardiologist Report: {self.extra_info.get('cardiologist_report', '')}
                Psychologist Report: {self.extra_info.get('psychologist_report', '')}
                Pulmonologist Report: {self.extra_info.get('pulmonologist_report', '')}
            """
        else:
            templates = {
                "Cardiologist": "Act like a cardiologist. Review: {medical_report}. Provide causes and next steps.",
                "Psychologist": "Act like a psychologist. Review: {medical_report}. Provide mental health issues and next steps.",
                "Pulmonologist": "Act like a pulmonologist. Review: {medical_report}. Provide respiratory issues and next steps."
            }
            templates = templates[self.role]
        return PromptTemplate.from_template(templates)
    
    def run(self):
        print(f"{self.role} is running...")
        # Check if medical_report exists to avoid formatting errors
        report_content = self.medical_report if self.medical_report else ""
        prompt = self.prompt_template.format(medical_report=report_content)
        
        try:
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error occurred in {self.role}:", e)
            return "Analysis fail ho gaya API error ki wajah se."

# Specialized agent classes
class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)
