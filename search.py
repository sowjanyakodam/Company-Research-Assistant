import os
from serpapi import GoogleSearch

def perform_search(query, topn=6, news=False):
    """Single helper function to run web or news search."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SERPAPI_KEY missing in .env")

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": topn,
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us"
    }

    # Google News mode
    if news:
        params["tbm"] = "nws"

    results = GoogleSearch(params).get_dict()
    items = []

    # In Google News, articles are in "organic_results"
    for r in results.get("organic_results", [])[:topn]:
        items.append({
            "title": r.get("title", ""),
            "snippet": r.get("snippet", ""),
            "link": r.get("link", "")
        })

    return items


def clean_results(items):
    """Remove duplicates + empty snippets."""
    seen = set()
    cleaned = []
    for item in items:
        key = (item["title"], item["snippet"])
        if item["snippet"] and key not in seen:
            cleaned.append(item)
            seen.add(key)
    return cleaned


def search_company(company, topn=6):
    """Perform multi-search for deeper company research."""

    all_items = []

    # ------------------- 1. General search -------------------
    general_query = f"{company} company overview profile financials business"
    all_items.extend(perform_search(general_query, topn=topn))

    # ------------------- 2. Products & Services search -------------------
    product_query = f"{company} products services list business segments"
    all_items.extend(perform_search(product_query, topn=topn))

    # ------------------- 3. Competitor search -------------------
    competitor_query = f"{company} competitors rivals alternatives comparison"
    all_items.extend(perform_search(competitor_query, topn=topn))

    # ------------------- 4. News search -------------------
    news_query = f"{company} recent news latest update"
    all_items.extend(perform_search(news_query, topn=topn, news=True))

    # Clean and return
    return clean_results(all_items)
