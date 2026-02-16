import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from app.agents.graph import build_agent_graph, get_pruner
from app.utils.file_loader import extract_text_from_file
from app.utils import count_tokens

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Token-Diet Agent",
    page_icon="💸",
    layout="wide"
)

# -------------------------
# Session State Initialization
# -------------------------
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "total_savings" not in st.session_state:
    st.session_state.total_savings = 0.0
if "total_tokens_saved" not in st.session_state:
    st.session_state.total_tokens_saved = 0

# -------------------------
# Header
# -------------------------
st.title("💸 Token-Diet Agent")
st.caption(
    "An intelligent AI agent that reduces LLM costs by 60-80% through semantic pruning and dynamic model routing"
)

# -------------------------
# Sidebar: Session Analytics
# -------------------------
with st.sidebar:
    st.header("📊 Session Analytics")
    
    if st.session_state.query_history:
        st.metric("💰 Total Saved", f"${st.session_state.total_savings:.6f}")
        st.metric("✂️ Tokens Saved", f"{st.session_state.total_tokens_saved:,}")
        st.metric("📝 Queries Run", len(st.session_state.query_history))
        
        st.divider()
        
        # Cumulative savings chart
        if len(st.session_state.query_history) > 1:
            cumulative_savings = []
            running_total = 0
            for query in st.session_state.query_history:
                running_total += query["money_saved"]
                cumulative_savings.append(running_total)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=cumulative_savings,
                mode='lines+markers',
                name='Cumulative Savings',
                line=dict(color='#00cc88', width=3),
                marker=dict(size=8)
            ))
            fig.update_layout(
                title="Cumulative Cost Savings",
                yaxis_title="Savings ($)",
                xaxis_title="Query Number",
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state.query_history = []
            st.session_state.total_savings = 0.0
            st.session_state.total_tokens_saved = 0
            st.rerun()
    else:
        st.info("Run a query to see analytics")

# -------------------------
# Load Agent
# -------------------------
@st.cache_resource
def load_agent():
    return build_agent_graph()

agent = load_agent()

# -------------------------
# Main UI Layout
# -------------------------
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload a PDF or TXT file",
        type=["pdf", "txt"],
        help="The agent will extract text and index it for semantic search"
    )

with col_right:
    st.subheader("❓ Ask a Question")
    prompt = st.text_area(
        "Enter your question",
        placeholder="What is this document about?",
        height=100,
        help="The agent will analyze complexity and route to the optimal model"
    )
    
    # Live token counter
    if prompt:
        prompt_tokens = count_tokens(prompt)
        st.caption(f"📊 Query tokens: {prompt_tokens} | Estimated cost: ${prompt_tokens * 2.50 / 1_000_000:.6f}")

st.divider()

# -------------------------
# Run Agent
# -------------------------
if st.button("🚀 Run Token-Diet Agent", type="primary", use_container_width=True):
    if not uploaded_file or not prompt:
        st.warning("⚠️ Please upload a document and enter a question.")
    else:
        # Step 1: Document Processing
        st.subheader("📄 Step 1: Processing Document")
        
        with st.spinner("Extracting text from uploaded file..."):
            context = extract_text_from_file(uploaded_file)
            doc_tokens = count_tokens(context)
        
        st.success(f"✅ Extracted **{len(context):,}** characters (**{doc_tokens:,}** tokens)")
        
        with st.spinner("Building vector index for semantic search..."):
            pruner = get_pruner()  # Use the same pruner instance as the graph
            pruner.ingest_document(context)
        
        st.success("✅ Document indexed in ChromaDB")
        
        st.divider()
        
        # Step 2: Agent Execution
        st.subheader("🤖 Step 2: Running Agent Pipeline")
        
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
        
        # Run the agent
        with st.spinner("⚙️ Agent is processing your query..."):
            final_state = agent.invoke(initial_state)
        
        # Display all results AFTER completion (so they stay visible)
        st.success(f"✅ **Prune Node**: Reduced from **{final_state['original_token_count']:,}** to **{final_state['final_token_count']:,}** tokens (**{round((1 - final_state['final_token_count'] / final_state['original_token_count']) * 100, 1) if final_state['original_token_count'] > 0 else 0}%** reduction)")
        
        st.success(f"✅ **Route Node**: Selected **{final_state['chosen_model']}** based on query complexity")
        
        st.success(f"✅ **Execute Node**: Generated response using **{final_state['chosen_model']}**")
        
        quality_emoji = "🌟" if final_state['quality_score'] >= 8 else "✅" if final_state['quality_score'] >= 7 else "⚠️"
        quality_text = "Excellent!" if final_state['quality_score'] >= 8 else "Good" if final_state['quality_score'] >= 7 else "Needs improvement"
        st.success(f"{quality_emoji} **Judge Node**: Quality score **{final_state['quality_score']}/10** - {quality_text}")
        
        st.info(f"🎯 **Pipeline Summary**: Completed in **{final_state['iteration_count']}** iteration(s) with **${final_state['money_saved']:.6f}** saved")
        
        st.divider()
        
        # -------------------------
        # Agent Reasoning Breakdown
        # -------------------------
        with st.expander("🔍 Detailed Agent Reasoning Breakdown", expanded=True):
            st.markdown("### How the Agent Optimized This Query")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### 🔹 Prune Node")
                st.write(f"**Original Context**: {final_state['original_token_count']:,} tokens")
                st.write(f"**After Pruning**: {final_state['final_token_count']:,} tokens")
                st.write(f"**Reduction**: {final_state['original_token_count'] - final_state['final_token_count']:,} tokens removed")
                st.write(f"**Method**: Semantic similarity search using ChromaDB")
                
                st.markdown("#### 🔹 Execute Node")
                st.write(f"**LLM Used**: {final_state['chosen_model']}")
                st.write(f"**Tokens Sent**: {final_state['final_token_count']:,}")
                st.write(f"**Response Generated**: ✅ Success")
            
            with col_b:
                st.markdown("#### 🔹 Route Node")
                st.write(f"**Selected Model**: {final_state['chosen_model']}")
                
                # Explain why this model was chosen
                if "70b" in final_state['chosen_model'].lower():
                    st.write(f"**Reason**: Simple query detected")
                    st.write(f"**Strategy**: Use cost-efficient model")
                else:
                    st.write(f"**Reason**: Complex query detected")
                    st.write(f"**Strategy**: Use high-reasoning model")
                
                st.markdown("#### 🔹 Judge Node")
                st.write(f"**Quality Score**: {final_state['quality_score']}/10")
                st.write(f"**Evaluation**: {'✅ Excellent' if final_state['quality_score'] >= 8 else '✅ Good' if final_state['quality_score'] >= 7 else '⚠️ Needs improvement'}")
                st.write(f"**Action**: {'Accepted' if final_state['quality_score'] >= 7 else 'Retry with more context'}")
                st.write(f"**Iterations**: {final_state['iteration_count']}")
        
        st.divider()
        
        # -------------------------
        # Results Section
        # -------------------------
        st.subheader("📋 Results")
        
        # AI Response
        st.markdown("### 🤖 AI Response")
        # Show response length for debugging
        st.caption(f"📝 Response length: {len(final_state['response'])} characters")
        
        if final_state["response"] and len(final_state["response"]) > 0:
            # Use a simple text box that's guaranteed to show
            st.text_area(
                "AI Generated Response:",
                value=final_state["response"],
                height=200,
                disabled=True
            )
        else:
            st.error("⚠️ No response generated. The response field is empty.")
            st.write("**Debug Info:**")
            st.json({
                "response": final_state["response"],
                "response_type": type(final_state["response"]).__name__,
                "response_length": len(final_state["response"])
            })
        
        st.divider()
        
        # Key Metrics
        st.markdown("### 📊 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🧠 Model Selected",
                final_state["chosen_model"].split("-")[1] if "-" in final_state["chosen_model"] else final_state["chosen_model"],
                help="Router selected this model based on query complexity"
            )
        
        with col2:
            st.metric(
                "🧪 Quality Score",
                f'{final_state["quality_score"]}/10',
                help="Judge's evaluation of response quality"
            )
        
        with col3:
            st.metric(
                "🔁 Iterations",
                final_state["iteration_count"],
                help="Number of retry attempts (self-correction)"
            )
        
        with col4:
            token_reduction = round((1 - final_state["final_token_count"] / final_state["original_token_count"]) * 100, 1) if final_state["original_token_count"] > 0 else 0
            st.metric(
                "📉 Token Reduction",
                f"{token_reduction}%",
                help="Percentage of tokens pruned"
            )
        
        st.divider()
        
        # Token & Cost Analysis
        st.markdown("### 💰 Cost Analysis")
        
        col5, col6, col7 = st.columns(3)
        
        with col5:
            st.metric(
                "📉 Original Tokens",
                f"{final_state['original_token_count']:,}",
                help="Tokens before semantic pruning"
            )
        
        with col6:
            st.metric(
                "✂️ Final Tokens",
                f"{final_state['final_token_count']:,}",
                delta=f"-{final_state['original_token_count'] - final_state['final_token_count']:,}",
                delta_color="inverse",
                help="Tokens after semantic pruning"
            )
        
        with col7:
            st.metric(
                "💰 Money Saved",
                f"${final_state['money_saved']:.6f}",
                help="Cost savings from pruning and routing"
            )
        
        # Visualization: Token Comparison
        st.markdown("### 📊 Token Usage Visualization")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Without Token-Diet',
            x=['Token Count'],
            y=[final_state['original_token_count']],
            marker_color='#ff6b6b',
            text=[f"{final_state['original_token_count']:,}"],
            textposition='auto',
        ))
        
        fig.add_trace(go.Bar(
            name='With Token-Diet',
            x=['Token Count'],
            y=[final_state['final_token_count']],
            marker_color='#00cc88',
            text=[f"{final_state['final_token_count']:,}"],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Token Reduction Impact",
            yaxis_title="Tokens",
            barmode='group',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Update session history
        st.session_state.query_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": prompt,
            "model": final_state["chosen_model"],
            "original_tokens": final_state["original_token_count"],
            "final_tokens": final_state["final_token_count"],
            "money_saved": final_state["money_saved"],
            "quality_score": final_state["quality_score"]
        })
        
        st.session_state.total_savings += final_state["money_saved"]
        st.session_state.total_tokens_saved += (final_state["original_token_count"] - final_state["final_token_count"])
        
        st.success("✅ Query completed successfully! Check the sidebar for session analytics.")
