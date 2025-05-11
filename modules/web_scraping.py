import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re

# Function to perform Google search and return top URLs
def google_search(query, num_results=10):
    search_results = []
    for url in search(query, num_results=num_results):
        search_results.append(url)
    return search_results

# Function to scrape content from a webpage
def scrape_webpage(url):
    print(f"Scraping the webpage: {url}")  # Debugging line
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            return page_content
        else:
            print(f"Failed to fetch {url}, status code {response.status_code}")
            return "Error"
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "Error"

# Function to filter the content based on a query
def filter_content(content, query):
    print(f"Filtering content for query: {query}")  # Debugging line
    soup = BeautifulSoup(content, "html.parser")
    
    # Collect headlines from common heading tags
    headlines = []
    for tag in soup.find_all(['h4', 'h5']):
        text = tag.get_text(strip=True)
        if text and (query.lower() in text.lower() or "news" in text.lower()):
            headlines.append(text)

    if headlines:
        return "Here are some headlines:\n" + "\n".join(headlines[:5])  # return top 5
    else:
        return "Sorry, I couldn't find relevant information."

# Function to handle the command and get data from the web
def handle_web_query(query):
    print(f"Searching for query: {query}")  # Debugging line
    search_results = google_search(query)
    print(f"Found search results: {search_results}")  # Debugging line
    
    for url in search_results:
        print(f"Scraping URL: {url}")  # Debugging line
        scraped_content = scrape_webpage(url)
        if scraped_content != "Error":
            answer = filter_content(scraped_content, query)
            if answer != "Sorry, I couldn't find relevant information.":
                print(f"Answer found: {answer}")  # Debugging line
                return answer

    return "Sorry, I couldn't find an answer to your question."
