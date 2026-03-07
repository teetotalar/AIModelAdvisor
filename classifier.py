def classify_usecase(text):
    text = text.lower()

    keywords = {
        "marketing": [
            "marketing", "campaign", "brochure", "ad", "advertisement",
            "brand", "promotion", "email blast", "copywriting", "landing page",
            "social media post", "product launch", "slogan", "tagline"
        ],
        "summarization": [
            "summarize", "summary", "summarization", "shorten", "brief",
            "overview", "tldr", "condense", "key points", "highlight",
            "extract", "report", "digest", "abstract"
        ],
        "chatbot": [
            "chatbot", "chat bot", "assistant", "support bot", "virtual agent",
            "conversational", "customer service", "helpdesk", "faq bot",
            "live chat", "dialogue", "respond to users", "answer questions"
        ],
        "rag": [
            "document", "knowledge base", "rag", "retrieval", "pdf",
            "internal docs", "search documents", "file", "database",
            "knowledge management", "enterprise search", "data retrieval"
        ],
        "coding": [
            "code", "coding", "program", "script", "function", "api",
            "software", "develop", "debug", "refactor", "automate",
            "python", "javascript", "sql", "backend", "frontend"
        ],
        "analysis": [
            "analyze", "analysis", "insight", "trend", "compare",
            "evaluate", "assess", "data", "metrics", "dashboard",
            "report", "forecast", "predict", "research"
        ],
    }

    scores = {task: 0 for task in keywords}
    for task, words in keywords.items():
        for word in words:
            if word in text:
                scores[task] += 1

    best = max(scores, key=scores.get)
    # Fall back to "analysis" if nothing matched
    return best if scores[best] > 0 else "analysis"