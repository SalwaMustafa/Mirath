from crewai import Task, Agent
from model import llm
from .tools.FetchCategory import fetch_categories
from .scheme import CategoryPaperQueries
import os


Fetch_Agent = Agent(
    role="Category Fetcher",
    goal="Fetch all categories from arXiv taxonomy.",
    backstory="An assistant specialized in collecting and organizing arXiv research categories.",
    tools=[fetch_categories],
    llm=llm,
    verbose=True
)

Fetch_Task = Task(
    description=("""
        Fetch all main and sub research categories from arXiv using the fetch_recent_papers tool. 
        It is CRITICAL that the output from the tool, which is a dictionary like {'Computer Science': ['cs.AI :Artificial Intelligence', ...]}, "
        is returned EXACTLY as is, without removing the codes.
                 """),
    agent=Fetch_Agent,
    expected_output="JSON file containing a dictionary: {category: [list of paper titles]}",
    output_json=CategoryPaperQueries,
    output_file=os.path.join("CrewArtifactsEX", "CategoryCollection.json"),
)
