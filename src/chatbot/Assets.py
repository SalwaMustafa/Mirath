from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_community.tools import TavilySearch
from helpers.config import get_settings

settings = get_settings()

def get_arxiv_tool():
    wrapper = ArxivAPIWrapper(
        top_k_results = 1,
        doc_content_chars_max = 1000
    )
    return ArxivQueryRun(api_wrapper = wrapper)


def get_tavily_tool():
    
    return TavilySearch(tavily_api_key = settings.TAVILY_API_KEY, max_results = 1)


def get_research_tools():
    return [
        get_tavily_tool(),
        get_arxiv_tool(),
    ]