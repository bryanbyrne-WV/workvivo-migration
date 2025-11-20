import streamlit as st
import requests
import time
import io
from datetime import datetime
import random
import os
import mimetypes

st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

st.title("🚀 Workvivo Migration Tool")
st.write("Run internal Workvivo migrations without touching Python scripts.")

# =========================================================
# 1) CONFIG FORM (SHOWN ONLY IF NOT SAVED)
# =========================================================

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

def create_global_space_and_enroll(company_name):
    """Creates the Global Space and enrolls all users."""
    ui_log(f"🌍 Creating Global Space: {company_name}")

    payload = {
        "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
        "name": company_name,
        "visibility": "company_wide",
        "enable_news": "true",
        "enable_events": "true",
        "enable_documents": "true",
        "enable_qa": "true",
        "enable_pages": "true",
    }

    resp = requests.post(
        f"{TARGET_API_URL}/spaces",
        headers=target_headers,
        data=payload
    )

    if resp.status_code not in (200, 201):
        ui_log(f"❌ Failed to create Global Space: {resp.text}")
        return None

    space_id = resp.json()["data"]["id"]
    ui_log(f"✅ Created Global Space (ID {space_id})")

    # Now fetch all target users and enroll them
    ui_log("👥 Enrolling all users into Global Space…")

    users = paginated_fetch(f"{TARGET_API_URL}/users", target_headers)

    numeric_ids = [u["id"] for u in users]
    chunks = [numeric_ids[i:i+50] for i in range(0, len(numeric_ids), 50)]

    for chunk in chunks:
        resp2 = requests.patch(
            f"{TARGET_API_URL}/spaces/{space_id}/users",
            headers=target_headers,
            json={"ids_to_add": chunk}
        )
        if resp2.status_code not in (200, 201):
            ui_log(f"⚠️ Failed batch enroll: {resp2.text}")

    ui_log("✅ Global Space enrollment complete!")
    return space_id

def migrate_user_avatars():
    ui_log("=== USER AVATAR MIGRATION START ===")

    users = paginated_fetch(f"{SOURCE_API_URL}/users", source_headers)

    for u in users:
        ext = u.get("external_id")
        src_url = u.get("avatar_url")

        if not ext or not src_url:
            continue

        path = download_file(src_url, f"avatar_{ext}.jpg")
        if not path:
            ui_log(f"⚠️ Failed to download avatar for {ext}")
            continue

        mime_type = mimetypes.guess_type(path)[0] or "image/jpeg"

        with open(path, "rb") as f:
            files = {"image": (os.path.basename(path), f, mime_type)}

            resp = requests.put(
                f"{TARGET_API_URL}/users/by-external-id/{ext}/profile-photo",
                headers={
                    "Authorization": f"Bearer {TARGET_API_TOKEN}",
                    "Workvivo-Id": TARGET_WORKVIVO_ID,
                    "Accept": "application/json"
                },
                files=files
            )

        if resp.status_code in (200,201):
            ui_log(f"🖼️ Uploaded avatar for {ext}")
        else:
            ui_log(f"⚠️ Avatar failed for {ext}: {resp.status_code}")

    ui_log("=== USER AVATAR MIGRATION END ===")

def migrate_spaces():
    ui_log("=== SPACE MIGRATION START ===")

    source_spaces = paginated_fetch(f"{SOURCE_API_URL}/spaces", source_headers)
    target_spaces = paginated_fetch(f"{TARGET_API_URL}/spaces", target_headers)

    target_names = {s["name"].strip().lower() for s in target_spaces}

    for s in source_spaces:
        name = s.get("name", "").strip()

        if name.lower() in target_names:
            ui_log(f"⚠️ Space exists, skipping: {name}")
            continue

        payload = {
            "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
            "name": name,
            "visibility": s.get("visibility") or "private",
            "description": s.get("description") or ""
        }

        resp = requests.post(
            f"{TARGET_API_URL}/spaces",
            headers=target_headers,
            data=payload
        )

        if resp.status_code in (200,201):
            ui_log(f"✅ Created space: {name}")
        else:
            ui_log(f"❌ Failed to create space {name}: {resp.text}")

    ui_log("=== SPACE MIGRATION END ===")

def migrate_memberships():
    ui_log("=== MEMBERSHIP MIGRATION START ===")

    source_spaces = paginated_fetch(f"{SOURCE_API_URL}/spaces", source_headers)
    target_spaces = paginated_fetch(f"{TARGET_API_URL}/spaces", target_headers)

    name_to_target = {s["name"].lower(): s["id"] for s in target_spaces}

    for s in source_spaces:
        name = s["name"].lower()
        if name not in name_to_target:
            continue

        target_id = name_to_target[name]

        members = paginated_fetch(
            f"{SOURCE_API_URL}/spaces/{s['id']}/users",
            source_headers
        )

        numeric_ids = [m["user"]["id"] for m in members if m.get("user")]

        chunks = [numeric_ids[i:i+50] for i in range(0, len(numeric_ids), 50)]

        for chunk in chunks:
            resp = requests.patch(
                f"{TARGET_API_URL}/spaces/{target_id}/users",
                headers=target_headers,
                json={"ids_to_add": chunk}
            )
            if resp.status_code not in (200,201):
                ui_log(f"⚠️ Failed to enroll batch for space {name}")

        ui_log(f"👥 Memberships migrated for {name}")

    ui_log("=== MEMBERSHIP MIGRATION END ===")

# =========================================================
# PHASE 1 RUNNER
# =========================================================
def run_phase_1(company_name, active_only):
    ui_log("▶ Starting Phase 1…")

    # 1. Global Space
    create_global_space_and_enroll(company_name)

    # 2. Users
    migrate_users(active_only)

    # 3. Avatars
    migrate_user_avatars()

    # 4. Spaces
    migrate_spaces()

    # 5. Memberships
    migrate_memberships()

    ui_log("🎉 Phase 1 fully completed!")

# =========================================================
# 2) PHASE SELECTION UI
# =========================================================
st.header("🚦 Run Migration")

phase = st.selectbox(
    "Choose migration phase",
    ["Phase 1 – Users, Avatars, Spaces, Memberships",
     "Phase 2 – Updates, Comments, Likes",
     "Phase 3 – Articles, Kudos, Events"],
    index=0,
    disabled=st.session_state.phase_running   # 🔒 Lock if running
)

if phase.startswith("Phase 1"):

    st.subheader("Phase 1 Options")

    company = st.text_input("Company Name for Global Space", value="My Company")
    active_only = st.checkbox("Migrate ONLY active users", value=True)

    if st.button("▶ Run Phase 1 Now"):
        run_phase_1(company, active_only)

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
st.header("📜 Migration Log Output")

# Always render the latest log output
st.text_area(
    label="Log Output",
    value=st.session_state.get("log_output", ""),
    height=400,
    disabled=True
)

