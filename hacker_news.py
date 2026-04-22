from bs4 import BeautifulSoup
import requests
import pprint

# fetch html from a url and parse it into a beautifulsoup object
# this lets us navigate and search the page like a tree
def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')


# sort stories by vote count (lowest → highest here)
# change reverse=true if you want highest first
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'])


# main function: extract structured data from multiple hacker news pages
def create_custom_hacker_news(pages):
    hn = []

    # loop through each page (each "soup" is one full html document)
    for soup in pages:

        # each post on hacker news is inside a <tr class="athing">
        # rhis grabs all posts on the page
        posts = soup.select('.athing')

        # process each post individually
        for post in posts:

            # inside each post, the title and link are in:
            # <span class="titleline"> → <a>
            title_tag = post.select_one('span.titleline a')

            # extract visible text (title) and href (link)
            title = title_tag.get_text()
            link = title_tag.get('href')

            # hacker news stores metadata (votes, author, comments)
            # in the next table row, not the same one
            # so move to the next sibling <tr>
            subtext = post.find_next_sibling('tr').select_one('.subtext')

            # votes are inside: <span class="score">123 points</span>
            vote = subtext.select_one('.score')

            # only want to include posts where votes exist
            if vote:
                # extract the number from "123 points"
                # split() -> ["123", "points"] -> take first element ["123"] -> convert to int  
                points = int(vote.get_text().split()[0])

                # store structured data as a dictionary
                hn.append({
                    'title': title,
                    'link': link,
                    'votes': points
                })

    # return the sorted list of stories
    return sort_stories_by_votes(hn)


# pages to scrape (first 3 pages of hacker news)
soup1 = get_soup('https://news.ycombinator.com/news')
soup2 = get_soup('https://news.ycombinator.com/news?p=2')
soup3 = get_soup('https://news.ycombinator.com/news?p=3')
soup4 = get_soup('https://news.ycombinator.com/news?p=4')

# combine pages and process them
result = create_custom_hacker_news([soup1, soup2, soup3, soup4])

pprint.pprint(result)# pretty print

# print(result)  # raw print