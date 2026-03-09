def classify_usecase(text):

    text = text.lower()

    keywords = {
        "marketing": ["marketing","campaign","advertisement","brand","promotion"],
        "summarization": ["summarize","summary","condense","overview","brief"],
        "chatbot": ["chatbot","assistant","support","faq","customer service"],
        "rag": ["document","knowledge base","retrieval","pdf","internal docs"],
        "coding": ["code","script","program","api","debug","python","javascript"],
        "analysis": ["analyze","analysis","trend","compare","metrics","data","insight"]
    }

    scores = {k:0 for k in keywords}

    for task, words in keywords.items():
        for w in words:
            if w in text:
                scores[task]+=1

    best = max(scores, key=scores.get)

    return best if scores[best] > 0 else "analysis"
