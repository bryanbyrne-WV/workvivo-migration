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

# =====================================================================
# 2) LOAD YOUR EXISTING MIGRATION CODE HERE
# =====================================================================

st.header("📦 Migration Engine")

st.info("Paste your Python migration functions into the sections below.")

# -------------------------------------------------------
# 📌 PHASE 1 Placeholder
# -------------------------------------------------------
# ===============================================================
# Phase 1 — Users
# ===============================================================
def migrate_users():
    """
    SCIM: copy users from source to target by externalId / userName.
    Creates if missing, skips on 409 conflict, logs errors.
    """
    log("=== USER MIGRATION START ===")
    all_users = []
    start_index = 1
    count = 100

    print("\nSelect which users to migrate:")
    print("  [1] Active users only")
    print("  [2] All users (active + deactivated)")
    choice = input("\nEnter your choice (1/2): ").strip()
    active_only = (choice == "1")

    log(f"🔍 Migrating {'active only' if active_only else 'all'} users from source...")

    # Prefetch all existing users from target (by email + externalId)
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
            if email_tgt:
                existing_emails.add(email_tgt)
            if ext_tgt:
                existing_external_ids.add(ext_tgt)
        if len(data_tgt) < count:
            break
        skip += count
        time.sleep(DEFAULT_SLEEP)
    log(f"✅ Found {len(existing_emails)} existing emails and {len(existing_external_ids)} externalIds on target.")

    # Pull users from source SCIM using pagination
    while True:
        if active_only:
            # Only active users
            url = f"{SOURCE_SCIM_URL}?filter=active eq true&startIndex={start_index}&count={count}"
        else:
            # All users (active + deactivated)
            url = f"{SOURCE_SCIM_URL}?startIndex={start_index}&count={count}"
        resp = requests.get(url, headers=source_scim_headers, verify=VERIFY_SSL)
        if resp.status_code != 200:
            log(f"❌ Failed to fetch users: {resp.status_code}")
            break
        data = resp.json()
        users = data.get("Resources", [])
        all_users.extend(users)
        total = int(data.get("totalResults", 0))
        log(f"✅ Fetched {len(users)} users (accum: {len(all_users)})")
        if start_index + count > total:
            break
        start_index += count
        time.sleep(DEFAULT_SLEEP)

    # CSV outputs for skipped/error users
    skipped_csv = os.path.join(EXPORT_DIR, f"skipped_users_{TIMESTAMP}.csv")
    error_csv = os.path.join(EXPORT_DIR, f"error_users_{TIMESTAMP}.csv")

    migrated = skipped = errors = 0
    with open(skipped_csv, "w", newline="", encoding="utf-8") as skip_f, \
         open(error_csv, "w", newline="", encoding="utf-8") as err_f:
        skip_writer = csv.DictWriter(skip_f, fieldnames=["external_id", "reason"])
        err_writer = csv.DictWriter(err_f, fieldnames=["external_id", "status_code", "message"])
        skip_writer.writeheader()
        err_writer.writeheader()

        for u in all_users:
            ext = u.get("externalId")
            email = u.get("userName")
            active = u.get("active", True)

            email = u.get("userName", "").strip().lower()
            ext = u.get("externalId")

            # Skip if missing first or last name
            name_obj = u.get("name", {}) or {}
            first_name = name_obj.get("givenName", "").strip()
            last_name = name_obj.get("familyName", "").strip()

            if not first_name or not last_name:
                skipped += 1
                skip_writer.writerow({
                    "external_id": ext or "",
                    "reason": "Missing first name or last name"
                })
                log(f"⚠️ Skipped user {email}: missing first/last name (external_id={ext})")
                continue

            # If email missing, skip (we can’t create users without one)
            if not email:
                skipped += 1
                skip_writer.writerow({"external_id": ext or "", "reason": "Missing email"})
                log(f"⚠️ Skipped user: missing email (external_id={ext})")
                continue

            # Skip if email or externalId already exists on target
            if email in existing_emails:
                skipped += 1
                skip_writer.writerow({"external_id": ext or "", "reason": "Duplicate email on target"})
                log(f"⚠️ Skipped user {email}: duplicate email on target")
                continue

            if ext and ext.strip().upper() in existing_external_ids:
                skipped += 1
                skip_writer.writerow({"external_id": ext, "reason": "Duplicate externalId on target"})
                log(f"⚠️ Skipped user {email or ext}: duplicate externalId on target")
                continue

            # --- Extract optional fields safely ---
            job_title = (
                    u.get("title")
                    or u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}).get("title")
            )
            manager_info = (
                    u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}).get("manager")
                    or {}
            )
            manager_display = manager_info.get("displayName")
            manager_value = manager_info.get("value")

            # --- Build SCIM payload ---
            payload = {
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:User",
                    "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
                ],
                "userName": email,
                "name": u.get("name", {}),
                "active": u.get("active", True),
            }

            # Add legacy ID tracking
            payload["legacy_system_id"] = u.get("legacy_system_id") or f"LEGACY-{ext}"

            # Handle missing or invalid externalId
            if not ext or not isinstance(ext, str) or not ext.strip():
                # Deterministic fallback: based on email hash
                if not ext or not isinstance(ext, str) or not ext.strip():
                    ext = f"WV-MIG-AUTO-{random.randint(10000000, 99999999)}"
                    log(f"🪪 Generated random fallback externalId {ext} for user {email}")
                log(f"🪪 Generated fallback externalId {ext} from email {email}")

            else:
                ext = ext.strip()

            payload["externalId"] = ext

            # Add job title only if present and valid
            if job_title and isinstance(job_title, str) and job_title.strip():
                payload["title"] = job_title.strip()

            # --- Build enterprise extension ---
            enterprise_ext = {}

            # Add unique legacy_system_id
            legacy_id = u.get("legacy_system_id")
            if not legacy_id:
                legacy_id = f"wm-mig-{random.randint(100000000000, 999999999999)}"
            enterprise_ext["legacy_system_id"] = legacy_id

            # Manager (optional)
            if manager_value and isinstance(manager_value, str) and manager_value.strip():
                enterprise_ext["manager"] = {
                    "displayName": manager_display or "",
                    "value": manager_value.strip()
                }

            # Hire Date + DOB (optional)
            enterprise_src = u.get("urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}) or {}
            hire_date = enterprise_src.get("hireDate") or enterprise_src.get("HireDate")
            dob = enterprise_src.get("dateOfBirth") or enterprise_src.get("DateOfBirth")

            if hire_date:
                enterprise_ext["hireDate"] = hire_date
            if dob:
                enterprise_ext["dateOfBirth"] = dob

            # Attach enterprise extension if not empty
            if enterprise_ext:
                payload["urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"] = enterprise_ext

            resp = requests.post(TARGET_SCIM_URL, headers=target_scim_headers, json=payload, verify=VERIFY_SSL)

            if resp.status_code in [200, 201]:
                migrated += 1
                log(f"✅ Created user {ext} (Active={active})")
                continue

            if resp.status_code == 409:
                skipped += 1
                skip_writer.writerow(
                    {"external_id": ext, "reason": "User already exists with this email or external ID"})
                log(f"⚠️ Error 409: User already exists on target → {email or ext}")
                continue

            errors += 1
            err_writer.writerow({
                "external_id": ext or "",
                "status_code": resp.status_code,
                "message": resp.text[:400]  # limit for readability
            })

            # Log user details for traceability
            log(f"❌ Error creating user {email or ext or 'UNKNOWN'} ({ext or 'no externalId'}) → {resp.status_code}")
            log(f"   Response: {resp.text[:400]}")

    log(f"=== USER MIGRATION END ===")
    log(f"Summary: Migrated={migrated}, Skipped={skipped}, Errors={errors}")

# ===============================================================
# Phase 1a — User Avatars
# ===============================================================
def upload_user_avatar(external_id, file_path):
    """Upload a user avatar to the target Workvivo tenant."""
    if not os.path.exists(file_path):
        log(f"⚠️ Avatar file missing for {external_id}")
        return False
    try:
        mime_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"
        with open(file_path, "rb") as f:
            files = {"image": (os.path.basename(file_path), f, mime_type)}
            headers = {
                "Authorization": f"Bearer {TARGET_API_TOKEN}",
                "Workvivo-Id": TARGET_WORKVIVO_ID,
                "Accept": "application/json",
            }
            r = requests.put(
                f"{TARGET_API_URL}/users/by-external-id/{external_id}/profile-photo",
                headers=headers,
                files=files,
                verify=VERIFY_SSL,
                timeout=60,
            )
        if r.status_code in (200, 201):
            log(f"🖼️ Uploaded avatar for {external_id}")
            return True
        else:
            log(f"⚠️ Avatar upload failed for {external_id}: {r.status_code} {r.text[:200]}")
    except Exception as e:
        log(f"⚠️ Avatar upload exception for {external_id}: {e}")
    return False


def migrate_user_images():
    """Download and upload all user avatars from source → target."""
    log("=== USER IMAGE MIGRATION START ===")
    users = paginated_fetch(f"{SOURCE_API_URL}/users", source_headers)
    csv_path = os.path.join(EXPORT_DIR, f"user_image_results_{TIMESTAMP}.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["external_id", "source_url", "status"])

        for u in users:
            ext = normalize_external_id(u.get("external_id"))
            src_url = u.get("avatar_url")
            email = u.get("email") or u.get("userName")
            ext = normalize_external_id(u.get("external_id"))

            # Skip users without external IDs — they should not exist in Phase 1A
            if not ext:
                log(f"⚠️ Skipping avatar for user with missing external_id: {email}")
                continue

            if not ext or not src_url:
                continue

            file_path = download_file(src_url, f"user_{ext}.jpg")
            if not file_path:
                writer.writerow([ext, src_url, "download_failed"])
                continue
            success = upload_user_avatar(ext, file_path)
            writer.writerow([ext, src_url, "success" if success else "failed"])
            time.sleep(DEFAULT_SLEEP)

    log(f"=== USER IMAGE MIGRATION END === → CSV saved to {csv_path}")

# ===============================================================
# Phase 1b
# ===============================================================
# ===============================================================
# Phase 1 — Spaces (with Logo + Header Migration, Single POST)
# ===============================================================
def migrate_spaces():
    """
    Create target spaces matching source spaces by name, using a fixed creator.
    Prevents duplicates by checking existing target spaces by name.
    Also migrates space logo (icon_url) and header image (header_url) via single POST call.
    """
    log("=== SPACE MIGRATION START ===")

    # Verify the migration user exists
    check_url = f"{TARGET_SCIM_URL}?filter=externalId eq \"{SPACE_CREATOR_EXTERNAL_ID}\""
    check = requests.get(check_url, headers=target_scim_headers, verify=VERIFY_SSL)
    creator_exists = check.status_code == 200 and bool(check.json().get("Resources"))
    if not creator_exists:
        log(f"❌ Space creator '{SPACE_CREATOR_EXTERNAL_ID}' not found on target. Please create it first.")
        return

    # Fetch all existing spaces from target
    target_spaces = fetch_all_spaces(TARGET_API_URL, target_headers, label="target", add_org_filter=True)
    target_names = {normalize_external_id(s.get("name")) for s in target_spaces}

    # Fetch all spaces from source
    source_spaces = fetch_all_spaces(SOURCE_API_URL, source_headers, label="source", add_org_filter=True)

    created, skipped, failed = 0, 0, 0
    for s in source_spaces:
        src_name = s.get("name", "").strip()
        norm_name = normalize_external_id(src_name)
        if norm_name in target_names:
            skipped += 1
            log(f"⚠️ Space '{src_name}' already exists on target — skipping.")
            continue

        # ✅ Prepare basic payload fields
        visibility = (s.get("visibility") or "private").lower()
        if visibility not in ["private", "public", "company_wide"]:
            visibility = "private"

        payload = {
            "user_external_id": SPACE_CREATOR_EXTERNAL_ID,
            "name": src_name,
            "visibility": visibility,
            "description": s.get("description", ""),
            "is_external": str(s.get("is_external", False)).lower(),
            "enable_news": "true",
            "enable_events": "true",
            "enable_documents": "true",
            "enable_qa": "true",
            "enable_pages": "true",
        }

        # ✅ Prepare optional images
        files = {}
        icon_url = s.get("icon_url")
        header_url = s.get("header_url")

        if icon_url:
            try:
                r_icon = requests.get(icon_url, stream=True, verify=VERIFY_SSL)
                if r_icon.status_code == 200:
                    files["image_icon"] = (f"{src_name}_icon.jpg", r_icon.content, "image/jpeg")
                    log(f"🖼️ Added logo for '{src_name}'")
            except Exception as e:
                log(f"⚠️ Failed to fetch logo for '{src_name}': {e}")

        if header_url:
            try:
                r_header = requests.get(header_url, stream=True, verify=VERIFY_SSL)
                if r_header.status_code == 200:
                    files["image_header"] = (f"{src_name}_header.jpg", r_header.content, "image/jpeg")
                    log(f"🖼️ Added header for '{src_name}'")
            except Exception as e:
                log(f"⚠️ Failed to fetch header for '{src_name}': {e}")

        # ✅ Send POST request (multipart/form-data)
        try:
            resp = requests.post(
                f"{TARGET_API_URL}/spaces",
                headers=target_headers_form,
                data=payload,
                files=files if files else None,
                verify=VERIFY_SSL,
            )

            if resp.status_code == 201:
                created += 1
                new_id = resp.json().get("data", {}).get("id")
                log(f"✅ Created space '{src_name}' (id={new_id}, visibility={visibility})")
            else:
                failed += 1
                log(f"❌ Failed to create '{src_name}': {resp.status_code} {resp.text[:200]}")
        except Exception as e:
            failed += 1
            log(f"⚠️ Exception creating '{src_name}': {e}")

    log(f"=== SPACE MIGRATION END === (created={created}, skipped={skipped}, failed={failed})")

def run_phase_1():
    print("\n=== PHASE 1: USER / SPACE / MEMBERSHIP MIGRATION ===\n")

    # 💬 Prompt for company name
    company_name = input("Enter the Company Name (for Global space creation): ").strip()
    if company_name:
        create_global_space_and_enroll(company_name)
    else:
        log("⚠️ No company name entered — skipping Global space creation.")

    log("▶️ Running Phase 1: Users → Avatars → Spaces → Memberships...")
    migrate_users()
    migrate_user_images()
    migrate_spaces()
    migrate_memberships()
    log("✅ Phase 1 completed successfully.")

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
    if st.button("▶ Run Phase 1"):
        run_phase_1()

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
