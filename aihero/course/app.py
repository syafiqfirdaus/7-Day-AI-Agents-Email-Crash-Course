import sys
import os

import sys
import os

# Force reinstall pydantic-ai if not found (best-effort). This runs once at import
# time when the module is missing. Streamlit deploys should install requirements,
# but this helps in case of transient missing package during startup.
try:
    import pydantic_ai
except Exception:
    try:
        import subprocess
        import site
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pydantic-ai-slim[openai]",
        ])
        # Reload site packages so that newly installed packages are importable
        import importlib

        importlib.reload(site)
        import pydantic_ai  # try import again
    except Exception:
        # If installation fails, continue — Streamlit will show the original ImportError
        pass

import streamlit as st
import asyncio
import os

import ingest
import search_agent
from logs import log_interaction_to_file  # Ensure logs.py defines this function


# -----------------------------
# Access control / secrets
# -----------------------------
# This app supports a simple email whitelist. Maintain the whitelist in
# Streamlit secrets (recommended) or in a local secrets file when self-hosting.
# Example `.streamlit/secrets.toml`:
#
# OPENAI_API_KEY = "sk-..."
#
# [whitelist]
# emails = ["alice@example.com", "bob@example.com"]

#

def is_whitelisted(email: str) -> bool:
    try:
        emails = st.secrets.get("whitelist", {}).get("emails", [])
        return email.lower() in [e.lower() for e in emails]
    except Exception:
        return False


def show_request_access_ui():
    st.info("This app is restricted. Please request access to use the assistant.")
    with st.form("request_access"):
        requester_email = st.text_input("Your email (so I can add you)")
        note = st.text_area("Optional message to the app owner", height=80)
        submitted = st.form_submit_button("Request access")
    if submitted and requester_email:
        st.success(
            "Thanks — your request has been noted. Send me a message with this email and I'll add you to the access list."
        )
        st.write("Request details:")
        st.write("- Email: ", requester_email)
        if note:
            st.write("- Note: ", note)


# --- Initialization ---
@st.cache_resource
def init_agent():
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    def filter(doc):
        return "data-engineering" in doc["filename"]

    st.write("🔄 Indexing repo...")
    index = ingest.index_data(repo_owner, repo_name, filter=filter)
    agent = search_agent.init_agent(index, repo_owner, repo_name)
    return agent


# --- Streamlit UI ---
st.set_page_config(page_title="AI FAQ Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI FAQ Assistant")
st.caption("Ask me anything about the DataTalksClub/faq repository")


# --- Simple auth gating ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.write("### Sign in / Request access")
    email = st.text_input("Enter your email to sign in")
    if st.button("Sign in") and email:
        if is_whitelisted(email):
            st.session_state.authenticated = True
            st.session_state.user_email = email
            # Some Streamlit versions don't expose experimental_rerun.
            # Strategy (best-effort):
            # 1. Use experimental_rerun if available (immediate rerun).
            # 2. Otherwise use the supported set_query_params API if present.
            # 3. Fall back to experimental_set_query_params for older versions.
            # 4. If nothing is available, ask the user to refresh manually.
            try:
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    import time

                    if hasattr(st, "set_query_params"):
                        # newer API (function)
                        st.set_query_params(_rerun=int(time.time()))
                    elif hasattr(st, "query_params"):
                        # preferred property-based API (no deprecation warning)
                        st.query_params = {"_rerun": int(time.time())}
                    elif hasattr(st, "experimental_set_query_params"):
                        # older, deprecated API (last resort)
                        st.experimental_set_query_params(_rerun=int(time.time()))
                    else:
                        st.warning("Signed in — please refresh the page to continue.")
            except Exception:
                # Best-effort: if rerun fails, the user can manually refresh.
                try:
                    st.warning("Signed in — please refresh the page to continue.")
                except Exception:
                    pass
        else:
            show_request_access_ui()
    else:
        show_request_access_ui()


if st.session_state.authenticated:
    # Load OPENAI_API_KEY from Streamlit secrets if present (server-side only)
    if "OPENAI_API_KEY" in st.secrets and os.environ.get("OPENAI_API_KEY") is None:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize agent lazily so secrets/env is set before pydantic_ai initializes
    agent = init_agent()

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    # --- Streaming helper ---
    def stream_response(prompt: str):
        async def agen():
            async with agent.run_stream(user_prompt=prompt) as result:
                last_len = 0
                full_text = ""
                async for chunk in result.stream_output(debounce_by=0.01):
                    # stream only the delta
                    new_text = chunk[last_len:]
                    last_len = len(chunk)
                    full_text = chunk
                    if new_text:
                        yield new_text
                # log once complete
                new_messages = result.new_messages()
                if isinstance(new_messages, tuple):
                    src = new_messages[1] if len(new_messages) > 1 else "user"
                    log_interaction_to_file(agent, new_messages[0], source=str(src))
                else:
                    log_interaction_to_file(agent, new_messages)
                st.session_state._last_response = full_text

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agen_obj = agen()

        try:
            while True:
                piece = loop.run_until_complete(agen_obj.__anext__())
                yield piece
        except StopAsyncIteration:
            return


    # --- Chat input ---
    if prompt := st.chat_input("Ask your question..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant message (streamed)
        with st.chat_message("assistant"):
            response_text = st.write_stream(stream_response(prompt))

        # Save full response to history
        final_text = getattr(st.session_state, "_last_response", response_text)
        st.session_state.messages.append({"role": "assistant", "content": final_text})
