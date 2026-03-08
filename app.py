import streamlit as st
import pandas as pd

from models import models
from classifier import classify_usecase
from token_estimator import estimate_tokens
from cost_calculator import calculate_cost


# -------------------------------------------------------
# Page configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Model Advisor",
    page_icon="⚡",
    layout="wide"
)


# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("⚡ AI Model Advisor")

st.markdown(
"""
Describe your GenAI use case and compare different LLMs based on  
**task suitability, estimated cost, speed, and context window.**
"""
)


# -------------------------------------------------------
# Example prompts
# -------------------------------------------------------

examples = [
    "Summarize a 200-page financial report and extract key risks",
    "Build a customer support chatbot using internal documentation",
    "Generate Python scripts from plain English specifications",
    "Analyze marketing campaign performance data and suggest improvements",
]

with st.expander("Try example use cases"):
    for ex in examples:
        if st.button(ex):
            st.session_state["prefill"] = ex


prefill = st.session_state.get("prefill", "")

user_input = st.text_area(
    "Describe your use case",
    value=prefill,
    height=120
)

analyze = st.button("Analyze")


# -------------------------------------------------------
# Main analysis
# -------------------------------------------------------

if analyze:

    if not user_input.strip():
        st.warning("Please enter a use case.")
        st.stop()

    with st.spinner("Analyzing use case..."):

        usecase = classify_usecase(user_input)

        input_tokens = estimate_tokens(user_input)

        output_tokens = int(input_tokens * 0.5)

        rows = []

        for model_name, data in models.items():

            cost = calculate_cost(
                input_tokens,
                output_tokens,
                data["input_price"],
                data["output_price"]
            )

            # -------------------------------
            # Task score
            # -------------------------------

            task_score = 5 if usecase in data["strengths"] else 2


            # -------------------------------
            # Cost score
            # -------------------------------

            if cost < 0.005:
                cost_score = 3
            elif cost < 0.02:
                cost_score = 2
            else:
                cost_score = 1


            # -------------------------------
            # Speed score
            # -------------------------------

            if data["speed"] == "Fast":
                speed_score = 2
            else:
                speed_score = 1


            # -------------------------------
            # Context window penalty
            # -------------------------------

            if input_tokens > data["context_window"]:
                context_penalty = -3
            else:
                context_penalty = 0


            total_score = task_score + cost_score + speed_score + context_penalty


            rows.append({
                "Model": model_name,
                "Provider": data["provider"],
                "Task Fit": "Yes" if usecase in data["strengths"] else "Partial",
                "Speed": data["speed"],
                "Context Window": data["context_window"],
                "Estimated Cost ($)": cost,
                "Total Score": total_score
            })


        df = pd.DataFrame(rows)

        df = df.sort_values("Total Score", ascending=False)

        winner = df.iloc[0]


# -------------------------------------------------------
# Results summary
# -------------------------------------------------------

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Detected Task", usecase)
    col2.metric("Input Tokens", input_tokens)
    col3.metric("Output Tokens", output_tokens)
    col4.metric("Models Evaluated", len(models))


# -------------------------------------------------------
# Recommendation
# -------------------------------------------------------

    st.subheader("Recommended Model")

    st.success(
        f"{winner['Model']} ({winner['Provider']})\n\n"
        f"Estimated cost: ${winner['Estimated Cost ($)']:.4f} | "
        f"Speed: {winner['Speed']}"
    )


# -------------------------------------------------------
# Comparison table
# -------------------------------------------------------

    st.subheader("Model Comparison")

    display_cols = [
        "Model",
        "Provider",
        "Task Fit",
        "Estimated Cost ($)",
        "Speed",
        "Context Window",
        "Total Score"
    ]

    st.dataframe(
        df[display_cols],
        use_container_width=True
    )


# -------------------------------------------------------
# Explanation
# -------------------------------------------------------

    with st.expander("How scoring works"):

        st.markdown(
        """
**Scoring factors**

| Factor | Score |
|------|------|
Task Fit | 5 if model specializes in this task, otherwise 2 |
Cost | 3 if < $0.005, 2 if < $0.02, otherwise 1 |
Speed | 2 for Fast, 1 for Medium |
Context Window | -3 penalty if input exceeds model context |

The model with the **highest total score** is recommended.

Token estimation uses the **OpenAI cl100k_base tokenizer** as a baseline approximation.
"""
        )


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.caption(
"Pricing estimates based on publicly available API rates. "
"Open-source models use approximate inference cost estimates."
)
