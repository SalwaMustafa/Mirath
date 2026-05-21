from langchain_core.tools import StructuredTool
from langchain_tavily import TavilySearch
from tavily import TavilyClient
from helpers.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI
import arxiv
import asyncio
import logging
import re

class ResearchTools:

    def __init__(self):

        self.settings = get_settings()
        self.tavily_client = TavilyClient(api_key = self.settings.TAVILY_API_KEY)
        self.tavily_tool = TavilySearch(tavily_api_key = self.settings.TAVILY_API_KEY, max_results = 3)
        self.arxiv_client = arxiv.Client(page_size = 5, delay_seconds = 5, num_retries = 1)
        self.logger = logging.getLogger(__name__)

    def get_model(self):
        return ChatGoogleGenerativeAI(
            model = self.settings.GENERATION_MODEL_ID, 
            temperature = self.settings.GENERATION_DAFAULT_TEMPERATURE,
            google_api_key = self.settings.GEMINI_API_KEY
        )
         

    async def search_research_papers(self, query: str):

        try:
            tavily_query = f"{query} site:arxiv.org"

            response = await asyncio.to_thread(
                lambda: self.tavily_client.search(
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
                id_list=paper_ids,
                max_results=5,
                sort_by=arxiv.SortCriterion.Relevance
            )

            results = await asyncio.to_thread(
                lambda: list(self.arxiv_client.results(search))
            )

            if not results:
                return "No arXiv metadata found."

            papers_content = []
            for paper in results:
                authors = ", ".join(
                    [a.name for a in paper.authors[:3]]
                )

                content = [
                    f"title: {paper.title}",
                    f"authors: {authors}",
                    f"published: {str(paper.published.date())}",
                    f"summary: {paper.summary}",
                    f"pdf_url: {paper.pdf_url}"
                ]
                papers_content.append("\n".join(content))

            return "\n\n".join(papers_content)

        except Exception as e:
            self.logger.error(f"arXiv search failed: {e}")
            return (
                "arxiv search failed temporarily. "
                "Continue using available knowledge."
            )

    async def safe_tavily(self, query: str):

        try:
            result = await self.tavily_tool.ainvoke(query)
            if not result:
                return "No web search results found."

            return result

        except Exception as e:
            self.logger.error(f"Tavily search failed: {e}")
            return f"""
            Tavily search failed temporarily.
            Error: {str(e)}
            Continue using available knowledge.
            """

    def get_arxiv_tool(self):
        return StructuredTool.from_function(
            coroutine=self.search_research_papers,
            name="research_paper_search",
            description="Search for academic papers on arXiv."
        )

    def get_tavily_tool(self):
        return StructuredTool.from_function(
            coroutine=self.safe_tavily,
            name="tavily_search",
            description="Use this for everything that needs live data."
        )

    def get_research_tools(self):
        return [
            self.get_tavily_tool(),
            self.get_arxiv_tool(),
        ]
    