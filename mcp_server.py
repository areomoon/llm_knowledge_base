"""
MCP server for the LLM Knowledge Base.

Exposes:
  Tools:
    - search_wiki(query)     — full-text search across wiki/concepts/ and wiki/derived/
    - read_article(filename) — read a specific wiki article by filename
  Resources:
    - wiki://index           — returns wiki/index.md content

Run:
    python mcp_server.py
"""

import glob
import os
import re

from mcp.server.fastmcp import FastMCP

WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki")
CONCEPTS_DIR = os.path.join(WIKI_DIR, "concepts")
DERIVED_DIR = os.path.join(WIKI_DIR, "derived")
INDEX_FILE = os.path.join(WIKI_DIR, "index.md")

mcp = FastMCP("llm-knowledge-base")


@mcp.tool()
def search_wiki(query: str) -> str:
    """Full-text search across wiki/concepts/ and wiki/derived/. Returns matching excerpts."""
    terms = [t.lower() for t in query.split() if t]
    if not terms:
        return "Please provide a search query."

    results = []
    search_dirs = [CONCEPTS_DIR, DERIVED_DIR]

    for directory in search_dirs:
        if not os.path.isdir(directory):
            continue
        for filepath in sorted(glob.glob(os.path.join(directory, "*.md"))):
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                continue

            content_lower = content.lower()
            if all(term in content_lower for term in terms):
                rel_path = os.path.relpath(filepath, WIKI_DIR)
                # Extract a short excerpt around the first match
                idx = content_lower.find(terms[0])
                start = max(0, idx - 100)
                end = min(len(content), idx + 300)
                excerpt = content[start:end].strip()
                excerpt = re.sub(r"\s+", " ", excerpt)
                results.append(f"**{rel_path}**\n> ...{excerpt}...\n")

    if not results:
        return f"No results found for: {query}"

    return f"Found {len(results)} result(s) for '{query}':\n\n" + "\n".join(results)


@mcp.tool()
def read_article(filename: str) -> str:
    """Read a specific wiki article. Accepts filenames like 'context-engineering.md'
    or paths like 'concepts/context-engineering.md'."""
    # Strip leading slashes or 'wiki/' prefix
    filename = filename.lstrip("/")
    if filename.startswith("wiki/"):
        filename = filename[len("wiki/"):]

    # Try exact path relative to wiki/
    candidates = [
        os.path.join(WIKI_DIR, filename),
        os.path.join(CONCEPTS_DIR, filename),
        os.path.join(DERIVED_DIR, filename),
    ]

    for path in candidates:
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                return f.read()

    # Fuzzy: find any .md in wiki/ whose basename matches
    for directory in [CONCEPTS_DIR, DERIVED_DIR, WIKI_DIR]:
        if not os.path.isdir(directory):
            continue
        for filepath in glob.glob(os.path.join(directory, "*.md")):
            if os.path.basename(filepath) == os.path.basename(filename):
                with open(filepath, encoding="utf-8") as f:
                    return f.read()

    return f"Article not found: {filename}\nTry search_wiki() to locate the right filename."


@mcp.resource("wiki://index")
def wiki_index() -> str:
    """Returns the wiki/index.md navigation page."""
    if not os.path.isfile(INDEX_FILE):
        return "wiki/index.md not found."
    with open(INDEX_FILE, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
