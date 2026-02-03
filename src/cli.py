import argparse

from .ingest import ingest_rss
from .preprocess import preprocess
from .embed import build_index
from .search import search as run_search
from .llm import summarize_results


def main():
    parser = argparse.ArgumentParser(prog="semantic-news-search")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest", help="Download news articles from RSS feeds")
    p_ing.add_argument("--limit", type=int, default=150, help="Max number of articles to ingest")

    sub.add_parser("preprocess", help="Clean and normalize raw articles")
    sub.add_parser("build-index", help="Create embeddings and save an index")

    p_search = sub.add_parser("search", help="Semantic search over the indexed corpus")
    p_search.add_argument("--query", type=str, required=True, help="Search query")
    p_search.add_argument("--top_k", type=int, default=5, help="Number of results to return")
    p_search.add_argument("--summarize", action="store_true", help="Summarize top-K results")

    args = parser.parse_args()

    if args.cmd == "ingest":
        n = ingest_rss(limit=args.limit)
        print(f"Ingested {n} articles to data/raw.")
    elif args.cmd == "preprocess":
        n = preprocess()
        print(f"Preprocessed {n} docs to data/processed.")
    elif args.cmd == "build-index":
        n = build_index()
        print(f"Built index for {n} docs in data/index.")
    elif args.cmd == "search":
        results = run_search(args.query, args.top_k)
        for r in results:
            print(f"\n[{r['score']:.3f}] {r['title']}")
            print(f"  {r.get('source','')} | {r.get('published_at','')}")
            print(f"  {r['url']}")
        if args.summarize:
            print("\n" + "=" * 60)
            print(summarize_results(results))


if __name__ == "__main__":
    main()
