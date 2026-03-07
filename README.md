# ⚡ AI Model Advisor

AI Model Advisor is a lightweight tool that helps compare different Large Language Models (LLMs) for a given use case.

Instead of guessing which model to use, the tool evaluates multiple models across **task suitability, estimated cost, and response speed** to provide a transparent recommendation.

The goal is to act as a **neutral decision assistant** for selecting the most appropriate model for a specific GenAI use case.

---

## 🌐 Supported Models

The tool currently compares the following models:

- GPT-4o (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
- Gemini 1.5 Pro (Google)
- Llama 3 (Meta)
- Mistral Large (Mistral AI)
- Qwen 2.5 (Alibaba)

Both proprietary API models and open-source models are included.

---

## 🧠 How the Recommendation Works

The system evaluates models using a transparent scoring heuristic based on three factors:

| Factor | Description |
|------|-------------|
| **Task Fit** | Whether the model is well suited for the detected use case (e.g., coding, summarization, chatbot) |
| **Estimated Cost** | Cost calculated from estimated input/output tokens using publicly available pricing |
| **Speed** | Approximate response speed classification (Fast / Medium) |

### Scoring Logic

| Factor | Score |
|------|------|
| Task Fit | 5 points if strong match, 2 points otherwise |
| Cost | 3 points if very low, 2 points if moderate, 1 point if higher |
| Speed | 2 points for Fast, 1 point for Medium |

The model with the **highest total score** is recommended.

---

## 🧮 Token Estimation

Token counts are estimated using the OpenAI tokenizer (`cl100k_base`) as a baseline.

Input tokens are calculated from the user prompt and output tokens are estimated as **50% of the input size**.

This allows approximate cost estimation across different models.

---

## ⚙️ Example Use Cases

The tool automatically detects common GenAI tasks such as:

- Marketing content generation
- Document summarization
- Chatbots / virtual assistants
- Retrieval-augmented generation (RAG)
- Coding assistance
- Data analysis

Example input:

Summarize a 200-page financial report and extract key risks


---

## 🏗 Architecture
User Input
│
▼
Use Case Classifier
│
▼
Token Estimator
│
▼
Cost Calculator
│
▼
Model Scoring Engine
│
▼
Comparison Table + Recommendation


---

## 🖥 Running the Project

### 1. Install dependencies


pip install -r requirements.txt


### 2. Run the application


streamlit run app.py


The tool will open in your browser.

---

## 📊 Example Output

The application provides:

- Recommended model
- Cost estimate
- Speed classification
- Context window information
- Side-by-side comparison of all models

---

## ⚠️ Disclaimer

This tool uses **heuristic scoring** based on public pricing, estimated token usage, and general model capabilities.

It is **not a benchmark system** and results should be treated as indicative guidance rather than definitive performance comparisons.

---

## 💡 Motivation

With the rapid growth of LLM providers, choosing the right model for a given task is increasingly difficult.

AI Model Advisor was built as a simple experiment to explore:

- model selection strategies
- cost estimation across LLM APIs
- transparent decision frameworks for GenAI architecture

---

## 🚀 Future Improvements

Potential enhancements include:

- real benchmark data integration
- live latency measurements
- automated prompt testing across models
- more granular task classification
- model capability database

---

## 📜 License

MIT License
