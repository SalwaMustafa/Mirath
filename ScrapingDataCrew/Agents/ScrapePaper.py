from crewai import Agent,Task
from .tools.ScrapePaper import scrape_paper
from model import llm
from .scheme.PaperContent import ScrapePapersOutput
from .SearchPapers import Search_Task
import os

Scrape_Agent = Agent(
    role="Arxiv Paper Scraper",
    goal="Scrape the full content of research papers from their arXiv page links.",
    backstory=(
       "You are an expert at scraping research papers from arXiv."
       "You use the 'scrape_paper' tool to fetch the full HTML content of each paper given its abstract page link."
    ),
    tools=[scrape_paper],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)
  
Scrape_Task = Task(
        description=(    
           "You must scrape the full content of papers from their arXiv abstract page links."
           "For EACH paper link provided:\n"
           "1. Use the 'scrape_paper' tool with the paper's abstract page link\n"
           "2. Collect the results\n\n"
           "IMPORTANT: You MUST call the tool once for each paper link listed above.\n"
           "Do not skip any paper."
        ),
        agent=Scrape_Agent,
        expected_output=(
            "A JSON object with the full content of each paper."
            " Each paper must have 'title', 'authors', 'citation', 'publishedAt', 'category', 'abstract', and 'content' fields."
        ),
        output_json=ScrapePapersOutput,
        output_file=os.path.join("CrewArtifactsEX", "ScrapePapers.json"),
        context = [Search_Task]
    )