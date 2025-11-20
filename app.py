import streamlit as st

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")
st.title("🚀 Workvivo Migration Tool")

st.markdown("---")

# =========================================================
# CONFIGURATION INPUTS
# =========================================================

st.header("🔐 Configuration — Source & Target Environments")

with st.expander("📥 Source Environment", expanded=True):
    SOURCE_SCIM_URL = st.text_input("Source SCIM URL")
    SOURCE_API_URL = st.text_input("Source API URL")
    SOURCE_SCIM_TOKEN = st.text_input("Source SCIM Token", type="password")
    SOURCE_API_TOKEN = st.text_input("Source API Token", type="password")
    SOURCE_WORKVIVO_ID = st.text_input("Source Workvivo-Id Header")

with st.expander("📤 Target Environment", expanded=True):
    TARGET_SCIM_URL = st.text_input("Target SCIM URL")
    TARGET_API_URL = st.text_input("Target API URL")
    TARGET_SCIM_TOKEN = st.text_input("Target SCIM Token", type="password")
    TARGET_API_TOKEN = st.text_input("Target API Token", type="password")
    TARGET_WORKVIVO_ID = st.text_input("Target Workvivo-Id Header")

with st.expander("⚙️ Additional Settings", expanded=True):
    SPACE_CREATOR_EXTERNAL_ID = st.text_input(
        "Space Creator External ID",
        placeholder="workvivo-migration-user"
    )

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
    st.warning("⚠️ Fill out all fields to continue.")
    st.stop()

st.success("✔️ Configuration Loaded Successfully")
st.markdown("---")

# =========================================================
# PHASE SELECTOR
# =========================================================
st.header("📦 Select Migration Phase")

phase_choice = st.radio(
    "Choose a migration phase:",
    ["Phase 1 — Users / Spaces / Members", 
     "Phase 2 — Updates / Comments / Likes / Articles / Kudos"]
)

st.markdown("---")

# =========================================================
# PHASE ACTIONS
# =========================================================

if phase_choice.startswith("Phase 1"):
    st.subheader("Phase 1 Options")
    
    if st.button("▶️ Migrate Users"):
        st.info("Running `migrate_users()`…")
        # CALL FUNCTION HERE: migrate_users()

    if st.button("🖼️ Migrate User Avatars"):
        st.info("Running `migrate_user_images()`…")
        # CALL FUNCTION HERE: migrate_user_images()

    if st.button("🏛️ Migrate Spaces"):
        st.info("Running `migrate_spaces()`…")
        # CALL FUNCTION HERE: migrate_spaces()

    if st.button("👥 Migrate Space Memberships"):
        st.info("Running `migrate_memberships()`…")
        # CALL FUNCTION HERE: migrate_memberships()


elif phase_choice.startswith("Phase 2"):
    st.subheader("Phase 2 Options")

    if st.button("⬆️ Migrate Updates"):
        st.info("Would run Phase 2 — Updates")
        # migrate_updates()

    if st.button("💬 Migrate Comments"):
        st.info("Would run Phase 2 — Comments")
        # migrate_comments()

    if st.button("❤️ Migrate Likes"):
        st.info("Would run Phase 2 — Likes")
        # migrate_likes()

    if st.button("📰 Migrate Articles"):
        st.info("Would run Phase 2 — Articles")
        # migrate_articles()

    if st.button("🏅 Migrate Kudos"):
        st.info("Would run Phase 2 — Kudos")
        # migrate_kudos()

st.markdown("---")
st.caption("Workvivo Migration Tool — Streamlit Edition")
