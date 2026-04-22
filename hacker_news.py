from bs4 import BeautifulSoup
import requests
import pprint

# Fetch HTML from a URL and parse it into a BeautifulSoup object
# This lets us navigate and search the page like a tree
def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')


# Sort stories by vote count (lowest → highest here)
# Change reverse=True if you want highest first
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'])


# Main function: extract structured data from multiple Hacker News pages
def create_custom_hacker_news(pages):
    hn = []

    # Loop through each page (each "soup" is one full HTML document)
    for soup in pages:

        # Each post on Hacker News is inside a <tr class="athing">
        # Rhis grabs all posts on the page
        posts = soup.select('.athing')

        # Process each post individually
        for post in posts:

            # Inside each post, the title and link are in:
            # <span class="titleline"> → <a>
            title_tag = post.select_one('span.titleline a')

            # Extract visible text (title) and href (link)
            title = title_tag.get_text()
            link = title_tag.get('href')

            # Hacker News stores metadata (votes, author, comments)
            # in the NEXT table row, not the same one
            # So move to the next sibling <tr>
            subtext = post.find_next_sibling('tr').select_one('.subtext')

            # Votes are inside: <span class="score">123 points</span>
            vote = subtext.select_one('.score')

            # Only want to include posts where votes exist
            if vote:
                # Extract the number from "123 points"
                # split() -> ["123", "points"] -> take first element ["123"] -> convert to int  
                points = int(vote.get_text().split()[0])

                # Store structured data as a dictionary
                hn.append({
                    'title': title,
                    'link': link,
                    'votes': points
                })

    # Return the sorted list of stories
    return sort_stories_by_votes(hn)


# Pages to scrape (first 3 pages of Hacker News)
soup1 = get_soup('https://news.ycombinator.com/news')
soup2 = get_soup('https://news.ycombinator.com/news?p=2')
soup3 = get_soup('https://news.ycombinator.com/news?p=3')


# Combine pages and process them
result = create_custom_hacker_news([soup1, soup2, soup3])



pprint.pprint(result)# pretty print

# print(result)  # raw print 