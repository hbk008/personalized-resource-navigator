import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
import openai
import json
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env file. Please add it to enable LLM search.")
    st.stop()

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load resources
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("resources.csv")
        # Removed the line that displayed the database count
        return df
    except FileNotFoundError:
        st.error("resources.csv not found. Please run generate_data.py first.")
        return pd.DataFrame()

# Current algorithm: Fuzzy matching
def search_resources(df, zip_code, needs, insurance, language, gender):
    results = []
    for _, row in df.iterrows():
        zip_match = str(row['ZIP_Code']).strip() == str(zip_code).strip()
        needs_match = fuzz.partial_ratio(needs.lower(), row['Services'].lower()) > 80
        insurance_match = insurance.lower() in row['Eligibility'].lower() or 'all' in row['Eligibility'].lower()
        language_match = language.lower() in row['Languages'].lower() or 'all' in row['Languages'].lower()
        gender_match = gender.lower() in row['Gender'].lower() or 'all' in row['Gender'].lower()
        
        if zip_match and needs_match and insurance_match and language_match and gender_match:
            results.append(row)
    
    return pd.DataFrame(results)

# LLM-based search with OpenAI
def search_resources_llm(zip_code, needs, insurance, language, gender):
    df = load_data()
    if df.empty:
        return pd.DataFrame(), "No resources available due to missing dataset."
    
    prompt = f"""
    You are a health resource navigator for uninsured patients in Austin, TX.
    Given the following patient inputs:
    - ZIP Code: {zip_code}
    - Medical Needs: {needs}
    - Insurance Status: {insurance}
    - Preferred Language: {language}
    - Gender-Specific Services: {gender}
    
    Filter the following resources (in CSV format) to find matching clinics. If no matches are found, generate up to 3 plausible resources in Austin, TX, that fit the criteria, ensuring realistic details (e.g., addresses in Austin, valid ZIP codes like 78701, 78702).
    
    Your response MUST be ONLY valid JSON in the exact format specified below, with no additional text, explanations, or markdown formatting.
    
    Resources:
    {df.to_csv(index=False)}
    
    REQUIRED OUTPUT FORMAT:
    {{
        "resources": [
            {{
                "Resource_Name": "...",
                "Address": "...",
                "Services": "...",
                "Eligibility": "...",
                "Hours": "...",
                "Contact": "...",
                "ZIP_Code": "...",
                "Languages": "...",
                "Gender": "..."
            }}
        ],
        "recommendation": "..." 
    }}
    
    The recommendation should be 50-100 words suggesting next steps or considerations for the patient.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available in your plan
            messages=[
                {"role": "system", "content": "You are a healthcare resource navigator assistant that returns only valid JSON. Your responses must contain nothing but properly formatted JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2500,
            temperature=0.5
        )
        output = response.choices[0].message.content
        
        # Log raw output for debugging
        with open("llm_response_log.txt", "w") as log_file:
            log_file.write(f"Raw response:\n{output}")
        
        # Clean the output to ensure it's valid JSON
        # Remove any markdown code block indicators
        clean_output = re.sub(r'```json|```', '', output).strip()
        
        # Parse the JSON
        parsed = json.loads(clean_output)
        
        resources = parsed.get("resources", [])
        recommendation = parsed.get("recommendation", "No recommendation provided.")
        
        # Convert to DataFrame
        return pd.DataFrame(resources), recommendation
    except Exception as e:
        st.error(f"LLM search failed: {str(e)}. Using current algorithm as fallback.")
        # Log the error and output for debugging
        with open("llm_error_log.txt", "w") as log_file:
            log_file.write(f"Error: {str(e)}\n\nOutput (if available):\n{locals().get('output', 'No output')}")
        return search_resources(df, zip_code, needs, insurance, language, gender), "LLM unavailable; used fuzzy matching."

# Improved scraping for generate_data.py (this doesn't change app.py functionality)
# You would need to make these changes in generate_data.py separately

# Streamlit app
st.title("Personalized Community Resource Navigator")
st.write("Find healthcare resources for uninsured patients in Austin, TX")

# Sidebar
st.sidebar.header("About")
st.sidebar.write("This app helps uninsured patients find community health resources in Austin, TX, tailored to their ZIP code, medical needs, insurance status, language, and gender-specific services. Powered by fuzzy matching and OpenAI LLM for advanced search and insights.")

# Input form
with st.form("search_form"):
    zip_code = st.text_input("ZIP Code", placeholder="e.g., 78701")
    needs = st.text_input("Medical Needs", placeholder="e.g., primary care, dental, mental health")
    insurance = st.selectbox("Insurance Status", ["Uninsured", "Medicaid", "Low-income", "All"])
    language = st.selectbox("Preferred Language", ["English", "Spanish", "Other", "All"])
    gender = st.selectbox("Gender-Specific Services", ["All", "Female-only", "Male-only"])
    
    col1, col2 = st.columns(2)
    with col1:
        current_button = st.form_submit_button("Traditional Search")
    with col2:
        llm_button = st.form_submit_button("AI-Powered Search")

# Load data
df = load_data()

# Process search
if current_button and zip_code and needs:
    results = search_resources(df, zip_code, needs, insurance, language, gender)
    recommendation = "Results based on fuzzy matching algorithm."
elif llm_button and zip_code and needs:
    results, recommendation = search_resources_llm(zip_code, needs, insurance, language, gender)
else:
    results = pd.DataFrame()
    recommendation = ""

# Display results
if not results.empty:
    st.subheader("Matching Resources")
    for _, row in results.iterrows():
        st.write(f"**{row['Resource_Name']}**")
        st.write(f"Address: {row['Address']}")
        st.write(f"Services: {row['Services']}")
        st.write(f"Eligibility: {row['Eligibility']}")
        st.write(f"Hours: {row['Hours']}")
        st.write(f"Contact: {row['Contact']}")
        st.write(f"Languages: {row['Languages']}")
        st.write(f"Gender: {row['Gender']}")
        st.write("---")
else:
    st.warning("No matching resources found. Try adjusting your inputs.")

# Display recommendation
if recommendation:
    st.subheader("Recommendation")
    st.write(recommendation)