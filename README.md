# AI-Agents-for-Medical-Diagnostics

<img width="900" alt="image" src="https://github.com/user-attachments/assets/b7c87bf6-dfff-42fe-b8d1-9be9e6c7ce86">

A Python project that creates specialized **LLM-based AI agents** to analyze complex medical cases.  
The system integrates insights from different medical specialists to provide comprehensive assessments  
and suggested treatment directions, demonstrating the potential of AI in multidisciplinary medicine.

> ⚠️ **Disclaimer**: This project is for research and educational purposes only. It is **not intended for clinical use**.

---

## ✨ What's New (Latest Update)

- Migrated LLM from OpenAI to **Google Gemini 2.0 Flash Lite** (free tier supported)
- Fixed **Python 3.14 compatibility** issue — now uses Python 3.11
- Replaced concurrent agent execution with **sequential execution + retry logic** to handle API rate limits gracefully
- Updated `requirements.txt` and added `.gitignore`
- Added **MIT License**

---

## 🚀 How It Works

Three specialized AI agents powered by **Google Gemini 2.0 Flash Lite** analyze a medical report sequentially.  
Each agent returns its findings, which are then combined by a **Multidisciplinary Team agent** into a final diagnosis.

### AI Agents

**1. 🫀 Cardiologist Agent**
- *Focus*: Detect cardiac issues such as arrhythmias or structural abnormalities.
- *Recommendations*: Cardiovascular testing, monitoring, and management strategies.

**2. 🧠 Psychologist Agent**
- *Focus*: Identify psychological conditions (e.g., panic disorder, anxiety).
- *Recommendations*: Therapy, stress management, or medication adjustments.

**3. 🫁 Pulmonologist Agent**
- *Focus*: Assess respiratory causes for symptoms (e.g., asthma, breathing disorders).
- *Recommendations*: Lung function tests, breathing exercises, respiratory treatments.

**4. 👥 Multidisciplinary Team Agent**
- Combines all three reports into a final comprehensive diagnosis.

---

## 📂 Repository Structure

```
AI-Agents-for-Medical-Diagnostics/
├── Medical Reports/      → Sample synthetic medical report (.txt files)
├── Results/              → AI-generated diagnosis outputs
├── Utils/
│   └── Agents.py         → Agent class definitions
├── Main.py               → Entry point — runs all agents
├── apikey.env            → Your Google API key (not committed to git)
├── requirements.txt      → Python dependencies
└── README.md
```

---

## ⚡ Quickstart

### Requirements
- Python **3.11** (recommended — 3.14 has compatibility issues with LangChain)
- Google Gemini API key (free) → [Get it here](https://aistudio.google.com/apikey)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/AI-Agents-for-Medical-Diagnostics.git
cd AI-Agents-for-Medical-Diagnostics
```

### 2. Create virtual environment
```bash
py -3.11 -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API key
Create a file named `apikey.env` in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Add a medical report
Place your `.txt` medical report inside the `Medical Reports/` folder.  
Then update this line in `Main.py`:
```python
with open("Medical Reports/YOUR_REPORT_FILE.txt", "r") as file:
```

### 6. Run the system
```bash
python Main.py
```

Output will be saved to `results/final_diagnosis.txt`.

---

## 📌 Notes

- This project uses the **free tier** of Google Gemini API (15 requests/min, 1500/day).
- If you hit quota limits, wait a minute and retry — the code handles this automatically.
- Do **not** commit `apikey.env` to GitHub — it's already in `.gitignore`.

---

## 🔮 Future Enhancements

- **Specialist Expansion**: Add agents for Neurology, Endocrinology, Immunology.
- **Web UI**: Flask or Streamlit interface for uploading reports and viewing results.
- **Local LLM Support**: Integrate models like **Llama 3** via Ollama for offline use.
- **Vision Capabilities**: Enable analysis of radiology images and medical scans.
- **Live Data Tools**: Real-time medical dataset querying.
- **PDF Support**: Accept PDF medical reports directly.

---

## 📜 License

This repository is licensed under the **MIT License**.  
You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions described in the [LICENSE](LICENSE) file.  
The software is provided **"as is"**, without warranty of any kind.