
# -*- coding: utf-8 -*-
import streamlit as st
import requests
import time
import io
from datetime import datetime
import random
import os
import mimetypes

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Workvivo2025!"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.markdown("""
        <style>

            /* Soft gradient background */
            body {
                background: linear-gradient(
                    180deg,
                    #EFE8FF 0%,
                    #E4D9FF 30%,
                    #DBEFFF 80%,
                    #F9FCFF 100%
                ) !important;
            }

            .login-wrapper {
                max-width: 420px;
                margin: 7rem auto;
                text-align: center;
            }

            /* Title (no logo above it) */
            .login-title {
                font-size: 2rem;
                color: #5A3EA6;
                font-weight: 700;
                margin-bottom: 0.4rem;
                margin-top: 1rem;
            }

            .login-note {
                font-size: 1.05rem;
                color: #6B56B0;
                opacity: 0.8;
                margin-bottom: 2.2rem;
            }

            /* Underline input style */
            .underline-input input {
                background: transparent !important;
                border: none !important;
                border-bottom: 1px solid #8368D8 !important;
                border-radius: 0 !important;
                color: #4A2F8A !important;
                padding: 0.6rem 0 !important;
                font-size: 1.05rem;
            }

            .underline-input input::placeholder {
                color: #9A84DD !important;
                opacity: 0.6;
            }

            /* Login button */
            .blue-btn button {
                width: 100%;
                background-color: #3C4FA8 !important;
                color: white !important;
                border-radius: 8px !important;
                height: 3rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                border: none !important;
                margin-top: 1.8rem;
            }

            /* Request access link */
            .request-button {
                display: inline-block;
                margin-top: 1.6rem;
                font-size: 0.95rem;
                color: #3C4FA8 !important;
                text-decoration: underline;
                opacity: 0.85;
            }

        </style>
    """, unsafe_allow_html=True)

    # Centered layout
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    # Header text (no logo)
    st.markdown('<div class="login-title">User Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-note">Please sign in to access the Migration Tool</div>',
                unsafe_allow_html=True)

    # Inputs
    st.markdown('<div class="underline-input">', unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Username")
    password = st.text_input("Password", placeholder="Password", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    remember = st.checkbox("Remember me")

    # Login button
    st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
    login_button = st.button("LOGIN")
    st.markdown('</div>', unsafe_allow_html=True)

    # Login logic
    if login_button:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    # Request access link
    st.markdown(
        """
        <a class="request-button"
           href="mailto:bryan.byrne@workvivo.com?subject=Access Request - Migration Tool&body=Hi Bryan,%0D%0A%0D%0ACan I please get access to the Migration Tool?%0D%0A%0D%0AThanks!">
            Request Access
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()



st.set_page_config(page_title="Workvivo Migration Tool", layout="wide")

# ==========================================
# Page state (2-page layout)
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "config"


# ============================================================
# WORKVIVO ADVANCED UI THEME + LOADING + BUTTONS + DARK-MODE
# ============================================================
WORKVIVO_LOGO_URL = "https://www.festivalofwork.com/media/Workvivo%20(1).png"

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
        font-size: 42px;
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

</style>
"""

# Brand Logo (Centered)
st.markdown("""
<div style="text-align:center; margin-top:10px; margin-bottom:5px;">
    <img src="https://www.festivalofwork.com/media/Workvivo%20(1).png" 
         style="height:80px;">
</div>
""", unsafe_allow_html=True)

# Cool Gradient Header (ONLY)
st.markdown("""
<style>
.cool-header {
    width: 100%;
    background: linear-gradient(90deg, #6203ed, #8a3dfc);
    padding: 28px 0;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(98,3,237,0.35);
    margin-bottom: 25px;
    animation: fadeSlide 0.6s ease-out;
}

.cool-header-title {
    color: white;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -1px;
    text-shadow: 0 4px 16px rgba(0,0,0,0.25);
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>

<div class="cool-header">
    <div class="cool-header-title">Internal Migration Tool v1.0</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.custom-continue > button {
    background-color: #6203ed !important;   /* Purple */
    color: white !important;                /* White text */
    border: none !important;
    padding: 10px 26px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
    transition: 0.2s;
}
.custom-continue > button:hover {
    background-color: #4c02b5 !important;   /* Darker purple */
    transform: translateY(-1px);
}
.custom-continue > button:active {
    transform: scale(0.98);
}
</style>
""", unsafe_allow_html=True)



# ============================
# CARD SELECTION UI STYLES
# ============================
st.markdown("""
<style>
.select-card {
    border-radius: 12px;
    padding: 18px;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 2px solid transparent;
    text-align: center;
    cursor: pointer;
    transition: 0.2s;
    min-height: 110px;
}
.select-card:hover {
    transform: translateY(-3px);
    border-color: #6203ed;
}
.select-card.selected {
    border-color: #6203ed !important;
    background: #f4ecff !important;
}
.select-card-icon {
    font-size: 32px;
    margin-bottom: 10px;
    color: #6203ed;
}
.select-card-title {
    font-size: 18px;
    font-weight: 600;
}
.select-card-sub {
    font-size: 14px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 1) CONFIG FORM (SHOWN ONLY IF NOT SAVED)
# =========================================================
st.markdown("<div id='_config'></div>", unsafe_allow_html=True)

if "config_saved" not in st.session_state:

    with st.form("config_form"):

        st.header("🔐 Environment Configuration")

        st.markdown("""
        <style>
            .config-card {
                background: #ffffff;
                padding: 18px 22px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 18px;
            }
            summary {
                font-size: 18px;
                font-weight: 600;
                color: #6203ed;
                cursor: pointer;
                padding: 6px 0;
            }
        </style>
        """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # SOURCE ENVIRONMENT
        # ----------------------------------------------------
        st.markdown("<div class='config-card'>", unsafe_allow_html=True)
        with st.expander("Source Environment", expanded=True):

            SOURCE_SCIM_URL = st.text_input(
                "Source SCIM URL",
                value="https://workvivo.workvivo.com/scim/v1/scim/Users/",
                help="SCIM endpoint for reading users from the SOURCE Workvivo environment."
            )

            SOURCE_API_URL = st.text_input(
                "Source API URL",
                value="https://api.workvivo.com/v2",
                help="Base API URL for fetching content, spaces, images and memberships from the SOURCE tenant."
            )

            SOURCE_SCIM_TOKEN = st.text_input(
                "Source SCIM Token",
                value="Yz1Pj7m6MOGPRmhkbpzGI85VxsCW8WdvCKFBIVcj",
                type="password",
                help="Authentication token for SCIM user requests in the SOURCE tenant."
            )

            SOURCE_API_TOKEN = st.text_input(
                "Source API Token",
                value="357|a6ad24b87add478518ae2fa2d1ff67d9a1040bf6",
                type="password",
                help="Bearer token used for API calls to retrieve content and metadata from the SOURCE tenant."
            )

            SOURCE_WORKVIVO_ID = st.text_input(
                "Source Workvivo ID",
                value="51",
                help="Workvivo ID required for API requests on the SOURCE tenant."
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # TARGET ENVIRONMENT
        # ----------------------------------------------------
        st.markdown("<div class='config-card'>", unsafe_allow_html=True)
        with st.expander("Target Environment", expanded=True):

            TARGET_SCIM_URL = st.text_input(
                "Target SCIM URL",
                value="https://migration-test-1.workvivo.com/scim/v2/scim/Users/",
                help="SCIM endpoint for creating users in the TARGET Workvivo environment."
            )

            TARGET_API_URL = st.text_input(
                "Target API URL",
                value="https://api.eu2.workvivo.com/v1",
                help="Base API URL for creating spaces, memberships and content in the TARGET tenant."
            )

            TARGET_SCIM_TOKEN = st.text_input(
                "Target SCIM Token",
                value="nLgLGVnMHaYySx9DqCixkHx0lUZqgxTGwT7RyKMj",
                type="password",
                help="Authentication token for SCIM user creation inside the TARGET tenant."
            )

            TARGET_API_TOKEN = st.text_input(
                "Target API Token",
                value="1006|fb9c50816d6db9f14163146b8205538bdb3264e5",
                type="password",
                help="Bearer token for creating spaces, uploading images and writing content to the TARGET tenant."
            )

            TARGET_WORKVIVO_ID = st.text_input(
                "Target Workvivo ID",
                value="3000384",
                help="Workvivo ID required for API requests on the TARGET tenant."
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MIGRATION USER (SPACE CREATOR)
        # ----------------------------------------------------
        st.markdown("<div class='config-card'>", unsafe_allow_html=True)

        SPACE_CREATOR_EXTERNAL_ID = st.text_input(
            "Migration External ID (Space Creator)",
            value="workvivo-migration-user",
            help="External ID of the system user used when creating spaces or system-owned content in the TARGET tenant."
        )

        st.markdown("</div>", unsafe_allow_html=True)

               # ----------------------------------------------------
        # VALIDATION + BUTTON STYLING
        # ----------------------------------------------------
        errors = []

        # Required source fields
        if not SOURCE_SCIM_URL:
            errors.append("Source SCIM URL is required.")
        if not SOURCE_API_URL:
            errors.append("Source API URL is required.")
        if not SOURCE_SCIM_TOKEN:
            errors.append("Source SCIM Token is required.")
        if not SOURCE_API_TOKEN:
            errors.append("Source API Token is required.")
        if not SOURCE_WORKVIVO_ID:
            errors.append("Source Workvivo-ID is required.")

        # Required target fields
        if not TARGET_SCIM_URL:
            errors.append("Target SCIM URL is required.")
        if not TARGET_API_URL:
            errors.append("Target API URL is required.")
        if not TARGET_SCIM_TOKEN:
            errors.append("Target SCIM Token is required.")
        if not TARGET_API_TOKEN:
            errors.append("Target API Token is required.")
        if not TARGET_WORKVIVO_ID:
            errors.append("Target Workvivo-ID is required.")

        # Required migration user
        if not SPACE_CREATOR_EXTERNAL_ID:
            errors.append("Migration External ID (Space Creator) is required.")

        # Show warnings
        if errors:
            for e in errors:
                st.warning("⚠️ " + e)


                # ----------------------------------------------------
        # SUPPORT NOTE
        # ----------------------------------------------------
        st.markdown("""
        <div style="margin-top: 20px; padding: 12px; background: #f4ecff; border-left: 4px solid #6203ed; border-radius: 6px;">
        <strong>Need help?</strong><br>
        If you cannot find any of this information, please contact 
        <a href="mailto:support@workvivo.com">support@workvivo.com</a>.
        </div>
        """, unsafe_allow_html=True)

        # Add styling for purple buttons
        st.markdown("""
        <style>
        .purple-btn > button {
            background-color: #6203ed !important;
            color: white !important;
            border: none !important;
            padding: 10px 26px !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            height: 48px !important;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
            transition: 0.2s;
        }
        .purple-btn > button:hover {
            background-color: #4c02b5 !important;
            transform: translateY(-1px);
        }
        .purple-btn > button:active {
            transform: scale(0.98);
        }
        </style>
        """, unsafe_allow_html=True)

        # SAVE BUTTON (purple)
        st.markdown('<div class="purple-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "Save Configuration",
            disabled=len(errors) > 0
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # OUTSIDE THE FORM — PROCESS SAVE
    # ----------------------------------------------------
    if submitted:

        # Save all values
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

        st.success("Configuration saved! Click Continue to proceed.")

        # CONTINUE BUTTON (purple)
        st.markdown('<div class="purple-btn">', unsafe_allow_html=True)
        if st.button("➡ CONTINUE"):
            st.session_state.page = "main"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.stop()

    st.stop()

# =========================================================
# If config not saved, stay on config page
# =========================================================
if "config_saved" not in st.session_state:
    st.session_state.page = "config"
else:
    if st.session_state.page == "config":
        st.session_state.page = "main"


# =========================================================
# CONFIG IS NOW SAVED — LOAD VALUES FROM SESSION
# =========================================================

# Allow user to return to environment configuration
st.markdown("""
<div style="margin-bottom: 15px;">
    <style>
    .back-btn > button {
        background-color: #6203ed !important;
        color: white !important;
        border: none !important;
        padding: 6px 18px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
        transition: 0.2s;
    }
    .back-btn > button:hover {
        background-color: #4c02b5 !important;
        transform: translateY(-1px);
    }
    </style>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.green-finish > button {
    background-color: #28a745 !important;  /* Green */
    color: white !important;
    border: none !important;
    padding: 10px 26px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
    transition: 0.2s;
}
.green-finish > button:hover {
    background-color: #1e7e34 !important;  /* Darker green */
    transform: translateY(-1px);
}
.green-finish > button:active {
    transform: scale(0.97);
}
</style>
""", unsafe_allow_html=True)


if st.session_state.page != "summary":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Edit Environment Settings"):
        if "config_saved" in st.session_state:
            del st.session_state["config_saved"]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



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

if st.session_state.page != "summary":
    st.success("🔐 Configuration active — ready to run migrations.")

# ============================================================
# Ensure SUMMARY dictionary exists before any migration starts
# ============================================================
if "summary" not in st.session_state:
    st.session_state.summary = {
        "users_migrated": 0,
        "users_skipped": 0,

        "spaces_created": 0,
        "spaces_skipped": 0,

        "memberships_added": 0,

        "updates_migrated": 0,
        "updates_skipped": 0,

        "kudos_migrated": 0,
        "kudos_skipped": 0,

        "articles_migrated": 0,
        "articles_skipped": 0,

        "events_migrated": 0,
        "events_skipped": 0,

        "global_pages_migrated": 0,
        "space_pages_migrated": 0,

        "start_time": datetime.utcnow(),
        "end_time": None,
    }

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

if "phase1_console_visible" not in st.session_state:
    st.session_state.phase1_console_visible = False


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
# Ensure console placeholder always exists
if "console_placeholder" not in st.session_state:
    st.session_state.console_placeholder = None

log_buffer = io.StringIO()

def ui_log(message):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] {message}"

    # Append to session buffer
    if "log_output" not in st.session_state:
        st.session_state["log_output"] = ""

    st.session_state["log_output"] += line + "\n"

    # Real-time UI update (only if placeholder exists)
    if "live_log_placeholder" in st.session_state:
        st.session_state.live_log_placeholder.text_area(
            "📡 Live Console Output",
            st.session_state["log_output"],
            height=400,
            disabled=True
        )



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

# ============================
# Helper: Selectable Card Component
# ============================
def selectable_card(key, title, icon, subtitle):
    selected = st.session_state.get(key, False)

    card_class = "select-card selected" if selected else "select-card"

    clicked = st.container().markdown(
        f"""
        <div class="{card_class}" onclick="document.getElementById('{key}').click()">
            <div class="select-card-icon">{icon}</div>
            <div class="select-card-title">{title}</div>
            <div class="select-card-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # hidden checkbox syncing state
    st.checkbox("hidden", key=key, value=selected, label_visibility="collapsed")

    return st.session_state[key]

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
            st.session_state.summary["users_migrated"] += 1
            ui_log(f"✅ Created {email}")
        else:
            skipped += 1
            st.session_state.summary["spaces_skipped"] += 1
            st.session_state.summary["users_skipped"] += 1
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
        st.session_state.summary["spaces_created"] += 1
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
    st.session_state.phase1_running = False
    st.session_state.cancel_requested = False
    ui_log("🔓 UI unlocked — migration stopped.")



def cancel_migration():
    st.session_state.cancel_requested = True
    ui_log("🛑 Cancel requested… Stopping after the current item.")


# Modify all long loops to respect cancellation
def check_cancel():
    """Call this inside loops to stop safely."""
    if st.session_state.cancel_requested:
        ui_log("⛔ Migration cancelled by user.")
        unlock_ui()
        raise Exception("Migration Cancelled")



# ============================================================
# MAIN PAGE (Migration Dashboard)
# ============================================================
if st.session_state.page == "main":

    st.markdown("## Migrate Workvivo Data")

    # ============================================================
    # 📅 Date Range for Content Migration
    # ============================================================
    st.markdown("#### 📅 Date Range")

    date_options = [
        "Last 6 months",
        "Last 1 year",
        "Last 2 years",
        "Last 3 years",
        "All time",
        "Custom range",
    ]

    if "migration_date_choice" not in st.session_state:
        st.session_state.migration_date_choice = "Last 1 year"

    date_choice = st.selectbox(
        "Select date range",
        date_options,
        index=date_options.index(st.session_state.migration_date_choice),
        key="migration_date_choice",
    )

    from datetime import datetime, timedelta

    today = datetime.utcnow()
    start_date = None
    end_date = today

    if date_choice == "Last 6 months":
        start_date = today - timedelta(days=182)
    elif date_choice == "Last 1 year":
        start_date = today - timedelta(days=365)
    elif date_choice == "Last 2 years":
        start_date = today - timedelta(days=365 * 2)
    elif date_choice == "Last 3 years":
        start_date = today - timedelta(days=365 * 3)
    elif date_choice == "All time":
        start_date = None
    elif date_choice == "Custom range":
        st.markdown("##### Custom Range")
        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")

    def fmt(d):
        if d is None:
            return "All time"
        if hasattr(d, "strftime"):
            return d.strftime("%b %d, %Y")
        return str(d)

    pretty_start = fmt(start_date)
    pretty_end = fmt(end_date)

    st.info(f"📌 Migrating content from **{pretty_start}** to **{pretty_end}**")

    st.session_state.migration_start_date = start_date
    st.session_state.migration_end_date = end_date

    # -----------------------------------------------------------
    # Company Name Prompt (for Global Feed creation)
    # -----------------------------------------------------------
    st.markdown("#### Organisation Name")
    st.session_state.phase1_company = st.text_input(
        "Enter the organisation name for the Global Feed",
        value=st.session_state.get("phase1_company", ""),
        placeholder="Example: Workvivo, Zoom, etc..."
    )
    
    if not st.session_state.phase1_company:
        st.warning("Please enter a company name — required to create the Global Feed.")

    # ============================================================
    # 🏢 Organisation settings and information
    # ============================================================
    st.markdown("### Organisation settings and information")
    st.markdown("""
    This section migrates users, spaces and space membership.
    """)

    migrate_users = st.toggle("Users", value=True, disabled=True)
    migrate_spaces = st.toggle("Spaces", value=True, disabled=True)

    st.markdown("---")

    # ============================================================
    # 👥 User activity on Workvivo
    # ============================================================
    st.markdown("### User activity on Workvivo")
    st.markdown("Migrate content & user interactions.")

    migrate_updates = st.toggle("Updates", value=True)
    migrate_kudos = st.toggle("Kudos", value=True)
    migrate_articles = st.toggle("Articles", value=True)
    migrate_events = st.toggle("Events", value=True)
    migrate_comments = st.toggle("Comments", value=True)
    migrate_likes = st.toggle("Likes", value=True)
    migrate_globalPages = st.toggle("Global Pages", value=True)
    migrate_spacePages = st.toggle("Space Pages", value=True)

    
    if st.button("▶ Run Migration"):
    
        # Smooth scroll (optional)
        st.components.v1.html(
            """
            <script>
                window.parent.scrollTo({ top: 0, behavior: 'smooth' });
            </script>
            """,
            height=0,
        )
    
        st.session_state.start_migration = True
        st.session_state.migration_finished = False
        st.session_state.cancel_requested = False
        st.session_state.progress = 0
    
        # Switch page
        st.session_state.page = "running"
    
        # ⭐ REQUIRED or user must click twice
        st.rerun()

        # Auto-scroll to the "Migration In Progress..." header
    st.components.v1.html(
        """
        <script>
            const el = Array.from(
                document.querySelectorAll('h1, h2, h3, h4')
            ).find(e => e.innerText.includes("Migration In Progress"));
            
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        </script>
        """,
        height=0,
)


    # ============================================================
    # LIVE LOG OUTPUT (optional)
    # ============================================================
    if "live_log_placeholder" not in st.session_state:
        st.session_state.live_log_placeholder = st.empty()

    if st.session_state.get("phase1_running") or st.session_state.get("log_output"):

        st.markdown("<div id='_logs'></div>", unsafe_allow_html=True)
        st.header("Migration Console")

        st.session_state.live_log_placeholder.text_area(
            "Live Console Output",
            st.session_state.get("log_output", ""),
            height=400,
            disabled=True
        )


# ============================================================
# MIGRATION PAGE — FINAL WORKING VERSION
# ============================================================
elif st.session_state.page == "running":

    # --------------------------------------------------------
    # HEADER LOGIC
    # --------------------------------------------------------
    if st.session_state.get("migration_finished", False):
        st.header("Migration Finished!")

    elif st.session_state.cancel_requested:
        st.header("Migration Cancelled")

    else:
        st.header("Migration In Progress...")

    # --------------------------------------------------------
    # CANCEL vs FINISH BUTTON
    # --------------------------------------------------------
    if not st.session_state.get("migration_finished", False) and not st.session_state.cancel_requested:
        # Migration is still running
        if st.button("🛑 Cancel Migration"):
            st.session_state.cancel_requested = True
            ui_log("🛑 Cancel requested by user…")
            st.rerun()
    else:
        # Migration complete or cancelled → show FINISH
        if st.button("✔ FINISH"):
    
            # Fully clear old migration state
            keys_to_clear = [
                "progress",
                "log_output",
                "migration_finished",
                "cancel_requested",
                "start_migration",
                "phase1_running",
                "live_log_placeholder"
            ]
    
            for k in keys_to_clear:
                if k in st.session_state:
                    del st.session_state[k]
    
            # Navigate back to main
            st.session_state.page = "main"
            st.rerun()
    

    # --------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------
    progress_bar = st.progress(st.session_state.progress)

    # --------------------------------------------------------
    # LOADING ANIMATION (MIGRATING DATA…)
    # --------------------------------------------------------
    loading_placeholder = st.empty()

    def animate_loading():
        dots = ["", ".", "..", "..."]
        for d in dots:
            # Stop animation if done or cancelled
            if st.session_state.get("migration_finished", False) or st.session_state.cancel_requested:
                loading_placeholder.empty()
                return
            loading_placeholder.markdown(f"### ⏳ Migrating{d}")
            time.sleep(0.25)

    # --------------------------------------------------------
    # RUN MIGRATION (ONLY ON FIRST VISIT)
    # --------------------------------------------------------
    if st.session_state.get("start_migration", False):

        st.session_state.start_migration = False
        st.session_state.migration_finished = False   # Reset finish flag

        ui_log("Starting migration...")

        steps = [
            ("Migrating users…", lambda: migrate_users(st.session_state.phase1_active_only)),
            ("Migrating spaces…", migrate_spaces),
            ("Migrating memberships…", migrate_memberships)
        ]

        total_steps = len(steps)
        pct = int(100 / total_steps)

        # Run step-by-step
        for i, (label, fn) in enumerate(steps):
            if st.session_state.cancel_requested:
                break

            ui_log(label)
            animate_loading()  # visual animation
            fn()  # actual migration work

            st.session_state.progress = (i + 1) * pct
            progress_bar.progress(st.session_state.progress)

        # FINISHED SUCCESSFULLY
        if not st.session_state.cancel_requested:
            st.session_state.progress = 100
            progress_bar.progress(100)
            ui_log("Migration Complete!")
        
            # Store end time
            st.session_state.summary["end_time"] = datetime.utcnow()
        
            # Navigate to summary page
            st.session_state.page = "summary"
            st.rerun()


    # --------------------------------------------------------
    # SHOW CONSOLE OUTPUT
    # --------------------------------------------------------
    st.subheader("Live Console Output")

    st.text_area(
        "Console",
        st.session_state.get("log_output", ""),
        height=400,
        disabled=True
    )

elif st.session_state.page == "summary":

    st.header("Migration Completed Successfully")

    s = st.session_state.summary

    st.subheader("Migration Summary")

    st.markdown(f"""
    **Users Migrated:** {s['users_migrated']}  
    **Users Skipped:** {s['users_skipped']}  
    **Spaces Created:** {s['spaces_created']}  
    **Spaces Skipped:** {s['spaces_skipped']}  
    **Memberships Added:** {s['memberships_added']}  
    **Start Time:** {s['start_time']}  
    **End Time:** {s['end_time']}
    """)

    st.markdown("---")

    # ✅ Now put FULL CONSOLE LOG here (and ONLY here)
    st.subheader("Full Console Log")

    st.text_area(
        "Log Output",
        st.session_state.get("log_output", ""),
        height=300
    )

    has_logs = bool(st.session_state.get("log_output"))

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("✔ Finish", key="finish_button"):
            for key in [
                "progress", "log_output", "migration_finished", "cancel_requested",
                "start_migration", "phase1_running", "live_log_placeholder",
                "summary"
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.page = "main"
            st.rerun()

    with col2:
        if has_logs:
            st.download_button(
                "⬇ Download Logs",
                st.session_state["log_output"],
                file_name="migration_logs.txt",
                mime="text/plain"
            )
        else:
            st.markdown(
                "<div style='opacity:0.4; text-align:center; padding-top:10px;'>No logs yet</div>",
                unsafe_allow_html=True
            )

