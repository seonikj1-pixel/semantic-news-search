import streamlit as st

st.set_page_config(page_title="Semantic News Search", layout="wide")
st.title("Semantic News Search (Embeddings + LLM Summaries)")

st.write("✅ App loaded successfully. Enter a query and click Search.")

query = st.text_input("Search query", value="AI regulation")
top_k = st.slider("Top-K results", min_value=3, max_value=10, value=5)

col1, col2 = st.columns(2)
with col1:
    do_search = st.button("Search", type="primary")
with col2:
    do_summarize = st.button("Summarize top results")

# Import lazily so errors show in UI instead of blank screen
try:
    from src.search import search
    from src.llm import summarize_results
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

results = None

if do_search and query.strip():
    try:
        results = search(query, top_k=top_k)
        st.subheader("Top Results")
        for r in results:
            st.markdown(f"### [{r['score']:.3f}] {r['title']}")
            st.caption(f"{r.get('source','')} | {r.get('published_at','')}")
            st.write(r["text"])
            st.write(r["url"])
            st.divider()
    except Exception as e:
        st.error(f"Search failed: {e}")

if do_summarize:
    try:
        if results is None and query.strip():
            results = search(query, top_k=top_k)
        st.subheader("Summary")
        st.write(summarize_results(results or []))
    except Exception as e:
        st.error(f"Summarization failed: {e}")
