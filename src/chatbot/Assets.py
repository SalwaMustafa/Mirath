from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_tavily import TavilySearch
from helpers.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

settings = get_settings()

def get_model():
    llm = ChatGoogleGenerativeAI(
    model = settings.GENERATION_MODEL_ID, 
    temperature = settings.GENERATION_DAFAULT_TEMPERATURE,
    google_api_key = settings.GEMINI_API_KEY
    )
    return llm


def get_arxiv_tool():
    wrapper = ArxivAPIWrapper(
        top_k_results = 3,
        doc_content_chars_max = 1000,
        arxiv_search_sleep_time=3
    )
    return ArxivQueryRun(api_wrapper = wrapper)


def get_tavily_tool():
    
    return TavilySearch(tavily_api_key = settings.TAVILY_API_KEY, max_results = 3)


def get_research_tools():
    return [
        get_tavily_tool(),
        get_arxiv_tool(),
    ]