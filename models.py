models = {
    "GPT-4o": {
        "provider": "OpenAI",
        "input_price": 0.005,
        "output_price": 0.015,
        "strengths": ["marketing", "chatbot", "analysis", "writing"],
        "speed": "Fast",
        "context_window": 128000,
        "pricing_note": "Pay-per-token via OpenAI API"
    },
    "Claude 3.5 Sonnet": {
        "provider": "Anthropic",
        "input_price": 0.003,
        "output_price": 0.015,
        "strengths": ["writing", "marketing", "analysis", "summarization"],
        "speed": "Fast",
        "context_window": 200000,
        "pricing_note": "Pay-per-token via Anthropic API"
    },
    "Gemini 1.5 Pro": {
        "provider": "Google",
        "input_price": 0.0035,
        "output_price": 0.0105,
        "strengths": ["rag", "summarization", "analysis"],
        "speed": "Fast",
        "context_window": 1000000,
        "pricing_note": "Pay-per-token via Google AI API"
    },
    "Llama 3": {
        "provider": "Meta (Open Source)",
        "input_price": 0.0009,
        "output_price": 0.0009,
        "strengths": ["chatbot", "rag", "analysis"],
        "speed": "Medium",
        "context_window": 8192,
        "pricing_note": "Estimated self-hosted / cloud inference cost"
    },
    "Mistral Large": {
        "provider": "Mistral AI",
        "input_price": 0.004,
        "output_price": 0.012,
        "strengths": ["coding", "analysis", "summarization"],
        "speed": "Medium",
        "context_window": 32000,
        "pricing_note": "Pay-per-token via Mistral API"
    },
    "Qwen 2.5": {
        "provider": "Alibaba (Open Source)",
        "input_price": 0.0008,
        "output_price": 0.0025,
        "strengths": ["coding", "chatbot", "analysis"],
        "speed": "Fast",
        "context_window": 128000,
        "pricing_note": "Estimated self-hosted / cloud inference cost"
    }
}