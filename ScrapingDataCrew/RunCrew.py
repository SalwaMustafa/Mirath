from crewai import Crew, Process
from Agents.CollectCategory import Fetch_Agent,Fetch_Task
from Agents.SearchPapers import Search_Agent,Search_Task
from Agents.ScrapePaper import Scrape_Agent,Scrape_Task

crew = Crew(
    agents=[
        Fetch_Agent,
        Search_Agent,
        Scrape_Agent,

    ],
    tasks=[
        Fetch_Task,
        Search_Task,
        Scrape_Task,
    ],
    process=Process.sequential,
    verbose=True,
    
)

crew.kickoff(
        inputs={ "limit": 1 },
)