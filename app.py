import streamlit as st

st.set_page_config(page_title="Workvivo Migration Tool – Phase 1", layout="wide")

st.title("🚀 Workvivo Migration Tool")
st.subheader("Phase 1 — Users, Avatars, Spaces & Memberships")

st.markdown("---")

# ======================================================
# SECTION 1 — CONFIGURATION INPUTS (EMPTY BY DEFAULT)
# ======================================================
st.header("🔐 Configuration — Source & Target Environments")

with st.expander("📥 Source Workvivo Environment", expanded=True):
    SOURCE_SCIM_URL = st.text_input(
        "Source SCIM URL",
        placeholder="https://<tenant>.workvivo.com/scim/v2/scim/Users/"
    )
    SOURCE_API_URL = st.text_input(
        "Source API URL",
        placeholder="https://api.workvivo.com/v1"
    )
    SOURCE_SCIM_TOKEN = st.text_input(
        "Source SCIM Token",
        value="",
        type="password",
        placeholder="Enter source SCIM token"
    )
    SOURCE_API_TOKEN = st.text_input(
        "Source API Token",
        value="",
        type="password",
        placeholder="Enter source API token"
    )
    SOURCE_WORKVIVO_ID = st.text_input(
        "Source Workvivo-Id Header",
        placeholder="e.g. 50"
    )

with st.expander("📤 Target Workvivo Environment", expanded=True):
    TARGET_SCIM_URL = st.text_input(
        "Target SCIM URL",
        placeholder="https://<tenant>.workvivo.com/scim/v2/scim/Users/"
    )
    TARGET_API_URL = st.text_input(
        "Target API URL",
        placeholder="https://api.<region>.workvivo.com/v1"
    )
    TARGET_SCIM_TOKEN = st.text_input(
        "Target SCIM Token",
        value="",
        type="password",
        placeholder="Enter target SCIM token"
    )
    TARGET_API_TOKEN = st.text_input(
        "Target API Token",
        value="",
        type="password",
        placeholder="Enter target API token"
    )
    TARGET_WORKVIVO_ID = st.text_input(
        "Target Workvivo-Id Header",
        placeholder="e.g. 3000384"
    )

with st.expander("⚙️ Additional Settings", expanded=True):
    SPACE_CREATOR_EXTERNAL_ID = st.text_input(
        "Space Creator External ID (must exist on target)",
        placeholder="workvivo-migration-user"
    )

st.markdown("---")

# ======================================================
# VALIDATION
# ======================================================

required = [
    SOURCE_SCIM_URL, SOURCE_API_URL,
    SOURCE_SCIM_TOKEN, SOURCE_API_TOKEN,
    SOURCE_WORKVIVO_ID,
    TARGET_SCIM_URL, TARGET_API_URL,
    TARGET_SCIM_TOKEN, TARGET_API_TOKEN,
    TARGET_WORKVIVO_ID,
    SPACE_CREATOR_EXTERNAL_ID,
]

if not all(required):
    st.warning("⚠️ Please enter ALL required configuration fields to unlock migration actions.")
    st.stop()

st.success("✔️ Configuration complete — You can now run Phase 1 migrations.")

st.markdown("---")

# ======================================================
# SECTION 2 — PHASE 1 ACTIONS
# ======================================================

st.header("📦 Phase 1 — Migration Actions")

st.write("""
Choose which operation you want to run.  
The actual migration functions will be connected after the UI is approved.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Migrate Users (SCIM)"):
        st.info("👉 Users migration would run now (function not yet wired).")

    if st.button("🖼️ Migrate User Avatars"):
        st.info("👉 User avatars migration would run now (function not yet wired).")

with col2:
    if st.button("🏛️ Migrate Spaces"):
        st.info("👉 Spaces migration would run now (function not yet wired).")

    if st.button("👥 Migrate Space Memberships"):
        st.info("👉 Membership migration would run now (function not yet wired).")

st.markdown("---")

st.caption("Workvivo Migration Tool — Streamlit UI Prototype (Phase 1 Only)")
