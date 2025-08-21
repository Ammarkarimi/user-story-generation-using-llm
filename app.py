import streamlit as st
import re
from main import (
    findStakeholder,
    generateElicitationTechniques,
    justificationElicitationTechnique,
    generateUserStories,
    checkInvestFramework,
    Prioritize,
    findEpicConflict
)

st.set_page_config(page_title="Requirement Engineering Assistant", layout="wide")

st.title("📌 Requirement Engineering Assistant")
st.write("End-to-End Assistant for Stakeholder Analysis, Elicitation, User Stories, Validation, and Prioritization")

# ---------------------------
# Utility: Validate GROQ API key
# ---------------------------
def validate_groq_api_key(api_key: str) -> bool:
    """
    Validate Groq API key format.
    Must start with 'gsk_' and followed by 40–60 alphanumeric chars.
    """
    pattern = r"^gsk_[A-Za-z0-9]{40,60}$"
    return bool(re.match(pattern, api_key))

# ---------------------------
# Step 0: API Key Input
# ---------------------------
# Step 0: API Key Input (with instructions)
st.sidebar.header("🔑 API Key Configuration")

st.sidebar.info(
    "Don’t have a GROQ API key yet? You can create one by visiting "
    "[Groq Console – API Keys](https://console.groq.com/keys). "
    "Once there, log in, go to **API Keys**, click **Create API Key**, "
    "copy the resulting `gsk_*` key and paste it here."
)
api_key = st.sidebar.text_input("Enter your GROQ API Key", type="password")


if api_key:
    if validate_groq_api_key(api_key):
        st.session_state["api_key"] = api_key

        # Step 1: Problem Statement Input
        problem_statement = st.text_area(
            "✍️ Enter Problem Statement", 
            height=150, 
            placeholder="e.g., Create a system to build LLM"
        )

        if st.button("🔍 Analyze Stakeholders"):
            with st.spinner("Identifying stakeholders..."):
                stakeholders = findStakeholder(problem_statement, st.session_state["api_key"])
            st.subheader("👥 Stakeholders & End Users")
            st.write(stakeholders)
            st.session_state["stakeholders"] = stakeholders

        # Step 2: Elicitation Techniques
        if "stakeholders" in st.session_state:
            if st.button("📋 Generate Elicitation Techniques"):
                with st.spinner("Generating elicitation techniques..."):
                    elicitation = generateElicitationTechniques(
                        st.session_state["stakeholders"], st.session_state["api_key"]
                    )
                st.subheader("🛠️ Elicitation Techniques")
                st.write(elicitation)
                st.session_state["elicitation"] = elicitation

        # Step 3: Justification
        if "elicitation" in st.session_state:
            if st.button("✅ Justify Elicitation Techniques"):
                with st.spinner("Justifying elicitation techniques..."):
                    justification = justificationElicitationTechnique(
                        st.session_state["elicitation"], st.session_state["api_key"]
                    )
                st.subheader("📖 Justification for Techniques")
                st.write(justification)
                st.session_state["justification"] = justification

        # Step 4: Generate User Stories
        if "stakeholders" in st.session_state:
            if st.button("📝 Generate User Stories"):
                with st.spinner("Generating user stories..."):
                    user_stories = generateUserStories(
                        st.session_state["stakeholders"], st.session_state["api_key"]
                    )
                st.subheader("📘 User Stories")
                st.write(user_stories)
                st.session_state["user_stories"] = user_stories

        # Step 5: Validate with INVEST
        if "user_stories" in st.session_state:
            if st.button("🔎 Validate with INVEST"):
                with st.spinner("Validating with INVEST framework..."):
                    invest = checkInvestFramework(
                        st.session_state["user_stories"], st.session_state["api_key"]
                    )
                st.subheader("✅ INVEST Validation Results")
                st.write(invest)
                st.session_state["invest"] = invest

        # Step 6: Prioritize with MoSCoW
        if "invest" in st.session_state:
            if st.button("📊 Prioritize with MoSCoW"):
                with st.spinner("Prioritizing user stories..."):
                    prioritize = Prioritize(
                        st.session_state["invest"], st.session_state["api_key"]
                    )
                st.subheader("📌 MoSCoW Prioritization")
                st.write(prioritize)
                st.session_state["prioritize"] = prioritize

        # Step 7: Find EPIC Conflicts
        if "invest" in st.session_state:
            if st.button("⚡ Identify Epic Conflicts"):
                with st.spinner("Analyzing conflicts across EPICs..."):
                    conflicts = findEpicConflict(
                        st.session_state["invest"], st.session_state["api_key"]
                    )
                st.subheader("⚔️ EPIC Conflicts & Resolutions")
                st.write(conflicts)
                st.session_state["conflicts"] = conflicts
    else:
        st.error("❌ Invalid API key format. Must start with `gsk_` and contain 40–60 alphanumeric characters.")
else:
    st.warning("⚠️ Please enter your API key in the sidebar to continue.")
