import streamlit as st
import google.genai as genai
from google.genai import types
import pandas as pd
import json

# Page configurations
st.set_page_config(
    page_title="B2B Lead & SEO Audit Engine",
    page_icon="🎯",
    layout="wide"
)

# Application Header
st.title("🎯 B2B Lead & SEO Audit Engine")
st.subheader("Micro-SaaS Prototype: Automated Data Aggregation & Compliance")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ API Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.markdown("---")
    st.markdown("### 💰 Asset Valuation Data")
    st.metric(label="Target Acquisition Value", value="$1,200")
    st.markdown("**Target Audience:** Agencies, B2B Growth Teams")
    st.markdown("**Engine State:** Stateless / Cloud-Ready")

# Helper function for Gemini audit generation
def generate_audit_report(target_site, business_type, api_key):
    try:
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are an expert B2B growth engineer and technical SEO auditor. "
            "Analyze the target site and business type. Identify critical SEO deficiencies and lead acquisition opportunities. "
            "You MUST reply ONLY with a valid JSON object containing two main keys: 'seo_deficiencies' (array of objects) and 'lead_strategies' (array of objects). "
            "Do not include markdown code blocks or wrapping. "
            "SEO objects must contain keys: 'issue', 'impact', 'fix'. "
            "Lead strategy objects must contain keys: 'strategy', 'target_persona', 'expected_roi'."
        )
        
        prompt = f"Run a diagnostic audit for business type: {business_type} targeting domain: {target_site}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception as e:
        st.error(f"Gemini API Error: {str(e)}")
        return None

# Main UI Layout
st.markdown("### 1. Configuration Workspace")
col1, col2 = st.columns(2)
with col1:
    target_domain = st.text_input("Target Domain:", placeholder="e.g., localdentalclinic.com")
with col2:
    biz_type = st.text_input("Business Category:", placeholder="e.g., Medical / Dental Practice")

# Conditional logic: Show Sandbox data if inputs are empty
if not target_domain or not biz_type:
    st.info("💡 Prototyping Mode: Displaying built-in sandbox mock data below. Fill in the fields above to run a custom analysis.")
    st.markdown("---")
    st.markdown("### 2. Strategic Audit & Lead Intelligence (Sandbox View)")
    
    st.markdown("#### 🔍 Technical SEO Deficiencies")
    mock_seo = pd.DataFrame([
        {"issue": "Missing Schema.org Structured Data Markup", "impact": "High - Prevents rich snippets in search results", "fix": "Inject localized dental practice JSON-LD schema into the homepage header."},
        {"issue": "Unoptimized Core Web Vitals (LCP > 3.4s)", "impact": "Medium - De-prioritizes mobile ranking metrics", "fix": "Compress next-gen image assets and defer non-critical render-blocking JS."}
    ])
    st.dataframe(mock_seo, use_container_width=True)
    
    st.markdown("#### 📈 High-Conversion Lead Capture Strategies")
    mock_leads = pd.DataFrame([
        {"strategy": "Hyper-local B2B Partner Outreach Campaign", "target_persona": "Local Corporate HR Managers", "expected_roi": "Estimated 4.5x via corporate dental benefits packages"},
        {"strategy": "Intent-Based Lead Magnet Conversion Funnel", "target_persona": "High-intent local patients searching emergency care", "expected_roi": "Estimated 22% lift in direct appointment bookings"}
    ])
    st.dataframe(mock_leads, use_container_width=True)
else:
    st.markdown("---")
    st.markdown("### 2. Strategic Audit & Lead Intelligence (Live Engine)")
    if st.button("⚡ Run Live Engine Diagnostic"):
        if not api_key:
            st.warning("Please enter your Gemini API key in the sidebar to execute a live context audit computation.")
        else:
            with st.spinner("Compiling contextual data fields via Gemini 2.5-Flash..."):
                raw_json = generate_audit_report(target_domain, biz_type, api_key)
                
                if raw_json:
                    try:
                        clean_json = raw_json.strip().strip("```json").strip("```")
                        data = json.loads(clean_json)
                        
                        st.success("🎉 Comprehensive Lead & SEO Diagnostic Complete!")
                        
                        st.markdown("#### 🔍 Technical SEO Deficiencies")
                        st.dataframe(pd.DataFrame(data.get('seo_deficiencies', [])), use_container_width=True)
                        
                        st.markdown("#### 📈 High-Conversion Lead Capture Strategies")
                        st.dataframe(pd.DataFrame(data.get('lead_strategies', [])), use_container_width=True)
                        
                    except Exception as e:
                        st.error("Failed to cleanly parse structured engine response. Please re-trigger the diagnostic.")
