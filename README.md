# Web Scraping Projects

A collection of web scraping projects built using Python.  
These projects focus on extracting, cleaning, and working with data from real websites.

---

## Project: Hacker News Scraper

This script scrapes the front pages of Hacker News and extracts:

- Title of each post  
- Link to the article  
- Number of upvotes
  
The results are sorted by vote count.

---
## How It Works
- Sends requests to Hacker News pages  
- Parses HTML using BeautifulSoup  
- Extracts post data from the page structure  
- Stores results in a list of dictionaries  
- Sorts posts based on vote count  
---

## How to Run

1. Save the script (for example: `hacker_news.py`)

2. Open a terminal in the project folder

3. Run:

python hacker_news.py

---

## Example Output

Each result looks like:

{
  'title': 'Example Post',
  'link': 'https://example.com',
  'votes': 123
}


