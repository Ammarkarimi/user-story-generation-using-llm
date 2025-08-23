import streamlit as st
import re
import uuid
from datetime import datetime
from main import (
    findStakeholder,
    generateElicitationTechniques,
    justificationElicitationTechnique,
    generateUserStories,
    checkInvestFramework,
    Prioritize,
    findEpicConflict
)
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import re

# Get DB values from Streamlit secrets
DB_USER = st.secrets["user"]
DB_PASS = st.secrets["password"]
DB_HOST = st.secrets["host"]
DB_PORT = st.secrets["port"]
DB_NAME = st.secrets["dbname"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class UserLog(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    student_id = Column(String)   # new column
    model_name = Column(String)   # new column
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create table if it doesn’t exist
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def log_event(user_id, action, details):
    """Store user actions in Supabase logs table with student_id & model_name."""
    session = Session()
    log = UserLog(
        user_id=user_id,
        student_id=st.session_state.get("student_id", "unknown"),
        model_name=st.session_state.get("model_name", "default"),
        action=action,
        details=str(details)
    )
    session.add(log)
    session.commit()
    session.close()

def get_logs(limit=20):
    """Retrieve recent logs for debugging or admin view."""
    session = Session()
    logs = session.query(UserLog).order_by(UserLog.timestamp.desc()).limit(limit).all()
    session.close()
    return logs

regex_pattern = r'<think>[\s\S]*?</think>\n\n'
# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(page_title="Requirement Engineering Assistant", layout="wide")

st.title("📌 Requirement Engineering Assistant")
st.write("End-to-End Assistant for Stakeholder Analysis, Elicitation, User Stories, Validation, and Prioritization")

# ---------------------------
# Utility: Validate GROQ API key
# ---------------------------
def validate_groq_api_key(api_key: str) -> bool:
    """Validate Groq API key format."""
    pattern = r"^gsk_[A-Za-z0-9]{40,60}$"
    return bool(re.match(pattern, api_key))

# ---------------------------
# Sidebar: User Info + API Key
# ---------------------------
st.sidebar.header("🔑 API Key Configuration")

# Initialize model lock state
if "lock_model" not in st.session_state:
    st.session_state.lock_model = False
if "epic_done" not in st.session_state:
    st.session_state.epic_done = False

# Student ID
st.sidebar.subheader("👤 User Info")
st.session_state["student_id"] = st.sidebar.text_input(
    "Student ID", value=st.session_state.get("student_id", "")
)

# Model dropdown (locked after first selection until epic is completed)
model_options = ["qwen/qwen3-32b", "openai/gpt-oss-120b", "llama-3.3-70b-versatile"]

selected_model = st.sidebar.selectbox(
    "Select Model:",
    model_options,
    index=model_options.index(st.session_state.get("model_name", model_options[0])),
    key="model_name",
    disabled=st.session_state.lock_model
)

# Lock model once selected (if not already locked)
if st.session_state["model_name"] and not st.session_state.lock_model:
    st.session_state.lock_model = True

st.sidebar.info(
    "Don’t have a GROQ API key yet? You can create one by visiting "
    "[Groq Console – API Keys](https://console.groq.com/keys). "
    "Once there, log in, go to **API Keys**, click **Create API Key**, "
    "copy the resulting `gsk_*` key and paste it here."
)

api_key = st.sidebar.text_input("Enter your GROQ API Key", type="password")

# Assign unique user_id for session (for logging)
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

# ---------------------------
# Workflow
# ---------------------------
if api_key:
    if validate_groq_api_key(api_key):
        st.session_state["api_key"] = api_key
        log_event(st.session_state["user_id"], "api_key_entered", {"api_key": "[REDACTED]"})

        # Step 1: Problem Statement Input
        problem_statement = st.text_area(
            "✍️ Enter Problem Statement", 
            height=150, 
            placeholder="e.g., Create a system to build LLM"
        )

        if st.button("🔍 Analyze Stakeholders"):
            with st.spinner("Identifying stakeholders..."):
                stakeholders = findStakeholder(problem_statement, st.session_state["api_key"], st.session_state["model_name"])
            st.subheader("👥 Stakeholders & End Users")
            if st.session_state["model_name"]=="qwen/qwen3-32b":
                stakeholders = re.sub(regex_pattern, '', stakeholders)
            st.write(stakeholders)
            st.session_state["stakeholders"] = stakeholders
            log_event(st.session_state["user_id"], "analyze_stakeholders", {"problem": problem_statement, "result": stakeholders})

        # Step 2: Elicitation Techniques
        if "stakeholders" in st.session_state:
            if st.button("📋 Generate Elicitation Techniques"):
                with st.spinner("Generating elicitation techniques..."):
                    elicitation = generateElicitationTechniques(
                        st.session_state["stakeholders"], st.session_state["api_key"], st.session_state["model_name"]
                    )
                st.subheader("🛠️ Elicitation Techniques")
                if st.session_state["model_name"]=="qwen/qwen3-32b":
                    elicitation=re.sub(regex_pattern, '', elicitation)
                st.write(elicitation)
                st.session_state["elicitation"] = elicitation
                log_event(st.session_state["user_id"], "generate_elicitation", {"result": elicitation})

        # Step 3: Justification
        if "elicitation" in st.session_state:
            if st.button("✅ Justify Elicitation Techniques"):
                with st.spinner("Justifying elicitation techniques..."):
                    justification = justificationElicitationTechnique(
                        st.session_state["elicitation"], st.session_state["api_key"], st.session_state["model_name"]
                    )
                st.subheader("📖 Justification for Techniques")
                if st.session_state["model_name"]=="qwen/qwen3-32b":
                    justification=re.sub(regex_pattern, '', justification)
                st.write(justification)
                st.session_state["justification"] = justification
                log_event(st.session_state["user_id"], "justify_elicitation", {"result": justification})

        # Step 4: Generate User Stories
        if "stakeholders" in st.session_state:
            if st.button("📝 Generate User Stories"):
                with st.spinner("Generating user stories..."):
                    user_stories = generateUserStories(
                        st.session_state["stakeholders"], st.session_state["api_key"], st.session_state["model_name"]
                    )
                st.subheader("📘 User Stories")
                if st.session_state["model_name"]=="qwen/qwen3-32b":
                    user_stories=re.sub(regex_pattern, '', user_stories)
                st.write(user_stories)
                st.session_state["user_stories"] = user_stories
                log_event(st.session_state["user_id"], "generate_user_stories", {"result": user_stories})

        # Step 5: Validate with INVEST
        if "user_stories" in st.session_state:
            if st.button("🔎 Validate with INVEST"):
                with st.spinner("Validating with INVEST framework..."):
                    invest = checkInvestFramework(
                        st.session_state["user_stories"], st.session_state["api_key"],st.session_state["model_name"]
                    )
                st.subheader("✅ INVEST Validation Results")
                if st.session_state["model_name"]=="qwen/qwen3-32b":
                    invest = re.sub(regex_pattern, '', invest)
                st.write(invest)
                st.session_state["invest"] = invest
                log_event(st.session_state["user_id"], "invest_validation", {"result": invest})

        # Step 6: Prioritize with MoSCoW
        if "invest" in st.session_state:
            if st.button("📊 Prioritize with MoSCoW"):
                with st.spinner("Prioritizing user stories..."):
                    prioritize = Prioritize(
                        st.session_state["invest"], st.session_state["api_key"],st.session_state["model_name"]
                    )
                st.subheader("📌 MoSCoW Prioritization")
                if st.session_state["model_name"]=="qwen/qwen3-32b":
                    prioritize = re.sub(regex_pattern, '', prioritize)
                st.write(prioritize)
                st.session_state["prioritize"] = prioritize
                log_event(st.session_state["user_id"], "prioritize", {"result": prioritize})

        # Step 7: Find EPIC Conflicts
        if "invest" in st.session_state:
            if st.button("⚡ Identify Epic Conflicts"):
                with st.spinner("Analyzing conflicts across EPICs..."):
                    conflicts = findEpicConflict(
                        st.session_state["invest"], st.session_state["api_key"], st.session_state["model_name"]
                    )
                st.subheader("⚔️ EPIC Conflicts & Resolutions")
                if st.session_state["model_name"] == "qwen/qwen3-32b":
                    conflicts = re.sub(regex_pattern, '', conflicts)
                st.write(conflicts)
                st.session_state["conflicts"] = conflicts
                log_event(st.session_state["user_id"], "epic_conflicts", {"result": conflicts})

                # ✅ Unlock model after epic is shown
                st.session_state.lock_model = False
                st.session_state.epic_done = True


        # Admin: View Logs (optional, at bottom of sidebar)
        # with st.sidebar.expander("📜 View Recent Logs"):
        #     for log in get_logs(10):
        #         st.write(f"[{log.timestamp}] {log.student_id} | {log.model_name} | {log.action}: {log.details}")

    else:
        st.error("❌ Invalid API key format. Must start with `gsk_` and contain 40–60 alphanumeric characters.")
else:
    st.warning("⚠️ Please enter your API key in the sidebar to continue.")
