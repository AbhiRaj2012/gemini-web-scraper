import streamlit as st
import pandas as pd
import os
import sys
import asyncio
from typing import Optional, List
from pydantic import create_model, Field
from dotenv import load_dotenv, set_key
from scrapegraphai.graphs import SmartScraperGraph

# --- WINDOWS FIX ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

st.set_page_config(page_title="API Scraping Agent", layout="wide", page_icon="🤖")


# --- SCHEMA ARCHITECT ---
def get_dynamic_schema(intent: str):
    fields = ["name", "email", "phone"]
    if "product" in intent.lower():
        fields = ["item", "price", "link"]

    field_defs = {f: (Optional[str], Field(description=f"The {f}")) for f in fields}
    ItemModel = create_model("ItemModel", **field_defs)
    return create_model("SchemaModel", data=(List[ItemModel], ...))


# --- SIDEBAR: API SETTINGS ---
with st.sidebar:
    st.header("🔑 API Settings")
    curr_key = os.getenv("GOOGLE_API_KEY", "")
    new_key = st.text_input("Google API Key", value=curr_key, type="password")
    new_model = st.text_input("Model Name", value=os.getenv("ONLINE_MODEL", "gemini-1.5-flash"))

    if st.button("Save Settings"):
        set_key(".env", "GOOGLE_API_KEY", new_key)
        set_key(".env", "ONLINE_MODEL", new_model)
        st.success("Saved!")
        st.rerun()

# --- CONFIGURATION ---
model_name = os.getenv("ONLINE_MODEL", "gemini-2.5-flash")
if not model_name.startswith("google_genai/"):
    model_name = f"google_genai/{model_name}"

config = {
    "llm": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "model": model_name,
        "max_tokens": 8192
    },
    "chunk_size": 4096,
    "headless": True,
    "timeout": 120,
    "only_fixed_schemas": True
}

# --- UI ---
st.title("API-Powered Scraping Agent 🤖")
url = st.text_input("URL", "https://infostatics.in/")
intent = st.text_input("What to extract?", "Extract names and emails")

if st.button("Run Extraction", type="primary"):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Please enter your Google API Key in the sidebar.")
    else:
        with st.status("Agent active...") as status:
            try:
                Schema = get_dynamic_schema(intent)

                # THE "ROBOT" PROMPT
                prompt = f"""
                Identify all {intent} from the provided text.
                Rules:
                1. Extract accurate data only.
                2. If info is missing, use null.
                3. Return valid JSON only. 
                4. No conversation.
                """

                scraper = SmartScraperGraph(
                    prompt=prompt,
                    source=url,
                    config=config,
                    schema=Schema
                )

                result = scraper.run()

                if result and "data" in result and len(result["data"]) > 0:
                    status.update(label="Success!", state="complete")

                    # Display Results
                    df = pd.DataFrame(result["data"])
                    st.dataframe(df, use_container_width=True)

                    # CSV Download
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download CSV", csv, "extracted_data.csv", "text/csv")
                else:
                    status.update(label="Extraction failed", state="error")
                    st.error("Model failed to structure data. Try adjusting the prompt or check the URL.")
                    st.write("Debug Output:", result)

            except Exception as e:
                status.update(label="Error Occurred", state="error")
                st.error(f"Error: {e}")