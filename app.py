import streamlit as st
import os
import time
import requests

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

st.title("🚀 Workvivo Migration Tool")
st.write("Run internal migrations without touching Python scripts.")

# =====================================================================
# 1) ENVIRONMENT CONFIGURATION
# =====================================================================

with st.form("config_form"):

    st.header("🔐 Environment Configuration")
    st.subheader("Source Workvivo Environment")

    SOURCE_SCIM_URL = st.text_input(
        "Source SCIM URL",
        value="https://workvivo.workvivo.com/scim/v2/scim/Users/"
    )

    SOURCE_API_URL = st.text_input(
        "Source API URL",
        value="https://api.workvivo.com/v1"
    )

    SOURCE_SCIM_TOKEN = st.text_input(
        "Source SCIM Token",
        value="Yz1Pj7m6MOGPRmhkbpzGI85VxsCW8WdvCKFBIVcj",
        type="password"
    )

    SOURCE_API_TOKEN = st.text_input(
        "Source API Token",
        value="357|a6ad24b87add478518ae2fa2d1ff67d9a1040bf6",
        type="password"
    )

    SOURCE_WORKVIVO_ID = st.text_input(
        "Source Workvivo-ID",
        value="50"
    )

    st.subheader("Target Workvivo Environment")

    TARGET_SCIM_URL = st.text_input(
        "Target SCIM URL",
        value="https://migration-test-1.workvivo.com/scim/v2/scim/Users/"
    )

    TARGET_API_URL = st.text_input(
        "Target API URL",
        value="https://api.eu2.workvivo.com/v1"
    )

    TARGET_SCIM_TOKEN = st.text_input(
        "Target SCIM Token",
        value="nLgLGVnMHaYySx9DqCixkHx0lUZqgxTGwT7RyKMj",
        type="password"
    )

    TARGET_API_TOKEN = st.text_input(
        "Target API Token",
        value="1006|fb9c50816d6db9f14163146b8205538bdb3264e5",
        type="password"
    )

    TARGET_WORKVIVO_ID = st.text_input(
        "Target Workvivo-ID",
        value="3000384"
    )

    SPACE_CREATOR_EXTERNAL_ID = st.text_input(
        "Migration External ID (Space Creator)",
        value="workvivo-migration-user"
    )

    submitted = st.form_submit_button("Save Configuration")

if not submitted:
    st.stop()

# Validate all fields
required = [
    SOURCE_SCIM_URL, SOURCE_API_URL, SOURCE_SCIM_TOKEN, SOURCE_API_TOKEN, SOURCE_WORKVIVO_ID,
    TARGET_SCIM_URL, TARGET_API_URL, TARGET_SCIM_TOKEN, TARGET_API_TOKEN, TARGET_WORKVIVO_ID,
    SPACE_CREATOR_EXTERNAL_ID,
]

if not all(required):
    st.error("❌ All fields above must be filled before proceeding.")
    st.stop()

st.success("✅ Environment configuration loaded.")

# -------------------------------------------------------
# 📌 PHASE 1 Placeholder
# -------------------------------------------------------
# ===============================================================
# Phase 1 — Users
# ===============================================================
# ===============================================================
# STREAMLIT LOGGING SUPPORT
# ===============================================================
import io
from datetime import datetime

log_buffer = io.StringIO()

def ui_log(message):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {message}"
    log_buffer.write(line + "\n")
    st.text(line)


# ===============================================================
# STREAMLIT-SAFE USER MIGRATION
# ===============================================================
def migrate_users_streamlit(active_only, log):
    log("=== USER MIGRATION START ===")
    all_users = []
    start_index = 1
    count = 100

    log(f"🔍 Migrating {'active only' if active_only else 'all'} users from source...")

    # Prefetch existing target users
    existing_emails = set()
    existing_external_ids = set()
    skip = 0
    count = 100

    log("🔄 Checking existing users on target to avoid duplicates...")
    while True:
        target_url = f"{TARGET_SCIM_URL}?startIndex={skip}&count={count}"
        resp_tgt = requests.get(target_url, headers=target_scim_headers, verify=VERIFY_SSL)
        if resp_tgt.status_code != 200:
            log(f"⚠️ Could not prefetch target users: {resp_tgt.status_code}")
            break

        data_tgt = resp_tgt.json().get("Resources", [])
        if not data_tgt:
            break

        for tu in data_tgt:
            email_tgt = tu.get("userName", "").strip().lower()
            ext_tgt = tu.get("externalId", "").strip().upper()
            if email_tgt: existing_emails.add(email_tgt)
            if ext_tgt: existing_external_ids.add(ext_tgt)

        if len(data_tgt) < count:
            break

        skip += count
        time.sleep(DEFAULT_SLEEP)

    log(f"✅ Found {len(existing_emails)} emails and {len(existing_external_ids)} externalIds on target.")

    # Fetch users from source
    while True:
        if active_only:
            url = f"{SOURCE_SCIM_URL}?filter=active eq true&startIndex={start_index}&count={count}"
        else:
            url = f"{SOURCE_SCIM_URL}?startIndex={start_index}&count={count}"

        resp = requests.get(url, headers=source_scim_headers, verify=VERIFY_SSL)

        if resp.status_code != 200:
            log(f"❌ Failed to fetch users: {resp.status_code}")
            break

        data = resp.json()
        users = data.get("Resources", [])
        all_users.extend(users)
        total = int(data.get("totalResults", 0))

        log(f"📥 Fetched {len(users)} users (total so far: {len(all_users)})")

        if start_index + count > total:
            break

        start_index += count
        time.sleep(DEFAULT_SLEEP)

    migrated = skipped = errors = 0

    # Process each user
    for u in all_users:
        ext = u.get("externalId")
        email = u.get("userName", "").strip().lower()

        name_obj = u.get("name", {}) or {}
        first_name = name_obj.get("givenName", "").strip()
        last_name = name_obj.get("familyName", "").strip()

        # Skip missing names
        if not first_name or not last_name:
            skipped += 1
            log(f"⚠️ Skipped {email}: missing first/last name")
            continue

        # Skip missing email
        if not email:
            skipped += 1
            log(f"⚠️ Skipped user (missing email) external_id={ext}")
            continue

        # Check duplicates
        if email in existing_emails:
            skipped += 1
            log(f"⚠️ Skipped {email}: email already on target")
            continue

        if ext and ext.strip().upper() in existing_external_ids:
            skipped += 1
            log(f"⚠️ Skipped {email}: externalId already on target")
            continue

        # Build SCIM payload
        payload = {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User",
                "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
            ],
            "userName": email,
            "name": u.get("name", {}),
            "active": u.get("active", True),
        }

        # Handle missing externalId
        if not ext or not isinstance(ext, str) or not ext.strip():
            ext = f"WV-MIG-AUTO-{random.randint(10000000,99999999)}"
            log(f"🪪 Generated fallback externalId {ext} for {email}")

        payload["externalId"] = ext

        # Add job title
        job_title = (
            u.get("title") or 
            u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}).get("title")
        )
        if job_title and isinstance(job_title, str):
            payload["title"] = job_title.strip()

        # Enterprise extension
        enterprise_ext = {}

        legacy_id = u.get("legacy_system_id")
        if not legacy_id:
            legacy_id = f"wm-mig-{random.randint(100000000000, 999999999999)}"

        enterprise_ext["legacy_system_id"] = legacy_id

        # Manager
        manager_info = u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}).get("manager") or {}
        if manager_info.get("value"):
            enterprise_ext["manager"] = {
                "displayName": manager_info.get("displayName", ""),
                "value": manager_info.get("value").strip()
            }

        # Optional fields
        enterprise_src = u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}) or {}
        if enterprise_src.get("hireDate"):
            enterprise_ext["hireDate"] = enterprise_src.get("hireDate")
        if enterprise_src.get("dateOfBirth"):
            enterprise_ext["dateOfBirth"] = enterprise_src.get("dateOfBirth")

        if enterprise_ext:
            payload["urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"] = enterprise_ext

        resp = requests.post(TARGET_SCIM_URL, headers=target_scim_headers, json=payload, verify=VERIFY_SSL)

        if resp.status_code in [200, 201]:
            migrated += 1
            log(f"✅ Created user {ext}")
            continue

        if resp.status_code == 409:
            skipped += 1
            log(f"⚠️ Duplicate user skipped → {email}")
            continue

        errors += 1
        log(f"❌ Error creating {email}: {resp.status_code} {resp.text[:200]}")

    log(f"=== USER MIGRATION END ===")
    log(f"Summary → Migrated={migrated}, Skipped={skipped}, Errors={errors}")


# ===============================================================
# Phase 1A — User Images (UI Logging Only)
# ===============================================================
def migrate_user_images():
    ui_log("=== USER IMAGE MIGRATION START ===")
    users = paginated_fetch(f"{SOURCE_API_URL}/users", source_headers)

    for u in users:
        ext = normalize_external_id(u.get("external_id"))
        src_url = u.get("avatar_url")

        if not ext or not src_url:
            continue

        file_path = download_file(src_url, f"user_{ext}.jpg")
        if not file_path:
            ui_log(f"⚠️ Failed to download avatar for {ext}")
            continue

        success = upload_user_avatar(ext, file_path)
        if success:
            ui_log(f"🖼️ Uploaded avatar for {ext}")

    ui_log("=== USER IMAGE MIGRATION END ===")


# ===============================================================
# Phase 1 — Spaces + Memberships (unchanged except UI logs)
# ===============================================================
def migrate_spaces():
    ui_log("=== SPACE MIGRATION START ===")
    # (Your existing migrate_spaces code here, replace log() with ui_log())
    ui_log("=== SPACE MIGRATION END ===")

def migrate_memberships():
    ui_log("=== MEMBERSHIP MIGRATION START ===")
    # (Your existing migrate_memberships code here, replace log() with ui_log())
    ui_log("=== MEMBERSHIP MIGRATION END ===")


# ===============================================================
# RUN PHASE 1 (Streamlit)
# ===============================================================
def run_phase_1(company_name, active_only):

    log = ui_log  # unify logging

    log("▶️ Starting Phase 1...")

    # GLOBAL SPACE
    create_global_space_and_enroll(company_name)

    # USERS
    migrate_users_streamlit(active_only, log)

    # IMAGES
    migrate_user_images()

    # SPACES
    migrate_spaces()

    # MEMBERSHIPS
    migrate_memberships()

    log("✅ Phase 1 Completed Successfully!")


# -------------------------------------------------------
# 📌 PHASE 2 Placeholder
# -------------------------------------------------------
def run_phase_2():
    """
    🔹 Updates
    🔹 Comments
    🔹 Likes
    """
    st.write("Running Phase 2...")
    time.sleep(1)
    st.write("✅ Phase 2 completed (placeholder).")

# -------------------------------------------------------
# 📌 PHASE 3 Placeholder
# -------------------------------------------------------
def run_phase_3(selected_modules):
    """Article / Kudos / Events migration."""
    st.write(f"Running Phase 3 modules: {selected_modules}")
    time.sleep(1)
    st.write("✅ Phase 3 completed (placeholder).")

# =====================================================================
# 3) MIGRATION PHASE SELECTION
# =====================================================================

st.header("🔧 Run Migration")

phase = st.selectbox(
    "Choose migration phase",
    ["Phase 1 – Users, Avatars, Spaces, Memberships",
     "Phase 2 – Updates, Comments, Likes",
     "Phase 3 – Articles, Kudos, Events"]
)

# ------------------------------
# Phase 1 – no options
# ------------------------------
if phase.startswith("Phase 1"):

    st.subheader("Phase 1 Options")

    company_name = st.text_input(
        "🏢 Company Name (for Global Space Creation)",
        placeholder="e.g. Workvivo"
    )

    active_choice = st.radio(
        "Which users to migrate?",
        ["Active Only", "All Users"]
    )
    active_only = (active_choice == "Active Only")

    if st.button("▶ Run Phase 1"):
        if not company_name:
            st.error("❌ Please enter a Company Name before running Phase 1.")
        else:
            run_phase_1(company_name, active_only)
            st.success("Phase 1 finished!")

# ------------------------------
# Phase 2 – no options
# ------------------------------
elif phase.startswith("Phase 2"):
    if st.button("▶ Run Phase 2"):
        run_phase_2()

# ------------------------------
# Phase 3 – user selects modules
# ------------------------------
else:
    st.subheader("Select content to migrate")
    modules = st.multiselect(
        "Choose modules to run",
        ["Articles", "Kudos", "Events"],
        default=["Articles"]
    )

    if st.button("▶ Run Phase 3"):
        run_phase_3(modules)
