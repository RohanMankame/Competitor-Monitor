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
        
        For EACH URL, your objective is to EXTRACT THE FOLLOWING 5 KEY METRICS:
        1. The main product name/title/URL.
        2. The current selling price of the product (scan carefully to differentiate between regular and discounted price).
        3. Any original/strike-through prices or active discounts.
        4. Any promotional banners or text (e.g., "Buy 1 Get 1", "20% off with code", "Prime Delivery").
        5. The product's star rating and number of reviews (or sales volume if available).
        
        CRITICAL: Do not quickly give up and say "not available". Scroll through the raw markdown text provided by the scraper thoroughly and try multiple angles to infer the price, ratings, and promotions accurately based on the visual context and surrounding text. Present your findings clearly for EVERY URL you process and explicitly list out all 5 metrics for each.""",
        expected_output="A structured and comprehensive summary containing the product title, current price, original price/discounts, ongoing promotions, and star rating/reviews extracted from EACH of the provided pages. Never use 'not available' unless you have exhaustively checked the page.",
        agent=agent
    )

def create_analysis_task(
    agent, 
    internal_price: float, 
    currency: str,
    internal_promotion: str, 
    internal_sales: str, 
    internal_rating: float
) -> Task:
    """
    Task for the Strategist to analyze the data and generate a strategic plan.
    """
    return Task(
        description=f"""You have the Scout's report containing pricing and promotional data from multiple competitor product pages.
        
        Our Internal Base Price for this product (or a functionally identical equivalent) is: {internal_price} {currency}.
        Our Internal Promotion/Discount: {internal_promotion}.
        Our Internal Sales Volume: {internal_sales}.
        Our Internal Star Rating: {internal_rating} out of 5.
        
        CRITICAL COMPARISON TASK:
        Compare the competitors' aggregated extracted metrics against ALL of our internal metrics specified above. You MUST analyze:
        1. Price: Identify the lowest, highest, and average competitor price from the Scout's data, and compare it strictly against our {internal_price} {currency}.
        2. Promotions/Discounts: Compare the competitors' promotional strategies with our internal promotion ({internal_promotion}).
        3. Ratings/Reviews: Compare competitors' ratings directly with our internal rating of {internal_rating} out of 5.
        4. Sales Volume: Estimate their popularity vs our internal sales ({internal_sales}).
        
        Draft a high-impact "Competitive Strategy Report". Make SURE no metric is left uncompared.
        Based on this multi-dimensional assessment, state clearly which of the following tactical moves we should make:
        - "LOWER PRICE": If they have a better overall value (lower price/better promos) and we can match.
        - "INCREASE AD SPEND": If we are cheaper but they are running heavier promotions or have way better ratings.
        - "HOLD": If our price is competitive, we have strong ratings, and they have no strong promotions.
        - "OVERHAUL VALUE PROP": If they are massively cheaper AND have better ratings AND stronger promotions.
        -If there are better options, feel free to suggest them with clear justification.
        
        Provide the strategic reasoning behind your tactical move based on the full metric comparison.""",
        expected_output="A detailed 'Competitive Strategy Report' formatted in Markdown. It must include the extracted competitor data, a rigorous comparison of EVERY internal metric (price, promotion, sales, ratings) against market reality, the chosen tactical move, and strategic reasoning.",
        agent=agent
    )
