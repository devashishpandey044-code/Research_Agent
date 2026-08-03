from langchain_core.tools import tool

import arxiv
import wikipediaapi
from langchain_community.tools import DuckDuckGoSearchRun

from rag import get_rag_chain

# ---------------- WIKIPEDIA ---------------- #

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="ResearchGPT/1.0"
)

# ---------------- DUCKDUCKGO ---------------- #

duck = DuckDuckGoSearchRun()

# ---------------- LOAD RAG CHAIN ---------------- #

try:
    rag_chain = get_rag_chain()
except Exception:
    rag_chain = None


# ---------------- PDF RESEARCH ---------------- #

@tool
def pdf_research(query: str) -> str:
    """
    Search the uploaded PDF research papers stored in the local Chroma vector database.

    Use this tool whenever the user's question refers to:
    - uploaded PDF
    - uploaded research paper
    - this paper
    - this PDF
    - summarize the uploaded paper
    - explain the uploaded paper
    - methodology
    - conclusion
    - results
    - dataset
    - architecture
    - limitations
    - findings
    - any follow-up question about an uploaded paper

    Input:
        A natural language question.

    Output:
        The answer retrieved from the uploaded research papers.
    """

    global rag_chain

    try:

        if rag_chain is None:
            rag_chain = get_rag_chain()

        print("=" * 60)
        print("PDF TOOL CALLED")
        print("Question:", query)
        print("=" * 60)

        return rag_chain.invoke(query)

    except Exception as e:
        return f"PDF Search Error:\n{str(e)}"


# ---------------- ARXIV ---------------- #

@tool
def arxiv_search(query: str) -> str:
    """
    Search arXiv for research papers that are NOT part of the uploaded PDFs.

    Use this tool when the user asks for:
    - latest research papers
    - papers on a topic
    - arXiv papers
    - recommendations of research papers

    Input:
        Research topic.

    Output:
        Relevant research papers from arXiv.
    """

    try:

        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []

        for paper in search.results():

            papers.append(
                f"""
Title: {paper.title}

Authors:
{', '.join(a.name for a in paper.authors)}

Published:
{paper.published.date()}

Summary:
{paper.summary}

PDF:
{paper.pdf_url}

----------------------------------------
"""
            )

        if len(papers) == 0:
            return "No research papers found."

        return "\n".join(papers)

    except Exception as e:
        return f"Arxiv Error:\n{e}"


# ---------------- WIKIPEDIA ---------------- #

@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for general concepts, definitions and background knowledge.

    Use this tool for:
    - AI concepts
    - Machine Learning concepts
    - Deep Learning concepts
    - Algorithms
    - General scientific terms

    Input:
        Topic name.

    Output:
        Wikipedia summary.
    """

    try:

        page = wiki.page(query)

        if not page.exists():
            return "No Wikipedia article found."

        return page.summary[:3000]

    except Exception as e:
        return f"Wikipedia Error:\n{e}"


# ---------------- WEB SEARCH ---------------- #

@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Use this tool for:
    - recent news
    - GitHub repositories
    - documentation
    - official websites
    - latest AI developments
    - information not available in uploaded PDFs

    Input:
        Search query.

    Output:
        Relevant web search results.
    """

    try:
        return duck.run(query)

    except Exception as e:
        return f"DuckDuckGo Error:\n{e}"


# ---------------- TOOL LIST ---------------- #

tools = [
    pdf_research,
    arxiv_search,
    wikipedia_search,
    web_search,
]