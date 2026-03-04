import os
from crewai import Crew, Process
from agents import create_researcher_agent, create_scout_agent, create_strategist_agent
from tasks import create_search_task, create_scraping_task, create_analysis_task

def run_competitor_analysis(
    product_name: str, 
    target_domains: list, 
    internal_price: float, 
    currency: str,
    internal_promotion: str, 
    internal_sales: str, 
    internal_rating: float
) -> str:
    """
    Orchestrates the CrewAI process to generate the Competitive Strategy Report.
    """
    # Instantiate agents
    researcher = create_researcher_agent()
    scout = create_scout_agent()
    strategist = create_strategist_agent()
    
    # Create tasks
    search_task = create_search_task(researcher, product_name, target_domains)
    scrape_task = create_scraping_task(scout)
    analysis_task = create_analysis_task(
        strategist, internal_price, currency,
        internal_promotion, internal_sales, internal_rating
    )
    
    # Ensure they pass context sequentially
    scrape_task.context = [search_task]
    analysis_task.context = [scrape_task]
    
    # Form the crew
    crew = Crew(
        agents=[researcher, scout, strategist],
        tasks=[search_task, scrape_task, analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Kickoff the process
    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        return f"An error occurred during the CrewAI execution: {str(e)}"
