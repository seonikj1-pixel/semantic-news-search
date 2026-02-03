from typing import List, Dict
import os

def fallback_summary(results: List[Dict]) -> str:
    if not results:
        return "No results to summarize."
    bullets = []
    for r in results[:5]:
        bullets.append(f"- {r['title']} ({r.get('source','')}): {r['text'][:200]}...")
    return (
        "Summary (fallback):\n"
        "Across the top results, the main themes repeat with differences in emphasis.\n\n"
        "Key snippets:\n" + "\n".join(bullets)
    )

def summarize_results(results: List[Dict]) -> str:
    """
    LLM summarization of the top-K retrieved documents with a safe fallback.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return fallback_summary(results)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        context = "\n\n".join(
            [f"TITLE: {r['title']}\nSOURCE: {r.get('source','')}\nSNIPPET: {r['text']}"
             for r in results[:5]]
        )[:6000]

        prompt = (
            "You are summarizing top search results for a semantic news search app.\n"
            "Write:\n"
            "1) A 3-4 sentence high-level summary of the common themes.\n"
            "2) 5 bullet takeaways.\n"
            "3) A short note on how results differ (framing, emphasis, recency).\n\n"
            f"RESULTS:\n{context}"
        )

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()

    except Exception:
        # Production behavior: do not crash; fall back gracefully
        return fallback_summary(results)
