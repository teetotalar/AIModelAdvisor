# ⚡ AI Model Advisor

AI Model Advisor is a lightweight tool that helps compare different Large Language Models (LLMs) for a given use case.

Instead of guessing which model to use, the tool evaluates multiple models across **task suitability, estimated cost, speed, and context limits** to provide a transparent recommendation.

The goal is to act as a **neutral decision assistant** when selecting an appropriate model for a specific GenAI use case.

---

## 🌐 Live Demo

Streamlit App  
https://aimodeladvisor.streamlit.app

---

## 🚀 Why This Tool Exists

While experimenting with multiple LLMs, one simple question kept coming up:

**For a given use case, which model should we actually pick?**

Most modern LLMs are surprisingly capable across many tasks.  
However, for **enterprise adoption**, the decision often comes down to practical factors such as:

- Cost
- Token usage
- Response speed
- Context window limits

AI Model Advisor helps visualize these trade-offs and provides a **transparent comparison across models**.

---

## 🧠 Supported Models

The tool currently compares models from multiple providers:

- GPT-4o (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
- Gemini 1.5 Pro (Google)
- Llama 3 (Meta)
- Mistral Large (Mistral AI)
- Qwen 2.5 (Alibaba)

Both **proprietary API models** and **open-source models** are included.

---

## ⚙️ How It Works

The system follows a simple decision pipeline:
User Use Case
↓
Use Case Classification
↓
Token Estimation
↓
Cost Calculation
↓
Policy-based Scoring
↓
Model Recommendation


The recommendation is based on:

- Task suitability
- Estimated token usage
- API pricing
- Model response speed
- Context window limits

The scoring logic is intentionally **rule-based and transparent** rather than using hidden ML models.

---

## 📊 Example Use Cases

You can try queries like:

- *"Summarize a 200 page financial report"*
- *"Build a customer support chatbot using internal documentation"*
- *"Analyze marketing campaign performance data"*
- *"Cluster infrastructure alerts and identify top root causes"*

The tool evaluates multiple models and suggests the most suitable one.

---

## 🏗️ Project Structure


AIModelAdvisor
│
├── app.py # Streamlit application
├── models.json # Model registry (pricing, context window, strengths)
├── classifier.py # Use case classification
├── scoring_rules.py # Scoring policy configuration
├── token_estimator.py # Token estimation using tiktoken
├── cost_calculator.py # Cost calculation logic
├── requirements.txt # Python dependencies
└── .gitignore


---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/teetotalar/AIModelAdvisor.git
cd AIModelAdvisor

Create a virtual environment:

python -m venv .venv

Activate the environment:

Windows

.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py
🔍 Design Principles

This project intentionally focuses on:

Simplicity

Transparency

Explainable scoring

Lightweight dependencies

Easy experimentation

It is not meant to replace benchmarks, but to act as a quick architectural decision aid.

⚠️ Disclaimer

Model pricing, performance, and capabilities change frequently.
All recommendations are heuristic and indicative, not definitive benchmarks.

Always validate model choices based on your actual workload and testing.

📌 Future Improvements

Potential enhancements include:

Expanding the model registry

Adding benchmark references

Incorporating latency measurements

Supporting additional enterprise models

🤝 Contributions

Contributions, suggestions, and improvements are welcome.

If you have ideas to improve the scoring logic or model registry, feel free to open an issue or submit a pull request.

📜 License

MIT License

