# 🕵️‍♂️ Gemini Autonomous Web Scraper

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=google&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EBA5F?logo=playwright&logoColor=white)

An intelligent, API-powered web scraping agent built with Python, Streamlit, and ScrapeGraphAI. It leverages **Google's Gemini 1.5 Flash** to autonomously navigate websites, dynamically generate data schemas based on user intent, and extract structured leads (names, emails, prices, etc.) into ready-to-use CSV files.

## ✨ Features
* **🧠 Dynamic Schema Architecture:** Tell the AI what you want (e.g., "Extract faculty names and emails"), and it automatically builds the underlying Pydantic models.
* **⚡ Gemini 2.5 Flash Integration:** Utilizes a massive 1M token context window to parse complex, messy HTML without crashing.
* **🛡️ Robust Error Handling:** Built-in timeouts, Playwright integration, and Windows asyncio fixes for bulletproof execution.
* **📊 One-Click Export:** Instantly download scraped data as clean, formatted CSV files.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed. You will also need a free [Google Gemini API Key](https://aistudio.google.com/).

### 2. Installation
Clone the repository and set up your virtual environment:
```bash
git clone [https://github.com/YOUR-USERNAME/gemini-web-scraper.git](https://github.com/YOUR-USERNAME/gemini-web-scraper.git)
cd gemini-web-scraper
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install streamlit pandas python-dotenv scrapegraphai langchain-google-genai pydantic
playwright install
```
### 3. Configuration
Create a .env file in the root directory and add your Google API key:
```bash
GOOGLE_API_KEY=your_api_key_here
ONLINE_MODEL=gemini-2.5-flash
```

### 4. Run the Agent
Launch the Streamlit interface:
```bash
streamlit run main.py
```
## 🛠️ Usage
* Paste the target URL into the app.

* Enter your Instruction (e.g., "Extract all product names and their prices").

* Click Run Extraction.

* Download the resulting CSV file.

## ⚠️ Disclaimer
This tool is for educational and authorized data extraction purposes only. Always respect a website's robots.txt file and Terms of Service when scraping.
