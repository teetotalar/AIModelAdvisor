import streamlit as st
import pandas as pd
from models import models
from classifier import classify_usecase
from token_estimator import estimate_tokens
from cost_calculator import calculate_cost

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Model Advisor",
    page_icon="⚡",
    layout="wide"
)

# ── Custom styling ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e0e1a; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    h1 { font-size: 2.4rem !important; font-weight: 800 !important; }
    .metric-card {
        background: #1a1a2e;
        border: 1px solid #2d2d50;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 8px;
    }
    .winner-card {
        background: linear-gradient(135deg, #1a1a3e, #12122a);
        border: 1px solid #6d28d9;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 16px 0 24px 0;
    }
    .winner-title { color: #a78bfa; font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; }
    .winner-name  { color: #ffffff; font-size: 1.8rem; font-weight: 800; margin: 4px 0 8px; }
    .winner-reason { color: #94a3b8; font-size: 0.9rem; line-height: 1.6; }
    .task-badge {
        display: inline-block;
        background: #2d1b6e;
        color: #a78bfa;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.78rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("⚡ AI Model Advisor")
st.markdown(
    "<p style='color:#64748b;font-size:1rem;margin-top:-8px;margin-bottom:28px'>"
    "Describe your use case. Get a neutral comparison of cost, speed, and fit across 6 leading models."
    "</p>",
    unsafe_allow_html=True
)

# ── Input ──────────────────────────────────────────────────────────────────────
examples = [
    "Summarize a 200-page financial report and extract key risks",
    "Build a customer support chatbot using internal documentation",
    "Generate Python scripts from plain English specifications",
    "Analyze marketing campaign performance data and suggest improvements",
]

with st.expander("💡 Try an example use case"):
    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state["prefill"] = ex

prefill = st.session_state.get("prefill", "")
user_input = st.text_area(
    "Describe your use case",
    value=prefill,
    height=120,
    placeholder='e.g. "I want to summarize a 200-page financial report and extract key risks"'
)

analyze = st.button("Analyze →", type="primary", use_container_width=True)

# ── Analysis ───────────────────────────────────────────────────────────────────
if analyze:
    if not user_input.strip():
        st.warning("Please describe a use case first.")
        st.stop()

    with st.spinner("Analyzing your use case…"):

        usecase      = classify_usecase(user_input)
        input_tokens = estimate_tokens(user_input)
        output_tokens = int(input_tokens * 0.5)

        rows = []
        for model_name, data in models.items():
            cost = calculate_cost(
                input_tokens, output_tokens,
                data["input_price"], data["output_price"]
            )

            # Task fit
            task_score = 5 if usecase in data["strengths"] else 2

            # Cost score (relative — lower is better)
            if cost < 0.005:   cost_score = 3
            elif cost < 0.02:  cost_score = 2
            else:              cost_score = 1

            # Speed score
            speed_score = 2 if data["speed"] == "Fast" else 1

            total_score = task_score + cost_score + speed_score

            rows.append({
                "Model":            model_name,
                "Provider":         data["provider"],
                "Task Fit":         "✅ Yes" if usecase in data["strengths"] else "➖ Partial",
                "Est. Cost ($)":    cost,
                "Speed":            data["speed"],
                "Context Window":   f"{data['context_window']:,}",
                "Input Tokens":     input_tokens,
                "Output Tokens":    output_tokens,
                "Pricing Note":     data["pricing_note"],
                # Hidden scoring columns (used for sort)
                "_total":           total_score,
                "_task":            task_score,
                "_cost":            cost_score,
                "_speed":           speed_score,
            })

        df = pd.DataFrame(rows).sort_values("_total", ascending=False).reset_index(drop=True)
        winner = df.iloc[0]

    # ── Summary stats ────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Detected Task",   usecase.capitalize())
    col2.metric("Input Tokens",    f"{input_tokens:,}")
    col3.metric("Output Tokens",   f"{output_tokens:,}")
    col4.metric("Models Evaluated","6")

    # ── Winner card ──────────────────────────────────────────────────────────
    reasons = []
    if winner["_task"] == 5:
        reasons.append(f"strong fit for {usecase} tasks")
    if winner["_cost"] == 3:
        reasons.append("lowest estimated cost")
    elif winner["_cost"] == 2:
        reasons.append("reasonable cost")
    if winner["Speed"] == "Fast":
        reasons.append("fast response speed")

    reason_str = " · ".join(reasons).capitalize() + "." if reasons else ""

    st.markdown(f"""
    <div class="winner-card">
        <div class="winner-title">🏆 Recommended Model</div>
        <div class="winner-name">{winner['Model']}</div>
        <div class="task-badge">{usecase}</div>
        <div class="winner-reason">
            <strong>{winner['Provider']}</strong> &nbsp;·&nbsp;
            Est. cost: <strong>${winner['Est. Cost ($)']:.4f}</strong> &nbsp;·&nbsp;
            Speed: <strong>{winner['Speed']}</strong><br>
            {reason_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Comparison table ─────────────────────────────────────────────────────
    st.subheader("Full Model Comparison")

    display_cols = ["Model", "Provider", "Task Fit", "Est. Cost ($)", "Speed", "Context Window", "Pricing Note"]
    display_df   = df[display_cols].copy()

    st.dataframe(
        display_df.style
            .format({"Est. Cost ($)": "${:.4f}"})
            .apply(lambda row: [
                "background-color: #1a1a3e; color: white;" if row.name == 0 else ""
                for _ in row
            ], axis=1)
            .set_properties(**{"font-size": "13px"}),
        use_container_width=True,
        hide_index=True,
    )

    # ── Scoring explainer ────────────────────────────────────────────────────
    with st.expander("How is the score calculated?"):
        st.markdown("""
        The recommendation is based on a transparent 3-factor score:

        | Factor | How it's scored |
        |---|---|
        | **Task Fit** | 5 pts if the model lists this task as a strength, 2 pts otherwise |
        | **Cost** | 3 pts if cost < $0.005 · 2 pts if < $0.02 · 1 pt otherwise |
        | **Speed** | 2 pts for Fast · 1 pt for Medium |

        The model with the highest total score is recommended.
        Token counts use OpenAI's `cl100k_base` tokenizer as a baseline.
        """)

    st.caption("Pricing based on publicly available API rates. Open-source model costs are estimated inference costs.")