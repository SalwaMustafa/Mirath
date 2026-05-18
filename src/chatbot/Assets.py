from langchain_core.tools import StructuredTool
from langchain_tavily import TavilySearch
from tavily import TavilyClient
from helpers.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI
import arxiv
import asyncio
import logging
import re

logger = logging.getLogger(__name__)
settings = get_settings()

def get_model():
    llm = ChatGoogleGenerativeAI(
    model = settings.GENERATION_MODEL_ID, 
    temperature = settings.GENERATION_DAFAULT_TEMPERATURE,
    google_api_key = settings.GEMINI_API_KEY
    )
    return llm


def get_arxiv_tool():

    async def search_research_papers(query: str):

        try:
            
            tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
            client = arxiv.Client()

            tavily_query = f"{query} site:arxiv.org"

            response = await asyncio.to_thread(
                lambda: tavily.search(
                    query=tavily_query,
                    max_results=5
                )
            )

            if not response or "results" not in response:
                return "No research papers found."

            paper_ids = []
            pattern = r'((?:\d{4}\.\d{4,5})|(?:[a-z\-]+(?:\.[A-Z]{2})?\/\d{7}))'

            for result in response["results"]:

                url = result.get("url", "")

                match = re.search(pattern, url)

                if match:
                    paper_ids.append(match.group(1))

            if not paper_ids:
                return "No valid arXiv papers found."

            paper_ids = list(dict.fromkeys(paper_ids))

            search = arxiv.Search(
                id_list=paper_ids
            )

            await asyncio.sleep(1)

            results = await asyncio.to_thread(
                lambda: list(client.results(search))
            )

            if not results:
                return "No arXiv metadata found."

            papers_content = []

            for paper in results:

                content = []
                authors = ", ".join(
                    [a.name for a in paper.authors[:3]]
                )

                content.append(f"title: {paper.title}")
                content.append(f"authors: {authors}")
                content.append(f"published: {str(paper.published.date())}")
                content.append(f"summary: {paper.summary}")
                content.append(f"pdf_url: {paper.pdf_url}")

                papers_content.append("\n".join(content))


            return "\n\n".join(papers_content)

        except Exception as e:
            logger.exception(f"arXiv search failed: {e}")
            return ""

    return StructuredTool.from_function(
        coroutine = search_research_papers,
        name = "research_paper_search",
        description ="Search for academic papers on arXiv."
                        )


def get_tavily_tool():

    tavily_tool = TavilySearch(
        tavily_api_key=settings.TAVILY_API_KEY,
        max_results=3
    )

    async def safe_tavily(query: str):

        try:
            result = await tavily_tool.ainvoke(query)

            if not result:
                return "No web search results found."

            return result

        except Exception as e:
            logger.exception(f"Tavily search failed: {e}")
            return f"""
            Tavily search failed temporarily.
            Error: {str(e)}

            Continue using available knowledge.
            """

    return StructuredTool.from_function(
        coroutine = safe_tavily,
        name = "tavily_search",
        description = "Use this for everything that needs live data."
    )

def get_research_tools():
    return [
        get_tavily_tool(),
        get_arxiv_tool(),
    ]
