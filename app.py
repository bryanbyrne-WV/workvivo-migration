
# -*- coding: utf-8 -*-
import streamlit as st
import requests
import time
import io
from datetime import datetime
import random
import os
import mimetypes

if "config_test_passed" not in st.session_state:
    st.session_state.config_test_passed = False

def get_api_url_from_workvivo_id(wv_id: str):
    """Return correct API base URL based on Workvivo ID prefix."""
    if not wv_id or len(wv_id) < 3:
        return "https://api.workvivo.com/v1"

    prefix = str(wv_id).strip()[:3]

    if prefix == "300":
        return "https://api.eu2.workvivo.com/v1"
    if prefix == "100":
        return "https://api.workvivo.us/v1"
    if prefix == "400":
        return "https://api.us2.workvivo.us/v1"

    return "https://api.workvivo.com/v1"

def test_workvivo_connection(scim_url, scim_token, api_url, api_token, wv_id):
    """Return (ok, message) with safe, non-detailed error responses."""

    headers_scim = {
        "Authorization": f"Bearer {scim_token}",
        "Accept": "application/json"
    }

    headers_api = {
        "Authorization": f"Bearer {api_token}",
        "Workvivo-Id": wv_id,
        "Accept": "application/json"
    }

    # ---- Test SCIM ----
    try:
        r = requests.get(f"{scim_url}?count=1", headers=headers_scim, timeout=6)

        if r.status_code == 401 or r.status_code == 403:
            return False, "❌ Invalid SCIM token"

        if r.status_code not in (200, 201):
            return False, "❌ SCIM authentication failed"
    except Exception:
        return False, "❌ SCIM connection failed"

    # ---- Test API ----
    try:
        r = requests.get(f"{api_url}/spaces?take=1", headers=headers_api, timeout=6)

        if r.status_code == 401 or r.status_code == 403:
            return False, "❌ Invalid API token"

        if r.status_code not in (200, 201):
            return False, "❌ API authentication failed"
    except Exception:
        return False, "❌ API connection failed"

    return True, "✅ All tests passed! API & SCIM are valid."

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
                margin: 1.5rem auto 2rem auto;
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

    # Centered Workvivo logo above login form
    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
            <img src="https://d3lkrqe5vfp7un.cloudfront.net/images/Picture4.png"
             style="height:170px;">
    </div>
    """, unsafe_allow_html=True)
        

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

    st.markdown(
        """
        <a class="request-button"
           href="https://support.workvivo.com/hc/en-gb/requests/new"
           target="_blank">
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
WORKVIVO_LOGO_URL = "https://d3lkrqe5vfp7un.cloudfront.net/images/Picture4.png"

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
    <img src="https://d3lkrqe5vfp7un.cloudfront.net/images/Picture4.png" 
         style="height:140px;">
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

        # ============================================================
# CLEAN CONFIG FORM — FINAL WORKING VERSION
# ============================================================

# Ensure test flag exists
if "config_test_passed" not in st.session_state:
    st.session_state.config_test_passed = False

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

            SOURCE_BASE_URL = st.text_input(
                "Source Workvivo URL",
                value="wv-migration2.workvivo.com",
                help="Enter your Workvivo domain (e.g. organisation.workvivo.com)"
            )

            SOURCE_SCIM_TOKEN = st.text_input(
                "Source SCIM Token",
                value="9BdzwvLUw0C8gZTE9ZWv6sd4K9thRMdWdUeZdSv1",
                type="password",
                help="Authentication token for SCIM user requests in the SOURCE tenant."
            )
            
            SOURCE_API_TOKEN = st.text_input(
                "Source API Token",
                value="388|636f9f76e508ae9fde1530f987080c9b275a4371",
                type="password",
                help="Bearer token used for API calls to retrieve content and metadata from the SOURCE tenant."
            )


            SOURCE_WORKVIVO_ID = st.text_input(
                "Source Workvivo ID",
                value="1584",
                help="Workvivo ID required for API requests on the SOURCE tenant."
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # TARGET ENVIRONMENT
        # ----------------------------------------------------
        st.markdown("<div class='config-card'>", unsafe_allow_html=True)
        with st.expander("Target Environment", expanded=True):
        
            TARGET_BASE_URL = st.text_input(
                "Target Workvivo URL",
                value="migration-test-1.workvivo.com",
                help="Enter your Workvivo domain (e.g. organisation.workvivo.com)"
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
        # VALIDATION
        # ----------------------------------------------------
        errors = []

        # Required source fields
        if not SOURCE_BASE_URL:
            errors.append("Source Workvivo URL is required.")
        if not SOURCE_SCIM_TOKEN:
            errors.append("Source SCIM Token is required.")
        if not SOURCE_API_TOKEN:
            errors.append("Source API Token is required.")
        if not SOURCE_WORKVIVO_ID:
            errors.append("Source Workvivo ID is required.")

        # Required target fields
        if not TARGET_BASE_URL:
            errors.append("Target Workvivo URL is required.")
        if not TARGET_SCIM_TOKEN:
            errors.append("Target SCIM Token is required.")
        if not TARGET_API_TOKEN:
            errors.append("Target API Token is required.")
        if not TARGET_WORKVIVO_ID:
            errors.append("Target Workvivo ID is required.")

        # Show warnings
        if errors:
            for e in errors:
                st.warning("⚠️ " + e)

        # ----------------------------------------------------
        # SUPPORT NOTE
        # ----------------------------------------------------
        st.markdown("""
        <div style="margin-top: 20px; padding: 12px; background: #f4ecff; 
        border-left: 4px solid #6203ed; border-radius: 6px;">
        <strong>Need help?</strong><br>
        If you cannot find any of this information, please contact 
        <a href="mailto:support@workvivo.com">support@workvivo.com</a>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")


        # ----------------------------------------------------
        # TEST CONFIGURATION BUTTON
        # ----------------------------------------------------
        st.markdown("### Test Connectivity")

        test_clicked = st.form_submit_button("Test Configuration")

        if test_clicked:

            clean_source = SOURCE_BASE_URL.replace("https://", "").replace("http://", "").strip("/")
            clean_target = TARGET_BASE_URL.replace("https://", "").replace("http://", "").strip("/")

            source_scim_test = f"https://{clean_source}/scim/v2/scim/Users/"
            target_scim_test = f"https://{clean_target}/scim/v2/scim/Users/"

            source_api_test = get_api_url_from_workvivo_id(SOURCE_WORKVIVO_ID)
            target_api_test = get_api_url_from_workvivo_id(TARGET_WORKVIVO_ID)

            st.info("Running tests…")

            ok1, msg1 = test_workvivo_connection(
                source_scim_test, SOURCE_SCIM_TOKEN, source_api_test, SOURCE_API_TOKEN, SOURCE_WORKVIVO_ID
            )
            st.write("Source Test:", msg1)

            ok2, msg2 = test_workvivo_connection(
                target_scim_test, TARGET_SCIM_TOKEN, target_api_test, TARGET_API_TOKEN, TARGET_WORKVIVO_ID
            )
            st.write("Target Test:", msg2)

            if ok1 and ok2:
                st.success("All configuration tests passed!")
                st.session_state.config_test_passed = True
            else:
                st.error("⚠️ One or more tests failed.")
                st.session_state.config_test_passed = False


        # ----------------------------------------------------
        # SAVE CONFIG BUTTON — DISABLED UNTIL TEST PASSES
        # ----------------------------------------------------
        st.markdown('<div class="purple-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "Save Configuration",
            disabled=(len(errors) > 0) or (not st.session_state.config_test_passed)
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # OUTSIDE THE FORM — PROCESS SAVE
    # ----------------------------------------------------
    if submitted:

        clean_source = SOURCE_BASE_URL.replace("https://", "").replace("http://", "").strip("/")
        st.session_state["SOURCE_SCIM_URL"] = f"https://{clean_source}/scim/v2/scim/Users/"

        clean_target = TARGET_BASE_URL.replace("https://", "").replace("http://", "").strip("/")
        st.session_state["TARGET_SCIM_URL"] = f"https://{clean_target}/scim/v2/scim/Users/"

        st.session_state["SOURCE_API_URL"] = get_api_url_from_workvivo_id(SOURCE_WORKVIVO_ID)
        st.session_state["TARGET_API_URL"] = get_api_url_from_workvivo_id(TARGET_WORKVIVO_ID)

        st.session_state["SOURCE_SCIM_TOKEN"] = SOURCE_SCIM_TOKEN
        st.session_state["SOURCE_API_TOKEN"] = SOURCE_API_TOKEN
        st.session_state["SOURCE_WORKVIVO_ID"] = SOURCE_WORKVIVO_ID

        st.session_state["TARGET_SCIM_TOKEN"] = TARGET_SCIM_TOKEN
        st.session_state["TARGET_API_TOKEN"] = TARGET_API_TOKEN
        st.session_state["TARGET_WORKVIVO_ID"] = TARGET_WORKVIVO_ID

        st.session_state["SPACE_CREATOR_EXTERNAL_ID"] = "workvivo-migration-user"
        st.session_state["config_saved"] = True

        st.success("Configuration saved! Click Continue to proceed.")

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

# Track newly created users + spaces
if "new_users" not in st.session_state:
    st.session_state.new_users = set()

if "new_spaces" not in st.session_state:
    st.session_state.new_spaces = set()


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

    if "log_output" not in st.session_state:
        st.session_state["log_output"] = ""

    st.session_state["log_output"] += line + "\n"

    if "live_log_placeholder" in st.session_state:

        # Convert newlines to <br> so each log is on its own line
        log_html = st.session_state["log_output"].replace("\n", "<br>")

        st.session_state.live_log_placeholder.markdown(
            f"<pre style='height:400px; overflow-y: scroll; background-color:#111; color:#eee; padding:10px; border-radius:6px;'>{log_html}</pre>",
            unsafe_allow_html=True
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

def pretty_time(dt):
    if not dt:
        return ""
    return dt.strftime("%B %-d, %Y %H:%M")  # e.g. "November 25, 2025 14:05"

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
def load_target_user_maps():
    """Fetch all target users and return:
    - email → externalId
    - externalId → email
    """
    users = paginated_fetch(f"{TARGET_API_URL}/users", target_headers)

    email_map = {}
    ext_map = {}

    for u in users:
        email = (u.get("email") or u.get("userName") or "").lower().strip()
        ext = (u.get("external_id") or "").strip()

        if email:
            email_map[email] = ext
        if ext:
            ext_map[ext] = email

    return email_map, ext_map


def migrate_users(active_only):
    ui_log("=== USER MIGRATION START ===")

    # Load existing target users
    target_email_map, target_ext_map = load_target_user_maps()

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
        
                # ----------------------------------------------
        # SKIP if email already exists in target
        # ----------------------------------------------
        if email in target_email_map:
            skipped += 1
            st.session_state.summary["users_skipped"] += 1
            ui_log(f"⏭ Skipped {email}: already exists in target (email match)")
            continue
        
        # ----------------------------------------------
        # SKIP if externalId already exists in target
        # ----------------------------------------------
        if ext and ext in target_ext_map:
            skipped += 1
            st.session_state.summary["users_skipped"] += 1
            ui_log(f"⏭ Skipped {email}: already exists in target (extId match)")
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
            st.session_state.new_users.add(ext)      # ⭐ NEW LINE
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

        # Skip avatar upload unless user was newly created
        if ext not in st.session_state.new_users:
            ui_log(f"⏭ Skipping avatar: user existed already ({ext})")
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

        if resp.status_code in (200, 201):
            created += 1
            st.session_state.summary["spaces_created"] += 1
            new_space_id = resp.json()["data"]["id"]     # ⭐ NEW
            st.session_state.new_spaces.add(new_space_id) # ⭐ NEW
            ui_log(f"✅ Created space '{name}'")
        else:
            ui_log(f"❌ Failed creating '{name}': {resp.text}")
        

    ui_log(f"=== SPACE MIGRATION END — created={created}, skipped={skipped} ===")


# =========================================================
# PHASE 1C — MEMBERSHIPS
# =========================================================
def migrate_memberships():
    ui_log("=== MEMBERSHIP MIGRATION START ===")

    # 1) Fetch source spaces
    source_spaces = paginated_fetch(
        f"{SOURCE_API_URL}/spaces",
        source_headers
    )

    # 2) Fetch target spaces
    target_spaces = paginated_fetch(
        f"{TARGET_API_URL}/spaces",
        target_headers
    )

    name_to_target_id = {
        s["name"].strip().lower(): s["id"]
        for s in target_spaces
    }

    # 3) Fetch target users → map ext → numeric
    target_users = paginated_fetch(
        f"{TARGET_API_URL}/users",
        target_headers
    )

    ext_to_numeric = {
        u.get("external_id"): u.get("id")
        for u in target_users
        if u.get("external_id")
    }

    for space in source_spaces:
        space_name = space["name"].strip()
        norm_name = space_name.lower()

        target_space_id = name_to_target_id.get(norm_name)
        if not target_space_id:
            ui_log(f"⚠️ No target match for space '{space_name}', skipping.")
            continue

        # 4) Fetch members of this space from source
        members = paginated_fetch(
            f"{SOURCE_API_URL}/spaces/{space['id']}/users",
            source_headers
        )

        numeric_ids = []

        for m in members:
            ext = (
                (m.get("user") or {}).get("external_id")
                or m.get("external_id")
            )

            if not ext:
                continue

            target_uid = ext_to_numeric.get(ext)
            if target_uid:
                numeric_ids.append(target_uid)

        ui_log(f"👥 '{space_name}': {len(numeric_ids)} members mapped")

        # Skip membership unless space was newly created
        if target_space_id not in st.session_state.new_spaces:
            ui_log(f"⏭ Skipping memberships for existing space '{space_name}'")
            continue

        # 5) PATCH memberships to target
        for chunk in [numeric_ids[i:i+100] for i in range(0, len(numeric_ids), 100)]:
            resp = requests.patch(
                f"{TARGET_API_URL}/spaces/{target_space_id}/users",
                headers=target_headers,
                json={"ids_to_add": chunk}
            )

            if resp.status_code in (200, 201):
                ui_log(f"   ✅ Added {len(chunk)} members")
            else:
                ui_log(f"   ❌ Failed patch: {resp.text[:150]}")

    ui_log("=== MEMBERSHIP MIGRATION END ===")


# =========================================================
# GLOBAL SPACE CREATION (PRIVATE) + ENROLLMENT
# =========================================================
def create_global_space_and_enroll(company_name):

    # 🔹 If reusing existing Global Feed, don't recreate
    if st.session_state.get("use_existing_global") and st.session_state.get("existing_global_id"):
        space_id = st.session_state.existing_global_id
        ui_log(f"🔁 Reusing existing Global Feed → Space ID {space_id}")
        return space_id

    # 🚫 Missing company name
    if not company_name or not company_name.strip():
        ui_log("⏭ Skipping Global Feed — no company name entered.")
        return None

    ui_log(f"🌍 Creating Global Feed: {company_name}")

    global_name = f"{company_name} Global Feed"

    # Check for existing space by name
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

    # ----------------------------------------------------
    # ⭐ NEW: ONLY enroll users created in this migration
    # ----------------------------------------------------

    new_user_ext_ids = st.session_state.new_users  # set of ext IDs

    all_target_users = paginated_fetch(f"{TARGET_API_URL}/users", target_headers)

    # Map external → numeric
    ext_to_numeric = {
        u.get("external_id"): u.get("id")
        for u in all_target_users
        if u.get("external_id")
    }

    # Only numeric IDs of newly created users
    numeric_ids = [
        ext_to_numeric[ext]
        for ext in new_user_ext_ids
        if ext in ext_to_numeric
    ]

    ui_log(f"👥 Enrolling {len(numeric_ids)} newly created users…")

    # Chunk & enroll
    chunks = [numeric_ids[i:i + 100] for i in range(0, len(numeric_ids), 100)]

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

        # 1) Global Space
        check_cancel()
        create_global_space_and_enroll(company_name)

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

    # ⭐ Add separator line (same style as other sections)
    st.markdown("---")

    
    # ============================================================
    # 🏢 Organisation settings and information
    # ============================================================
    st.markdown("### Organisation settings and information")
    st.markdown("This section migrates users, spaces and space membership.")
    
    # Users & Spaces (always on)
    migrate_users_flag = st.toggle("Users", value=True, disabled=True)
    migrate_spaces_flag = st.toggle("Spaces", value=True, disabled=True)
    
    # -----------------------------------------------------------
    # ALPHA: Selective User Migration
    # -----------------------------------------------------------
    st.markdown("#### Selective User Migration (Alpha Feature)")
    
    if "use_selected_users" not in st.session_state:
        st.session_state.use_selected_users = False
    if "selected_user_ids" not in st.session_state:
        st.session_state.selected_user_ids = ""
    
    st.session_state.use_selected_users = st.checkbox(
        "Migrate only selected users",
        value=st.session_state.use_selected_users,
        help="Enable this to migrate only the users whose external IDs you input."
    )
    
    if st.session_state.use_selected_users:
        selected_ids_text = st.text_area(
            "Enter external IDs (comma-separated)",
            value=st.session_state.selected_user_ids,
            placeholder="e.g. 12345, abcde-1002, ext_88991"
        )
    
        # Store in state
        st.session_state.selected_user_ids = selected_ids_text
    
        st.info("Only these users will be migrated.")
    else:
        st.session_state.selected_user_ids = ""

    st.markdown("---")


      # -----------------------------------------------------------
    # Company Name Prompt (for Global Feed creation)
    # -----------------------------------------------------------
    st.markdown("#### Global Feed Options")
    
    # Ensure keys exist
    if "phase1_company" not in st.session_state:
        st.session_state.phase1_company = ""
    
    if "use_existing_global" not in st.session_state:
        st.session_state.use_existing_global = False
    
    if "existing_global_id" not in st.session_state:
        st.session_state.existing_global_id = ""
    
    # --- LOCAL variable that drives UI immediately ---
    use_existing = st.checkbox(
        "Use existing Global Feed Space from a previous migration?",
        value=st.session_state.use_existing_global
    )
    
    # --- ORGANISATION NAME INPUT ---
    if use_existing:
        # Greyed-out version
        st.text_input(
            "Enter the organisation name for the Global Feed",
            value=st.session_state.phase1_company,
            placeholder="Disabled when using an existing Global Feed Space",
            disabled=True
        )
    else:
        # Editable version
        new_company = st.text_input(
            "Enter the organisation name for the Global Feed",
            value=st.session_state.phase1_company,
            placeholder="Example: Workvivo, Zoom, etc..."
        )
        st.session_state.phase1_company = new_company
    
        if not new_company:
            st.warning("Required on the first migration to create the Global Feed Space.")
    
    # --- GLOBAL FEED SPACE ID INPUT (ONLY WHEN REUSING) ---
    if use_existing:
        new_id = st.text_input(
            "Enter the Global Feed Space ID",
            value=st.session_state.existing_global_id,
            placeholder="Example: 279184"
        )
        st.session_state.existing_global_id = new_id
    else:
        st.session_state.existing_global_id = ""
    
    # --- Update session state AFTER UI renders ---
    st.session_state.use_existing_global = use_existing
    
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
    
    # Invisible scroll anchor
    scroll_anchor = st.empty()
    scroll_anchor.markdown("<div id='top'></div>", unsafe_allow_html=True)

        # Force scroll to the anchor
    st.components.v1.html(
        """
        <script>
            var topElement = window.parent.document.querySelector("div[id='top']");
            if (topElement) {
                topElement.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        </script>
        """,
        height=0,
    )

    

    # --------------------------------------------------------
    # HEADER LOGIC
    # --------------------------------------------------------
    if st.session_state.get("migration_finished", False):
        st.header("Migration Finished!")
    
    elif st.session_state.cancel_requested:
        st.header("Migration Cancelled")
    
    else:
        st.header("Migration In Progress...")
    
        # 🔥 Create the live log placeholder once on the running page
        if "live_log_placeholder" not in st.session_state:
            st.session_state.live_log_placeholder = st.empty()




    # --------------------------------------------------------
    # CANCEL vs FINISH BUTTON
    # --------------------------------------------------------
    if not st.session_state.get("migration_finished", False) and not st.session_state.cancel_requested:
        # Migration is still running
        if st.button("CANCEL"):
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
            ("Migrating user avatars…", migrate_user_images),
            ("Migrating spaces…", migrate_spaces),
            ("Migrating memberships…", migrate_memberships),
            ("Creating Global Feed…", lambda: create_global_space_and_enroll(st.session_state.phase1_company)),
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

    s = st.session_state.summary

    # ======= PAGE TITLE =======
    title_text = (
        "Migration Completed Successfully!!"
        if st.session_state.get("summary_type") != "cancelled"
        else "Migration Cancelled"
    )

    st.markdown(f"""
    <style>
        .summary-title {{
            font-size: 40px;
            font-weight: 800;
            color: #000000;
            text-align: center;
            margin-bottom: 10px;
            margin-top: 5px;
        }}

        .section-header {{
            font-size: 22px;
            font-weight: 700;
            color: #6203ed;            /* purple */
            margin-top: 25px;
            margin-bottom: 6px;
        }}

        .summary-item {{
            font-size: 16px;
            color: #000;
            padding: 2px 0;
        }}

        .divider {{
            border-top: 1px solid #ddd;
            margin: 18px 0;
        }}
    </style>

    <div class="summary-title">{title_text}</div>
    """, unsafe_allow_html=True)

    # -------- USERS & SPACES --------
    st.markdown("<div class='section-header'>Users & Spaces</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-item"><strong>Users Migrated:</strong> {s['users_migrated']}</div>
    <div class="summary-item"><strong>Spaces Created:</strong> {s['spaces_created']}</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # -------- CONTENT MIGRATED --------
    st.markdown("<div class='section-header'>Content Migrated</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-item"><strong>Updates Migrated:</strong> {s.get('updates_migrated', 0)}</div>
    <div class="summary-item"><strong>Kudos' Migrated:</strong> {s.get('kudos_migrated', 0)}</div>
    <div class="summary-item"><strong>Articles Migrated:</strong> {s.get('articles_migrated', 0)}</div>
    <div class="summary-item"><strong>Events Migrated:</strong> {s.get('events_migrated', 0)}</div>
    <div class="summary-item"><strong>Global Pages Migrated:</strong> {s.get('global_pages_migrated', 0)}</div>
    <div class="summary-item"><strong>Space Pages Migrated:</strong> {s.get('space_pages_migrated', 0)}</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # -------- TIMELINE --------
    st.markdown("<div class='section-header'>Migration Timeline</div>", unsafe_allow_html=True)
    
    start_pretty = pretty_time(s['start_time'])
    end_pretty = pretty_time(s['end_time'])
    
    st.markdown(f"""
    <div class="summary-item"><strong>Start:</strong> {start_pretty}</div>
    <div class="summary-item"><strong>End:</strong> {end_pretty}</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


    # -------- FULL LOG --------
    st.markdown("<div class='section-header'>Full Console Log</div>", unsafe_allow_html=True)

    st.text_area(
        "Console Output",
        st.session_state.get("log_output", ""),
        height=300
    )

    # ======== BUTTON ROW ========
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("✔ Finish", key="finish_button"):

            keys_to_reset = [
                # Migration progress & logs
                "progress", "log_output", "migration_finished", "cancel_requested",
                "start_migration", "phase1_running", "live_log_placeholder",
                "summary", "summary_type",

                # Migration page inputs
                "phase1_company",
                "migration_date_choice",
                "migration_start_date",
                "migration_end_date",

                # Toggles
                "migrate_updates", "migrate_kudos", "migrate_articles",
                "migrate_events", "migrate_comments", "migrate_likes",
                "migrate_globalPages", "migrate_spacePages",
                "phase1_active_only",
            ]

            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.page = "main"
            st.rerun()

    with c2:
        if st.session_state.get("log_output"):
            st.download_button(
                "⬇ Download Logs",
                st.session_state["log_output"],
                file_name="migration_logs.txt",
                mime="text/plain"
            )
        else:
            st.markdown(
                "<div style='opacity:0.4;'>No logs available</div>",
                unsafe_allow_html=True
            )
