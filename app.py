import streamlit as st
import pandas as pd
import json

from classifier import classify_usecase
from token_estimator import estimate_tokens
from cost_calculator import calculate_cost
from scoring_rules import SCORING


# ---------------------------------------------------
# Load model registry
# ---------------------------------------------------

with open("models.json") as f:
    models = json.load(f)


# ---------------------------------------------------
# Page config
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Model Advisor",
    layout="wide"
)

st.title("⚡ AI Model Advisor")

st.markdown(
"""
Describe your use case and compare LLMs based on:

• Task suitability  
• Estimated token usage  
• Cost  
• Speed  
• Context window
"""
)


# ---------------------------------------------------
# Example prompts
# ---------------------------------------------------

examples = [
    "Summarize a 200 page financial report",
    "Build a customer support chatbot using internal documentation",
    "Generate Python scripts from plain English instructions",
    "Analyze marketing campaign data and suggest improvements"
]

with st.expander("Try example prompts"):

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


# ---------------------------------------------------
# Main logic
# ---------------------------------------------------

if analyze:

    if not user_input.strip():

        st.warning("Please enter a use case.")

        st.stop()

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


        # -------------------------
        # Task score
        # -------------------------

        task_score = (
            SCORING["task_match"]
            if usecase in data["strengths"]
            else SCORING["task_partial"]
        )


        # -------------------------
        # Cost score
        # -------------------------

        if cost < SCORING["cost_thresholds"]["cheap"]:

            cost_score = SCORING["cost_scores"]["cheap"]

        elif cost < SCORING["cost_thresholds"]["medium"]:

            cost_score = SCORING["cost_scores"]["medium"]

        else:

            cost_score = SCORING["cost_scores"]["expensive"]


        # -------------------------
        # Speed score
        # -------------------------

        speed_score = SCORING["speed_scores"].get(data["speed"], 1)


        # -------------------------
        # Context window penalty
        # -------------------------

        context_penalty = (
            SCORING["context_penalty"]
            if input_tokens > data["context_window"]
            else 0
        )


        total_score = (
            task_score +
            cost_score +
            speed_score +
            context_penalty
        )


        rows.append({

            "Model": model_name,
            "Provider": data["provider"],
            "Task Fit": "Yes" if usecase in data["strengths"] else "Partial",
            "Speed": data["speed"],
            "Context Window": data["context_window"],
            "Estimated Cost ($)": cost,
            "Score": total_score

        })


    df = pd.DataFrame(rows)

    df = df.sort_values("Score", ascending=False)

    winner = df.iloc[0]


    # ---------------------------------------------------
    # Results
    # ---------------------------------------------------

    st.subheader("Recommended Model")

    st.success(
        f"{winner['Model']} ({winner['Provider']}) | Estimated cost ${winner['Estimated Cost ($)']:.4f}"
    )


    st.subheader("Model Comparison")

    st.dataframe(df, use_container_width=True)


    # ---------------------------------------------------
    # Explanation
    # ---------------------------------------------------

    with st.expander("How scoring works"):

        st.markdown("""

Task Match  
• Match = 5  
• Partial = 2  

Cost Score  
• Cheap (< $0.005) = 3  
• Medium (< $0.02) = 2  
• Otherwise = 1  

Speed Score  
• Fast = 2  
• Medium = 1  

Context Window  
• Penalty applied if estimated tokens exceed the model context window.

""")
