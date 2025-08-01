#  Tech Support & Troubleshooting ReAct Agent

A conversational tech support assistant built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [Streamlit](https://streamlit.io/).  
**Solves real-world device and software issues by:**
- Searching the web and forums in real time
- Generating step-by-step instructions for troubleshooting
- Using multiple sources to ensure the best fix for your case

---

##  Features

- **ReAct Multi-Tool Reasoning:** The agent breaks your problem into subtasks, uses the right tool for each part, and gives a single, clear "Final answer" at the end.
- **Integrated Tools:**
  - SerpAPI, DuckDuckGo, Tavily for web and community searches
  - Python REPL and custom step-by-step tutorial tools
  - Forum or FAQ scraper/search via web/targeted queries
- **Streamlit UI:** Only the final solution is shown to users, in clear formatting.

---

##  Example User Prompts

### Android & iPhone
---
My Android phone overheats and runs slow after an update.
What are common fixes? Give me step-by-step instructions to speed it up,
and check if there are reports of this on Samsung forums.
---
My iPhone battery drains quickly after the latest update.
What are the most effective fixes? Give me steps for clearing cache, and check Apple community forums for recent battery complaints.
---

### PC / Mac
---
My Windows 11 laptop randomly reboots.
Search for possible causes, list step-by-step troubleshooting,
and find recent related reports on Microsoft support forums.
---

### Apps & Services
---
WhatsApp crashes every time I open it.
Find any official fixes or updates, and guide me through clearing app cache on Android.
---

### General Electronics
My smart TV won’t connect to Wi-Fi.
What are common solutions, and are other users reporting this with the same TV brand?
---

## 🛠️ Installation
   ```bash

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/Viswa-Prakash/Tech_Support_Troubleshooting_MultiTool_Agent.git
   cd Tech_Support_Troubleshooting_MultiTool_Agent

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   

3. **API Keys:**
   ```bash
    - OpenAI API Key
    - SERPAPI Key
    - TAVILY API Key

4. **Run the Script:**
   ```bash
    streamlit run app.py   

## 📌 Usage
   - The script will prompt you to enter the type of device you're troubleshooting.
   - Based on your input, it will display a list of common issues and their corresponding solutions.
   - You can select an issue to get detailed steps or search for more information online.
   - The script will also check for recent reports on relevant forums to help you identify if others are experiencing similar issues.