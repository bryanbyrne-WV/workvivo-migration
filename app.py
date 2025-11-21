
# -*- coding: utf-8 -*-
import streamlit as st
import requests
import time
import io
from datetime import datetime
import random
import os
import mimetypes

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

# ============================================================
# WORKVIVO ADVANCED UI THEME + LOADING + BUTTONS + DARK-MODE
# ============================================================
WORKVIVO_LOGO = "/mnt/data/wv.png"

advanced_styles = f"""
<style>

    /* GLOBAL PAGE BACKGROUND */
    .main {{
        background-color: #F7F9FC !important;
    }}

    /* DARK MODE SUPPORT */
    @media (prefers-color-scheme: dark) {{
        .main {{
            background-color: #0d1117 !important;
        }}
        .header-bar {{
            background-color: #3d0199 !important;
        }}
        .header-title {{
            color: #ffffff !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #1a0638 !important;
        }}
        .sidebar-link {{
            color: #cbd5e1 !important;
        }}
        .sidebar-footer {{
            color: #94a3b8 !important;
        }}
    }}

    /* HEADER BAR */
    .header-bar {{
        background-color: #6203ed;
        padding: 18px 28px;
        width: 100%;
        display: flex;
        align-items: center;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.18);
        animation: fade-slide-down 0.6s ease-out;
    }}

    .header-logo {{
        height: 46px;
        margin-right: 18px;
    }}

    .header-title {{
        color: white;
        font-size: 30px;
        font-weight: 650;
        letter-spacing: -0.5px;
        margin-top: 2px;
    }}

    @keyframes fade-slide-down {{
        0% {{ opacity: 0; transform: translateY(-10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background-color: #4502b4 !important;
        padding: 20px 15px;
    }}

    .sidebar-logo {{
        width: 170px;
        margin-bottom: 20px;
        margin-top: 10px;
        animation: fade-in 0.8s;
    }}

    @keyframes fade-in {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}

    .sidebar-title {{
        color: #ffffff;
        font-size: 20px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 10px;
    }}

    .sidebar-link {{
        color: #ffffff !important;
        padding: 10px 6px;
        display: block;
        font-size: 17px;
        font-weight: 500;
        border-radius: 5px;
        margin-bottom: 6px;
        text-decoration: none !important;
        transition: 0.2s;
    }}

    .sidebar-link:hover {{
        background-color: rgba(255,255,255,0.18);
        padding-left: 12px;
    }}

    .sidebar-footer {{
        margin-top: 40px;
        padding: 12px;
        border-top: 1px solid rgba(255,255,255,0.25);
        color: #d0d8e8;
        font-size: 14px;
        text-align: center;
        line-height: 1.4;
    }}

    /* BEAUTIFUL BUTTONS */
    .stButton > button {{
        border-radius: 6px;
        height: 48px;
        background-color: #6203ed;
        border: none;
        color: white;
        font-size: 17px;
        font-weight: 550;
        padding: 8px 20px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        background-color: #4c02b5;
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        transform: scale(0.98);
    }}

    /* COLLAPSIBLE LOG CONTAINER */
    details {{
        background: #ffffff;
        border-radius: 8px;
        padding: 10px 14px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.12);
        margin-bottom: 10px;
    }}

    summary {{
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        color: #6203ed;
        padding: 6px;
    }}

    /* LOADING SPINNER */
    .loading {{
        border: 5px solid #e3e3e3;
        border-top: 5px solid #6203ed;
        border-radius: 50%;
        width: 38px;
        height: 38px;
        animation: spin 0.8s linear infinite;
        margin: auto;
    }}

    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

</style>
"""

st.markdown(advanced_styles, unsafe_allow_html=True)

# Render Header
st.markdown(f"""
<div class="header-bar">
    <img src="{WORKVIVO_LOGO}" class="header-logo">
    <div class="header-title">Workvivo Migration Tool</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        f"""<img src="{WORKVIVO_LOGO}" class="sidebar-logo">""",
        unsafe_allow_html=True
    )

    st.markdown("""<div class="sidebar-title">Navigation</div>""", unsafe_allow_html=True)

    # CONFIGURATION
    st.markdown(
        """<a class="sidebar-link" href="#_config">Configuration</a>""",
        unsafe_allow_html=True
    )

    # DATA MIGRATION (covers Phase 1 + Phase 2 + Phase 3)
    st.markdown(
        """<a class="sidebar-link" href="#_migration">📦 Data Migration</a>""",
        unsafe_allow_html=True
    )

    # LOGS
    st.markdown(
        """<a class="sidebar-link" href="#_logs">📜 Logs</a>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div class="sidebar-footer">Built for internal Workvivo migrations<br>© Bryan Byrne</div>""",
        unsafe_allow_html=True
    )



st.title("🚀 Workvivo Migration Tool")
st.write("Run internal Workvivo migrations without touching Python scripts.")

# =========================================================
# 1) CONFIG FORM (SHOWN ONLY IF NOT SAVED)
# =========================================================
st.markdown("<div id='_config'></div>", unsafe_allow_html=True)

if "config_saved" not in st.session_state:

    with st.form("config_form"):
        st.header("🔐 Environment Configuration")

        st.subheader("Source Environment")
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
        SOURCE_WORKVIVO_ID = st.text_input("Source Workvivo-ID", value="50")

        st.subheader("Target Environment")
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
        TARGET_WORKVIVO_ID = st.text_input("Target Workvivo-ID", value="3000384")

        SPACE_CREATOR_EXTERNAL_ID = st.text_input(
            "Migration External ID (Space Creator)",
            value="workvivo-migration-user"
        )

        submitted = st.form_submit_button("Save Configuration")

    if submitted:
        # Save everything into session state
        st.session_state["config_saved"] = True
        st.session_state["SOURCE_SCIM_URL"] = SOURCE_SCIM_URL
        st.session_state["SOURCE_API_URL"] = SOURCE_API_URL
        st.session_state["SOURCE_SCIM_TOKEN"] = SOURCE_SCIM_TOKEN
        st.session_state["SOURCE_API_TOKEN"] = SOURCE_API_TOKEN
        st.session_state["SOURCE_WORKVIVO_ID"] = SOURCE_WORKVIVO_ID

        st.session_state["TARGET_SCIM_URL"] = TARGET_SCIM_URL
        st.session_state["TARGET_API_URL"] = TARGET_API_URL
        st.session_state["TARGET_SCIM_TOKEN"] = TARGET_SCIM_TOKEN
        st.session_state["TARGET_API_TOKEN"] = TARGET_API_TOKEN
        st.session_state["TARGET_WORKVIVO_ID"] = TARGET_WORKVIVO_ID

        st.session_state["SPACE_CREATOR_EXTERNAL_ID"] = SPACE_CREATOR_EXTERNAL_ID

        st.success("✅ Configuration saved! You can now run migrations.")
        st.stop()

    st.stop()  # prevent loading rest of the app UNTIL config is saved

# =========================================================
# CONFIG IS NOW SAVED — LOAD VALUES FROM SESSION
# =========================================================

SOURCE_SCIM_URL = st.session_state["SOURCE_SCIM_URL"]
SOURCE_API_URL = st.session_state["SOURCE_API_URL"]
SOURCE_SCIM_TOKEN = st.session_state["SOURCE_SCIM_TOKEN"]
SOURCE_API_TOKEN = st.session_state["SOURCE_API_TOKEN"]
SOURCE_WORKVIVO_ID = st.session_state["SOURCE_WORKVIVO_ID"]

TARGET_SCIM_URL = st.session_state["TARGET_SCIM_URL"]
TARGET_API_URL = st.session_state["TARGET_API_URL"]
TARGET_SCIM_TOKEN = st.session_state["TARGET_SCIM_TOKEN"]
TARGET_API_TOKEN = st.session_state["TARGET_API_TOKEN"]
TARGET_WORKVIVO_ID = st.session_state["TARGET_WORKVIVO_ID"]

SPACE_CREATOR_EXTERNAL_ID = st.session_state["SPACE_CREATOR_EXTERNAL_ID"]

st.success("🔐 Configuration active — ready to run migrations.")

# ============================================================
# Streamlit session state setup
# ============================================================
if "phase_running" not in st.session_state:
    st.session_state.phase_running = False

if "current_phase" not in st.session_state:
    st.session_state.current_phase = None

if "phase_log" not in st.session_state:
    st.session_state.phase_log = ""

if "phase1_company" not in st.session_state:
    st.session_state.phase1_company = ""

if "phase1_active_only" not in st.session_state:
    st.session_state.phase1_active_only = True


# =========================================================
# GLOBAL HEADERS FOR API CALLS
# =========================================================
source_scim_headers = {
    "Authorization": f"Bearer {SOURCE_SCIM_TOKEN}",
    "Accept": "application/json"
}

source_headers = {
    "Authorization": f"Bearer {SOURCE_API_TOKEN}",
    "Workvivo-Id": SOURCE_WORKVIVO_ID,
    "Accept": "application/json"
}

target_scim_headers = {
    "Authorization": f"Bearer {TARGET_SCIM_TOKEN}",
    "Accept": "application/json"
}

target_headers = {
    "Authorization": f"Bearer {TARGET_API_TOKEN}",
    "Workvivo-Id": TARGET_WORKVIVO_ID,
    "Accept": "application/json"
}


# =========================================================
# LOGGING AREA
# =========================================================
log_buffer = io.StringIO()

def ui_log(message):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {message}"

    # Store into ONE variable
    if "log_output" not in st.session_state:
        st.session_state["log_output"] = ""

    st.session_state["log_output"] += line + "\n"

    # Immediately show the update
    st.write(line)


# =========================================================
# HELPER: Fetch users
# =========================================================
def paginated_fetch(url, headers, take=100):
    """Fetch paginated results from Workvivo API."""
    results = []
    skip = 0

    while True:
        final_url = f"{url}?skip={skip}&take={take}"
        resp = requests.get(final_url, headers=headers)

        if resp.status_code != 200:
            ui_log(f"❌ Failed to fetch: {resp.status_code}")
            return results

        batch = resp.json().get("data", [])
        results.extend(batch)

        if len(batch) < take:
            break

        skip += take

    return results


def download_file(url, filename):
    """Download a file from a URL to /tmp."""
    try:
        resp = requests.get(url, stream=True)
        if resp.status_code != 200:
            return None

        path = f"/tmp/{filename}"
        with open(path, "wb") as f:
            f.write(resp.content)

        return path
    except:
        return None


def fetch_users(active_only=True):
    """Fetch users from SCIM in pages."""
    users = []
    start_index = 1
    count = 100

    while True:
        if active_only:
            url = f"{SOURCE_SCIM_URL}?filter=active eq true&startIndex={start_index}&count={count}"
        else:
            url = f"{SOURCE_SCIM_URL}?startIndex={start_index}&count={count}"

        resp = requests.get(url, headers=source_scim_headers)
        if resp.status_code != 200:
            ui_log(f"❌ Error fetching users: {resp.status_code}")
            break

        data = resp.json()
        batch = data.get("Resources", [])
        users.extend(batch)

        if len(batch) < count:
            break

        start_index += count
        time.sleep(0.25)

    return users

def create_global_space_and_enroll(company_name):
    """Creates a private Global Feed space and enrolls all users."""
    ui_log(f"🌍 Creating Global Feed space for: {company_name}")

    global_space_name = f"{company_name.strip()} Global Feed"

    # Step 1 — Check if already exists
    existing_spaces = paginated_fetch(f"{TARGET_API_URL}/spaces", target_headers)
    match = next((s for s in existing_spaces if s["name"] == global_space_name), None)

    if match:
        ui_log(f"⚠️ Global space already exists (ID {match['id']}) — using existing.")
        space_id = match["id"]
    else:
        # Step 2 — CREATE SPACE with PRIVATE visibility (matching your Python script)
        payload = {
            "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
            "name": global_space_name,
            "visibility": "private",   # <-- FIXED!!
            "description": f"{company_name} Global Feed private space.",
            "is_external": False
        }

        resp = requests.post(
            f"{TARGET_API_URL}/spaces",
            headers=target_headers,
            json=payload
        )

        if resp.status_code not in (200,201):
            ui_log(f"❌ Failed to create Global Space: {resp.text}")
            return None

        space_id = resp.json()["data"]["id"]
        ui_log(f"✅ Created Global Space '{global_space_name}' (ID {space_id})")

    # Step 3 — Enroll all target users
    ui_log("👥 Enrolling users into Global Space…")

    users = paginated_fetch(f"{TARGET_API_URL}/users", target_headers)
    numeric_ids = [u["id"] for u in users]

    chunks = [numeric_ids[i:i+100] for i in range(0, len(numeric_ids), 100)]

    for chunk in chunks:
        resp = requests.patch(
            f"{TARGET_API_URL}/spaces/{space_id}/users",
            headers=target_headers,
            json={"ids_to_add": chunk}
        )

        if resp.status_code not in (200,201):
            ui_log(f"⚠️ Failed to add user chunk: {resp.text}")

    ui_log("✅ Global Space enrollment complete!")
    return space_id


# =========================================================
# PHASE 1 — USERS
# =========================================================
def migrate_users(active_only):
    ui_log("=== USER MIGRATION START ===")

    users = fetch_users(active_only)
    ui_log(f"📥 Loaded {len(users)} users from source.")

    migrated = skipped = 0

    for u in users:
        email = (u.get("userName") or "").lower().strip()
        ext = u.get("externalId")

        if not email:
            skipped += 1
            ui_log(f"⚠️ Skipped missing email → {ext}")
            continue

        # Auto externalId fallback
        if not ext:
            ext = f"WV-AUTO-{random.randint(10000000, 99999999)}"
            ui_log(f"🪪 Generated extId {ext} for {email}")

        payload = {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User",
                "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
            ],
            "userName": email,
            "externalId": ext,
            "name": u.get("name", {}),
            "active": u.get("active", True)
        }

        resp = requests.post(TARGET_SCIM_URL, headers=target_scim_headers, json=payload)

        if resp.status_code in (200, 201):
            migrated += 1
            ui_log(f"✅ Created {email}")
        else:
            skipped += 1
            ui_log(f"⚠️ Skipped {email}: {resp.status_code}")

    ui_log(f"=== USER MIGRATION END — migrated={migrated}, skipped={skipped} ===")


# =========================================================
# PHASE 1A — USER AVATARS
# =========================================================
def upload_user_avatar(external_id, file_path):
    """Upload an avatar to the target tenant."""
    try:
        mime = "image/jpeg"
        with open(file_path, "rb") as f:
            files = {"image": (os.path.basename(file_path), f, mime)}

            resp = requests.put(
                f"{TARGET_API_URL}/users/by-external-id/{external_id}/profile-photo",
                headers=target_headers,
                files=files
            )

        return resp.status_code in (200, 201)

    except Exception as e:
        ui_log(f"⚠️ Avatar upload error for {external_id}: {e}")
        return False


def migrate_user_images():
    ui_log("=== USER IMAGE MIGRATION START ===")

    users = paginated_fetch(f"{SOURCE_API_URL}/users", source_headers)

    for u in users:
        ext = (u.get("external_id") or "").strip()
        url = u.get("avatar_url")

        if not ext or not url:
            continue

        file_path = download_file(url, f"user_{ext}.jpg")
        if not file_path:
            ui_log(f"⚠️ Failed to download avatar for {ext}")
            continue

        if upload_user_avatar(ext, file_path):
            ui_log(f"🖼️ Uploaded avatar for {ext}")
        else:
            ui_log(f"⚠️ Upload failed for {ext}")

    ui_log("=== USER IMAGE MIGRATION END ===")


# =========================================================
# PHASE 1B — SPACES
# =========================================================
def migrate_spaces():
    ui_log("=== SPACE MIGRATION START ===")

    source_spaces = paginated_fetch(f"{SOURCE_API_URL}/spaces", source_headers)
    target_spaces = paginated_fetch(f"{TARGET_API_URL}/spaces", target_headers)

    target_names = {s["name"].strip().lower(): s["id"] for s in target_spaces}

    created = skipped = 0

    for s in source_spaces:
        name = s.get("name", "").strip()
        norm = name.lower()

        if norm in target_names:
            skipped += 1
            ui_log(f"⚠️ Space already exists: {name}")
            continue

        payload = {
            "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
            "name": name,
            "visibility": "private",
            "description": s.get("description", ""),
            "is_external": False,
        }

        resp = requests.post(
            f"{TARGET_API_URL}/spaces",
            headers=target_headers,
            json=payload
        )

        if resp.status_code not in (200, 201):
            ui_log(f"❌ Failed creating '{name}': {resp.text}")
            continue

        created += 1
        ui_log(f"✅ Created space '{name}'")

    ui_log(f"=== SPACE MIGRATION END — created={created}, skipped={skipped} ===")


# =========================================================
# PHASE 1C — MEMBERSHIPS
# =========================================================
def migrate_memberships():
    ui_log("=== MEMBERSHIP MIGRATION START ===")

    source_memberships = paginated_fetch(f"{SOURCE_API_URL}/memberships", source_headers)

    for m in source_memberships:
        space_id = m.get("space_id")
        user_id = m.get("user_id")

        payload = {"ids_to_add": [user_id]}

        resp = requests.patch(
            f"{TARGET_API_URL}/spaces/{space_id}/users",
            headers=target_headers,
            json=payload
        )

        if resp.status_code in (200, 201):
            ui_log(f"👤 Added user {user_id} to space {space_id}")
        else:
            ui_log(f"⚠️ Membership failed: {resp.text[:150]}")

    ui_log("=== MEMBERSHIP MIGRATION END ===")


# =========================================================
# GLOBAL SPACE CREATION (PRIVATE) + ENROLLMENT
# =========================================================
def create_global_space_and_enroll(company_name):
    ui_log(f"🌍 Creating Global Feed: {company_name}")

    global_name = f"{company_name} Global Feed"

    spaces = paginated_fetch(f"{TARGET_API_URL}/spaces", target_headers)
    existing = next((s for s in spaces if s["name"] == global_name), None)

    if existing:
        ui_log(f"⚠️ Global space already exists → ID {existing['id']}")
        space_id = existing["id"]
    else:
        payload = {
            "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
            "name": global_name,
            "visibility": "private",
            "description": f"{company_name} Global Feed",
            "is_external": False
        }

        resp = requests.post(
            f"{TARGET_API_URL}/spaces",
            headers=target_headers,
            json=payload
        )

        if resp.status_code not in (200, 201):
            ui_log(f"❌ Failed to create Global Space: {resp.text}")
            return None

        space_id = resp.json()["data"]["id"]
        ui_log(f"✅ Created Global Space (ID {space_id})")

    # Enroll ALL users
    users = paginated_fetch(f"{TARGET_API_URL}/users", target_headers)
    user_ids = [u["id"] for u in users]

    ui_log(f"👥 Enrolling {len(user_ids)} users…")

    chunks = [user_ids[i:i + 100] for i in range(0, len(user_ids), 100)]

    for chunk in chunks:
        resp = requests.patch(
            f"{TARGET_API_URL}/spaces/{space_id}/users",
            headers=target_headers,
            json={"ids_to_add": chunk}
        )

        if resp.status_code not in (200, 201):
            ui_log(f"⚠️ Failed to add batch: {resp.text[:200]}")

    ui_log("✅ Global Space Enrollment Complete!")
    return space_id


# =========================================================
# PHASE 1 RUNNER — FULL END-TO-END
# =========================================================
def run_phase_1(company_name, active_only):
    lock_ui_for_phase()
    ui_log("▶ Starting Phase 1…")

    try:
        # 1) Global Space
        check_cancel()
        create_global_space_and_enroll(company_name)

        # 2) Users
        check_cancel()
        migrate_users(active_only)

        # 3) Avatars
        check_cancel()
        migrate_user_images()

        # 4) Spaces
        check_cancel()
        migrate_spaces()

        # 5) Memberships
        check_cancel()
        migrate_memberships()

        ui_log("🎉 Phase 1 Completed Successfully!")

    except Exception as e:
        # Cancel or error
        ui_log(f"⚠️ Migration stopped: {str(e)}")

    finally:
        unlock_ui()

# ============================================================
# 🔒 MIGRATION PHASE LOCKING + CANCEL SUPPORT
# ============================================================

# Initialize flags
if "phase_running" not in st.session_state:
    st.session_state.phase_running = False

if "cancel_requested" not in st.session_state:
    st.session_state.cancel_requested = False


def lock_ui_for_phase():
    """Lock UI during migration."""
    st.session_state.phase_running = True
    st.session_state.cancel_requested = False
    ui_log("🔒 UI locked — migration started…")


def unlock_ui():
    """Unlock UI when migration finishes or cancels."""
    st.session_state.phase_running = False
    st.session_state.cancel_requested = False
    ui_log("🔓 UI unlocked — migration stopped.")


def cancel_migration():
    """Request cancellation."""
    st.session_state.cancel_requested = True
    ui_log("🛑 Cancel requested… Stopping after the current item.")


# Modify all long loops to respect cancellation
def check_cancel():
    """Call this inside loops to stop safely."""
    if st.session_state.cancel_requested:
        ui_log("⛔ Migration cancelled by user.")
        unlock_ui()
        raise Exception("Migration Cancelled")

# =========================================================
# 2) PHASE SELECTION UI
# =========================================================
st.markdown("<div id='_migration'></div>", unsafe_allow_html=True)

st.header("🚦 Run Migration")

# 🔒 Disable all UI during migration
disabled = st.session_state.phase_running

phase = st.selectbox(
    "Choose migration phase",
    [
        "Phase 1 – Users, Avatars, Spaces, Memberships",
        "Phase 2 – Updates, Comments, Likes",
        "Phase 3 – Articles, Kudos, Events"
    ],
    index=0,
    disabled=disabled
)

# -------------------------------
# Phase 1
# -------------------------------
if phase.startswith("Phase 1"):

    st.subheader("Phase 1 Options")

    # Disable inputs if running
    disabled = st.session_state.phase_running

    company = st.text_input(
        "Company Name for Global Space",
        value=st.session_state.get("phase1_company", "My Company"),
        key="phase1_company",
        disabled=disabled
    )

    active_only = st.checkbox(
        "Migrate ONLY active users",
        value=st.session_state.get("phase1_active_only", True),
        key="phase1_active_only",
        disabled=disabled
    )

    # ============================
    # RUN BUTTON — triggers lock
    # ============================
    if not st.session_state.phase_running:
        # Only visible when not running
        if st.button("▶ Run Phase 1 Now"):
            st.session_state.phase_running = True
            st.session_state.cancel_requested = False
            st.session_state.start_phase_1 = True  # trigger for next cycle
            st.rerun()

    # ============================
    # CANCEL BUTTON — while running
    # ============================
    if st.session_state.phase_running:
        st.warning("Migration is currently running…")

        if st.button("❌ Cancel Migration", key="cancel_phase1_button"):
            cancel_migration()

    # ============================
    # START MIGRATION AFTER RERUN
    # ============================
    if st.session_state.get("start_phase_1", False):
        st.markdown("<div class='loading'></div>", unsafe_allow_html=True)
        run_phase_1(company, active_only)
        st.session_state.start_phase_1 = False

elif phase.startswith("Phase 2"):
    if st.button("▶ Run Phase 2"):
        ui_log("Phase 2 placeholder executed.")

else:
    modules = st.multiselect("Choose modules", ["Articles", "Kudos", "Events"])
    if st.button("▶ Run Phase 3"):
        ui_log(f"Phase 3 running modules: {modules}")


# =========================================================
# BOTTOM LOG OUTPUT
# =========================================================
st.markdown("<div id='_logs'></div>", unsafe_allow_html=True)

st.header("📜 Migration Log Output")

# Always render the latest log output
st.text_area(
    label="Log Output",
    value=st.session_state.get("log_output", ""),
    height=400,
    disabled=True
)

