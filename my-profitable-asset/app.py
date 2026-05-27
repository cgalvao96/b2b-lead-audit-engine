import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import time
st.set_page_config(page_title="B2B Lead Engine", layout="centered")
st.title("B2B Lead & SEO Audit Engine")
target_url = st.text_input("Enter business website URL:")
max_links_to_check = st.slider("Max internal links to audit:", 5, 50, 20)
def audit_website(base_url, max_links):
    found_links = set()
    audited_results = []
    marketing_tags = {"Meta/FB Pixel": ["connect.facebook.net", "fbpixel"], "Google Analytics": ["googletagmanager.com", "google-analytics.com"], "TikTok Pixel": ["://tiktok.com"]}
    detected_marketing = {k: False for k in marketing_tags}
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(base_url, headers=headers, timeout=10)
        html_content = res.text
        soup = BeautifulSoup(html_content, "html.parser")
        for name, footprints in marketing_tags.items():
            if any(f in html_content.lower() for f in footprints):
                detected_marketing[name] = True
        domain = urlparse(base_url).netloc
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            absolute_url = urljoin(base_url, href)
            if urlparse(absolute_url).netloc == domain and absolute_url not in found_links:
                found_links.add(absolute_url)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None
    progress_bar = st.progress(0)
    links_list = list(found_links)
    for idx, link in enumerate(links_list):
        time.sleep(0.1)
        try:
            status_check = requests.head(link, headers=headers, timeout=5, allow_redirects=True)
            status_code = status_check.status_code
        except: status_code = "Failed"
        status_msg = "?? Functional (200)" if status_code == 200 else f"?? Broken ({status_code})"
        audited_results.append({"Page URL": link, "Status": status_msg})
        progress_bar.progress((idx + 1) / len(links_list))
    return audited_results, detected_marketing
if st.button("Run Audit Strategy", type="primary"):
    if not target_url: st.warning("Please enter a URL.")
    else:
        if not target_url.startswith("http"): target_url = "https://" + target_url
        with st.spinner("Analyzing code infrastructure..."):
            audit_report, marketing_report = audit_website(target_url, max_links_to_check)
            if audit_report:
                st.success("Audit Completed!")
                st.subheader("?? Marketing Tech Fingerprint")
                for pixel, status in marketing_report.items():
                    if status: st.write(f"? **{pixel}:** Installed")
                    else: st.write(f"?? **{pixel}:** **MISSING** (High-Value Pitch Angle!)")
                st.subheader("?? Crawled Link Health")
                df = pd.DataFrame(audit_report)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button(label="?? Download Lead Audit Sheet (.CSV)", data=df.to_csv(index=False), file_name="website_lead_audit.csv", mime="text/csv")
