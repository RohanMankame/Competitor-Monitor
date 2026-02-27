from crewai import Task

def create_search_task(agent, product_name: str, target_domains: list) -> Task:
    """
    Task for the Researcher to find product URLs.
    """
    domains_str = ", ".join(target_domains) if target_domains else "the broader web"
    return Task(
        description=f"""Your objective is to find exact-match product pages for the following product: '{product_name}'.
        
        Focus your search on these target domains: {domains_str}.
        Use your scraping/search tool to perform web queries (e.g. '{product_name} site:amazon.in').
        
        Compile a list of up to 3 valid, direct product URLs where this item is currently sold.
        Do NOT return search result pages, only direct product pages.""",
        expected_output="A list of 1 to 3 direct competitor product URLs.",
        agent=agent
    )

def create_scraping_task(agent) -> Task:
    """
    Task for the Scout to scrape the competitor URLs found by the Researcher.
    """ 
    return Task(
        description=f"""You will receive a list of product URLs found by the Researcher.
        
        Use your scraping tool to visit EACH competitor product URL provided.
        
        For EACH URL, your objective is to extract:
        1. The main product name/title.
        2. The current selling price of the product.
        3. Any original/strike-through prices or active discounts.
        4. Any promotional banners or text (e.g., "Buy 1 Get 1", "20% off with code").
        5. Recent sales volume or popularity metrics (e.g., "1K+ bought in past month", "Best Seller").
        
        Ensure you look at the raw markdown text provided by the scraper and infer the price accurately 
        based on visual context. Present your findings clearly for EVERY URL you process.""",
        expected_output="A structured summary containing the product title, current price, discounts, ongoing promotions, and sales volume extracted from EACH of the provided pages.",
        agent=agent
    )

def create_analysis_task(agent, internal_price: float, currency: str, internal_promotions: str = "") -> Task:
    """
    Task for the Strategist to analyze the data and generate a strategic plan.
    """
    promotions_context = f"\n        Our current internal promotions/discounts: {internal_promotions}" if internal_promotions else ""
    return Task(
        description=f"""You have the Scout's report containing pricing and promotional data from multiple competitor product pages.
        
        Our Internal Base Price for this product (or a functionally identical equivalent) is: {internal_price} {currency}.{promotions_context}
        
        Compare the competitors' aggregated extracted prices, promotions, and sales volume against our Internal Price, internal promotions, and the exact currency specified ({currency}).
        Draft a high-impact "Competitive Strategy Report". Provide actionable recommendations.
        Identify the lowest, highest, and average competitor price from the Scout's data.
        Specifically, state clearly which of the following tactical moves we should make:
        - "LOWER PRICE": If they are significantly cheaper and we can match.
        - "INCREASE AD SPEND": If we are cheaper but they are running heavy promotions.
        - "HOLD": If our price is competitive and they have no strong promotions.
        - "OVERHAUL VALUE PROP": If they are cheaper AND running heavy promotions.
        
        Provide the reasoning behind your tactical move.""",
        expected_output="A detailed 'Competitive Strategy Report' formatted in Markdown, including the extracted competitor data, comparison to internal price, the chosen tactical move, and strategic reasoning.",
        agent=agent
    )
