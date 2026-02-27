import os
from dotenv import load_dotenv
from crewai import Agent
from tools import FirecrawlScrapeTool, FirecrawlSearchTool

load_dotenv()

def create_researcher_agent() -> Agent:
    """
    Instantiates the 'Researcher' agent for locating competitor product pages.
    """
    search_tool = FirecrawlSearchTool()
    
    return Agent(
        role='Market Researcher',
        goal='Find relevant competitor product URLs across specified domains or the broader web.',
        backstory="""You are an expert market researcher. Your job is to take a product name 
        (and optionally some target domains) and construct effective search queries. 
        You use your search tool to compile a list of authoritative, exact-match 
        product page URLs for your team to analyze. You only care about finding the correct URLs.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool]
    )

def create_scout_agent() -> Agent:
    """
    Instantiates the 'Scout' agent for competitive intelligence gathering.
    """
    scrape_tool = FirecrawlScrapeTool()
    
    return Agent(
        role='Competitive Intelligence Scout',
        goal='Extract competitor pricing, discounts, and product details from multiple URLs.',
        backstory="""You are the best data scout in the e-commerce industry. 
        You receive a list of product URLs found by the Researcher. Your specialty is 
        navigating to EACH of these competitor products incrementally and figuring out exactly 
        how much they charge, what discounts they are running, and uncovering hidden 
        promotional details. You excel at extracting structured, tabular facts from messy markdown pages 
        so that the Strategist can compare them.""",
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool]
    )

def create_strategist_agent() -> Agent:
    """
    Instantiates the 'Strategist' agent for generating the Competitive Strategy Report.
    """
    return Agent(
        role='E-commerce Strategy Consultant',
        goal='Analyze competitor data against internal metrics to recommend actionable counter-strategies.',
        backstory="""You are an analytical, data-driven e-commerce strategist. 
        You look at competitor pricing and current internal baselines, and you formulate 
        insightful but realistic strategic plans ('Competitive Strategy Reports'). 
        You decide whether to "Buy" (meaning undercut), "Lower Price", "Increase Ad Spend", 
        or "Hold" based on margins and competitor moves.""",
        verbose=True,
        allow_delegation=False
    )
