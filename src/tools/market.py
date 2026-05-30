import warnings
# Suppress the specific deprecation warning to keep our logs clean
warnings.filterwarnings("ignore", category=DeprecationWarning)

# We go back to the reliable community tool
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config import Config

def get_market_search_tool():
    """
    Returns the Tavily Search Tool configured for Ugandan Context.
    """
    tool = TavilySearchResults(
        max_results=3,
        tavily_api_key=Config.TAVILY_API_KEY,
    )
    tool.name = "market_research"
    tool.description = "Use this to search for real-time prices, venues, and trends in Uganda."
    return tool