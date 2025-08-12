# 📄 MacroScope – Malicious Document Triage Toolkit

MacroScope is an open-source, offline-first framework for detecting and analyzing malicious document files.  
It supports **Microsoft Office**, **PDF**, and **RTF** formats, helping analysts and students quickly identify hidden threats like macros, embedded payloads, and exploit signatures.  

---

## ✨ Features
- 🕵️ Detects malicious macros, JavaScript, and embedded objects
- 📂 Supports `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.pdf`, `.rtf`
- 🔍 Extracts and deobfuscates VBA macros & PDF JavaScript
- 🚨 Suspiciousness scoring with clear risk indicators
- 💻 100% local execution – no cloud upload needed
- 🛡️ Runs in isolated processes to protect your system

---

## 💡 Use Cases
- 📨 **Email Security** – Triage suspicious attachments before opening them
- 🧪 **Malware Research** – Quickly surface potential payloads for deeper analysis
- 🏫 **Education & Training** – Teach students about document-based threats
- 🛠️ **Incident Response** – Rapidly investigate documents during phishing incidents
- 📊 **Threat Hunting** – Identify recurring malicious document patterns

---

## 📥 Installation

### Requirements
- Python 3.9+
- `pip` package manager

### Steps
```bash
# 1️⃣ Clone the repository
git clone https://github.com/pottsie283/MacroScope
cd macroscope

# 2️⃣ Create a virtual environment (recommended)
python3 -m venv macroscope
source macroscope/bin/activate  # Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

python scripts/cli.py --help
# 4️⃣ Run MacroScope

---

## 🔮 Future Development
- 📌 **OneNote & HTML Smuggling Support** – Expand file format coverage
- 📌 **Dynamic Analysis Sandbox Mode** – Optional safe execution to capture runtime behavior
- 📌 **Threat Intel Integration** – Check file hashes against known malware databases
- 📌 **GUI Frontend** – Drag-and-drop document analysis for non-technical users
- 📌 **Rule-based Scoring Engine** – Customizable detection rules
- 📌 **Timeline View** – Visualize macro or script execution flow
- 📌 **Multi-Language Support** – Internationalized reports

---

## ⚠️ Disclaimer

MacroScope is provided for **educational and research purposes only**.  
Use it only on files you have permission to analyze.  
The authors are **not responsible** for misuse, damage, or any consequences arising from the use of this software.  
Always run MacroScope in a **safe, isolated environment** when working with suspicious files.