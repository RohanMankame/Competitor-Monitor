import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import Field
from firecrawl import FirecrawlApp

load_dotenv()

class FirecrawlScrapeTool(BaseTool):
    name: str = "FirecrawlScrapeTool"
    description: str = "Scrapes the content of a target URL and returns markdown. Input should be a valid URL as a string."
    
    def _run(self, url: str) -> str:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key or api_key == "your_firecrawl_api_key_here":
            return "Error: FIRECRAWL_API_KEY is not set or is invalid in the environment."
        
        try:
            app = FirecrawlApp(api_key=api_key)
            scrape_result = app.scrape(url, formats=['markdown'])
            if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                return scrape_result.markdown
            elif isinstance(scrape_result, dict) and 'markdown' in scrape_result:
                return scrape_result['markdown']
            else:
                return f"Error: Firecrawl did not return markdown."
        except Exception as e:
            return f"Error scraping the URL with Firecrawl: {str(e)}"
        


        

class FirecrawlSearchTool(BaseTool):
    name: str = "FirecrawlSearchTool"
    description: str = "Searches the web for a query and returns related URLs. Use this to find competitor product pages."
    
    def _run(self, query: str) -> str:
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key or api_key == "your_firecrawl_api_key_here":
            return "Error: FIRECRAWL_API_KEY is not set or is invalid in the environment."
        
        try:
            app = FirecrawlApp(api_key=api_key)
            # The search endpoint acts like a standard search engine.
            search_result = app.search(query)
            
            # The v2 SDK returns a SearchResponse object with a `web` array of result dictionaries
            if not hasattr(search_result, 'web') or not search_result.web:
                return f"No search results found for query: {query}"
                
            urls = []
            for item in search_result.web[:5]: # Only take top 5 to keep context window manageable
                if isinstance(item, dict) and 'url' in item:
                    urls.append(item['url'])
                elif hasattr(item, 'url'):
                    urls.append(item.url)
                    
            if not urls:
                return "Failed to extract URLs from search results."
                
            return "Found the following competitor product URLs:\n" + "\n".join(urls)
        except Exception as e:
            return f"Error searching with Firecrawl: {str(e)}"
