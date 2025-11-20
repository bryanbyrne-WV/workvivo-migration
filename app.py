import streamlit as st

st.set_page_config(
    page_title="Workvivo Migration Tool",
    layout="wide",
)

# ---------------------------------------------------------
# Placeholder migration functions
# Replace these with your actual migration code
# ---------------------------------------------------------

def run_phase1():
    st.info("Running Phase 1: Users, Spaces, Memberships...")
    # call your real code here

def run_phase1a():
    st.info("Running Phase 1A: Users + Avatars...")
    # call your real code here

def run_phase1b():
    st.info("Running Phase 1B: Spaces + Memberships...")
    # call your real code here

def run_phase2_updates():
    st.info("Running Phase 2A: Updates migration...")
    # call your real code here

def run_phase2_comments():
    st.info("Running Phase 2B: Comments migration...")
    # call your real code here

def run_phase2_likes():
    st.info("Running Phase 2C: Likes migration...")
    # call your real code here

def run_phase3_articles():
    st.info("Running Phase 3: Articles migration...")
    # call your real code here

def run_phase4_global_pages():
    st.info("Running Phase 4: Global Pages Migration...")
    # call your real code here

def run_phase5_space_pages():
    st.info("Running Phase 5: Space Pages Migration...")
    # call your real code here

def run_phase6_events():
    st.info("Running Phase 6: Events Migration...")
    # call your real code here

def run_phase7_kudos():
    st.info("Running Phase 7: Kudos Migration...")
    # call your real code here


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------

st.title("🚀 Workvivo Migration Tool")
st.markdown("A simple interface to run migration phases without touching Python code.")

st.sidebar.title("Navigation")

phase = st.sidebar.selectbox(
    "Select Migration Phase",
    [
        "Phase 1 - Users / Spaces / Memberships",
        "Phase 1A - Users + Avatars",
        "Phase 1B - Spaces + Memberships",
        "Phase 2A - Updates",
        "Phase 2B - Comments",
        "Phase 2C - Likes",
        "Phase 3 - Articles",
        "Phase 4 - Global Pages",
        "Phase 5 - Space Pages",
        "Phase 6 - Events",
        "Phase 7 - Kudos",
    ]
)

st.write("---")

# Display phase description
phase_descriptions = {
    "Phase 1 - Users / Spaces / Memberships": "Full user + space migration.",
    "Phase 1A - Users + Avatars": "User migration only (with avatars).",
    "Phase 1B - Spaces + Memberships": "Space migration only.",
    "Phase 2A - Updates": "Stage 1 of content migration.",
    "Phase 2B - Comments": "Stage 2 of content migration.",
    "Phase 2C - Likes": "Stage 3 of content migration.",
    "Phase 3 - Articles": "Article migration including comments + likes.",
    "Phase 4 - Global Pages": "Global pages (top-level) migration.",
    "Phase 5 - Space Pages": "Pages within spaces.",
    "Phase 6 - Events": "Events, RSVP data, etc.",
    "Phase 7 - Kudos": "Kudos (Recognitions) migration.",
}

st.subheader("📘 " + phase)
st.markdown(phase_descriptions.get(phase, ""))

st.write("---")

# Run the appropriate function when the user clicks "Run"
if st.button("Run Migration", type="primary"):
    st.success("Migration started... check the output below.")

    if phase == "Phase 1 - Users / Spaces / Memberships":
        run_phase1()
    elif phase == "Phase 1A - Users + Avatars":
        run_phase1a()
    elif phase == "Phase 1B - Spaces + Memberships":
        run_phase1b()
    elif phase == "Phase 2A - Updates":
        run_phase2_updates()
    elif phase == "Phase 2B - Comments":
        run_phase2_comments()
    elif phase == "Phase 2C - Likes":
        run_phase2_likes()
    elif phase == "Phase 3 - Articles":
        run_phase3_articles()
    elif phase == "Phase 4 - Global Pages":
        run_phase4_global_pages()
    elif phase == "Phase 5 - Space Pages":
        run_phase5_space_pages()
    elif phase == "Phase 6 - Events":
        run_phase6_events()
    elif phase == "Phase 7 - Kudos":
        run_phase7_kudos()

st.write("---")
st.info("Tip: Logs and output will appear here once the backend functions are wired in.")
