import streamlit as st
import subprocess
import threading
import queue
import time

# ------------------------------------------------------------
#  STREAMLIT UI WRAPPER FOR YOUR MIGRATION TOOL
# ------------------------------------------------------------

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

st.title("🚀 Workvivo → Workvivo Migration Tool (UI)")

st.write("""
This interface allows non-technical users to run your migration tool 
**without touching any Python code**.
""")

# ------------------------------------------------------------
#  CONFIG INPUT SECTION
# ------------------------------------------------------------
st.header("🔧 Configuration")

col1, col2 = st.columns(2)

with col1:
    source_api = st.text_input("Source API URL", placeholder="https://api.source.workvivo.com")
    source_key = st.text_input("Source API Key", placeholder="xxxx", type="password")
    source_wv_id = st.text_input("Source Workvivo-Id", placeholder="12345")

with col2:
    target_api = st.text_input("Target API URL", placeholder="https://api.target.workvivo.com")
    target_key = st.text_input("Target API Key", placeholder="xxxx", type="password")
    target_wv_id = st.text_input("Target Workvivo-Id", placeholder="67890")

st.divider()

# ------------------------------------------------------------
#  PHASE PICKER
# ------------------------------------------------------------
st.header("📦 Migration Phases")

phase = st.selectbox(
    "Select a migration phase:",
    [
        "Phase 1 – Users",
        "Phase 1A – Users + Avatars",
        "Phase 1B – Spaces",
        "Phase 1C – Space Role Mapper",
        "Phase 1D – Teams",
        "Phase 2 – Updates + Comments + Likes",
        "Phase 3 – Articles",
        "Phase 4 – Global Pages",
        "Phase 5 – Space Pages",
        "Phase 6 – Events",
        "Phase 7 –
