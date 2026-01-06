from crewai import Agent,Task
from .tools.FetchPaperLinks import search_arxiv_by_category_code
from model import llm
from .scheme import ArxivPapersOutput
from .CollectCategory import Fetch_Task
import os

Search_Agent = Agent(
    role="ArXiv Paper Searcher",
    goal="Find recent paper titles and their links for given arXiv category codes.",
    backstory=(
        "You are an expert at querying the arXiv API. "
        "You use the 'search_arxiv_by_category_code' tool to fetch papers "
        "for each category code provided to you."
    ),
    tools=[search_arxiv_by_category_code],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


    
Search_Task = Task(
        description=(    
            "You must search for papers in these arXiv categories\n"
            "For each category code above:\n"
            "1. Use the 'search_arxiv_by_category_code' tool with the category code\n"
            "2. Set max_results={limit}\n"
            "3. Collect the results\n\n"
            "IMPORTANT: You MUST call the tool once for each category code listed above.\n"
            "Do not skip any category."
        ),
        agent=Search_Agent,
        expected_output=(
            "A JSON object with a 'papers' key containing a list of paper dictionaries. "
            "Each paper must have 'title', 'link', and 'category' fields."
        ),
        output_json=ArxivPapersOutput,
        output_file=os.path.join("CrewArtifactsEX", "ResearchLinks.json"),
        context = [Fetch_Task]
    )