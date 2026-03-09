# Competitor Strategy Agent

The **AI Competitor Strategy Dashboard** is an intelligent e-commerce analysis tool powered by CrewAI and Streamlit. It orchestrates a team of specialized AI agents to scout the web for competitor products, extract pricing and promotional data, and generate actionable strategic recommendations by comparing market realities against your internal product metrics.

## Features

- **Automated Web Research**: Employs a Market Researcher agent to automatically find exact-match competitor product pages across selected target domains (e.g., Amazon, Flipkart) or the broader web.
- **Data Scraping & Extraction**: Uses a Competitive Intelligence Scout agent equipped with Firecrawl to scrape competitor pricing, active discounts, promotional banners, and user ratings directly from product URLs.
- **Strategic Analysis**: A Strategist agent analyzes gathered market data against your provided internal metrics (base price, promotions, target sales, and expected ratings).
- **Actionable Insights**: Generates a rich, multi-dimensional "Competitive Strategy Report" recommending tactical moves such as "LOWER PRICE", "INCREASE AD SPEND", "HOLD", or "OVERHAUL VALUE PROP".
- **Interactive UI**: An intuitive, easy-to-use Streamlit dashboard for entering product details, target domains, and internal metrics.

## Prerequisites

Before running this application, you will need the following API keys configured in a `.env` file in the root directory:

- `OPENAI_API_KEY`: Required by LangChain/CrewAI for the underlying LLMs.
- `FIRECRAWL_API_KEY`: Required by the `FirecrawlSearchTool` and `FirecrawlScrapeTool` to perform web searches and scrape site content.

## Installation

1. **Clone the repository** (if not already local):
   ```bash
   git clone <repository_url>
   cd Competitor-Monitor
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Ensure you have a `.env` file containing your API keys:
   ```env
   OPENAI_API_KEY="sk-..."
   FIRECRAWL_API_KEY="fc-..."
   ```

## Usage

Start the Streamlit web application:

```bash
streamlit run app.py
```

1. Open the provided local URL (typically `http://localhost:8501`) in your browser.
2. Enter the **Product Name / Search Query** (e.g., *Apple AirPods Pro 2*).
3. Select any **Target Domains** you want to focus on (or leave blank for universal search).
4. Enter your **Internal Base Price**, **Currency**, **Promotion/Discount**, **Sales Volume**, and **Star Rating**.
5. Click **Run Strategic Analysis**.
6. Wait 1-2 minutes while the AI agents gather and process the data to produce your report.

## How It Works (The Crew)

The application runs a sequential CrewAI process with three distinct agents:

1. **Market Researcher (`agents.py`)**: Uses the web search tool to find direct product URLs based on the user's query and target domains.
2. **Competitive Intelligence Scout (`agents.py`)**: Takes the URLs from the researcher, scrapes the product pages, and extracts structured key metrics (price, discounts, ratings, promotions).
3. **E-commerce Strategy Consultant (`agents.py`)**: Takes the scraped market data and compares it against the provided internal data to decide on the best tactical move and formulate the final strategic report.

## Dependencies

- [Streamlit](https://streamlit.io/) for the frontend UI.
- [CrewAI](https://github.com/joaomdmoura/crewAI) for orchestrating the AI agents.
- [Firecrawl](https://firecrawl.dev/) for web search and scraping.
- [LangChain](https://python.langchain.com/) / OpenAI for AI reasoning.
- `python-dotenv` for environment management.
- `pydantic` for structured data models.
