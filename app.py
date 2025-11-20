import streamlit as st

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

st.title("🚀 Workvivo Migration Tool")
st.write("Fill in your Source & Target credentials below to unlock migration options.")

# ===============================
# SECTION 1 — AUTHENTICATION INPUTS
# ===============================
st.header("🔐 Source & Target Configuration")

with st.container():
    st.subheader("📥 Source System Credentials")

    source_api_url = st.text_input("Source API Base URL", placeholder="https://api.workvivo.com/v1")
    source_token = st.text_input("Source API Token", type="password")
    source_wvid = st.text_input("Source Workvivo-ID", placeholder="Required for Kudos")

    st.subheader("📤 Target System Credentials")

    target_api_url = st.text_input("Target API Base URL", placeholder="https://api.workvivo.com/v1")
    target_token = st.text_input("Target API Token", type="password")
    target_wvid = st.text_input("Target Workvivo-ID", placeholder="Required for Kudos")

st.markdown("---")

# ===============================
# SECTION 2 — MIGRATION SETTINGS
# ===============================
st.header("⚙️ Migration Settings")

migration_user_ext = st.text_input("Migration User External ID (used when no creator found)")
global_space_id = st.text_input("Global Space ID (fallback for articles, kudos, updates)")

# Button is disabled until required fields are complete
credentials_ready = all([
    source_api_url, source_token, target_api_url, target_token,
    migration_user_ext, global_space_id
])

if not credentials_ready:
    st.warning("⚠️ Fill in all required fields above to unlock migration phases.")

st.markdown("---")

# ===============================
# SECTION 3 — MIGRATION PHASE SELECTOR
# ===============================
st.header("📦 Migration Phases")

if credentials_ready:
    phase = st.selectbox(
        "Choose a migration phase:",
        [
            "Phase 1 — Users & Spaces",
            "Phase 2 — Updates & Comments",
            "Phase 3 — Articles",
            "Phase 4 — Global Pages",
            "Phase 5 — Space Pages",
            "Phase 6 — Events",
            "Phase 7 — Kudos",
        ]
    )

    st.success(f"Selected: **{phase}**")
    
    st.write("⬇️ When your migration functions are added, the button below will trigger them.")

    if st.button("Run Migration"):
        st.info("Migration would start here. Function hooks not yet connected.")
else:
    st.stop()

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("Workvivo Migration Tool — Streamlit UI Prototype")
