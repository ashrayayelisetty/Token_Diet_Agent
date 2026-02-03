import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from app.agents.graph import build_agent_graph
from app.utils.file_loader import extract_text_from_file
from app.services.pruner import SemanticPruner

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Token-Diet Agent",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Token-Diet Agent")
st.caption(
    "Upload a document and ask questions. "
    "The agent prunes irrelevant text to save tokens and cost."
)

# -------------------------
# Load Agent
# -------------------------
@st.cache_resource
def load_agent():
    return build_agent_graph()

agent = load_agent()

# -------------------------
# UI Layout
# -------------------------
st.subheader("📄 Upload Document")
uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

st.subheader("❓ Ask a Question")
prompt = st.text_area(
    "Enter your question",
    placeholder="What is this document about?"
)

st.divider()

# -------------------------
# Run Agent
# -------------------------
if st.button("🚀 Run Token-Diet Agent"):
    if not uploaded_file or not prompt:
        st.warning("Please upload a document and enter a question.")
    else:
        pruner = SemanticPruner()

    with st.spinner("Reading document..."):
        context = extract_text_from_file(uploaded_file)

    with st.spinner("Indexing document..."):
        pruner.ingest_document(context)

    with st.spinner("Agent is reasoning..."):
        initial_state = {
            "prompt": prompt,
            "context": context,
            "response": "",
            "quality_score": 0,
            "chosen_model": "",
            "original_token_count": 0,
            "final_token_count": 0,
            "money_saved": 0.0,
            "iteration_count": 0
        }

        final_state = agent.invoke(initial_state)


        st.success("✅ Agent completed successfully")

        # -------------------------
        # Output
        # -------------------------
        st.subheader("🤖 AI Response")
        st.write(final_state["response"])

        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric("🧠 Model Used", final_state["chosen_model"])
        col2.metric("🧪 Judge Score", f'{final_state["quality_score"]}/10')
        col3.metric("🔁 Iterations", final_state["iteration_count"])

        st.divider()

        col4, col5, col6 = st.columns(3)
        col4.metric("📉 Original Tokens", final_state["original_token_count"])
        col5.metric("✂️ Final Tokens", final_state["final_token_count"])
        col6.metric("💰 Money Saved ($)", final_state["money_saved"])
