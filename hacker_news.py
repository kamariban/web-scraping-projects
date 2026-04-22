from bs4 import BeautifulSoup
import requests
import pprint

def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'])

def create_custom_hacker_news(pages):
    hn = []

    for soup in pages:
        posts = soup.select('.athing')

        for post in posts:
            title_tag = post.select_one('span.titleline a')
            title = title_tag.get_text()
            link = title_tag.get('href')

            # get the subtext row (next sibling)
            subtext = post.find_next_sibling('tr').select_one('.subtext')
            vote = subtext.select_one('.score')

            if vote:
                points = int(vote.get_text().split()[0])

                hn.append({
                    'title': title,
                    'link': link,
                    'votes': points
                })

    return sort_stories_by_votes(hn)


# pages
soup1 = get_soup('https://news.ycombinator.com/news')
soup2 = get_soup('https://news.ycombinator.com/news?p=2')
soup3 = get_soup('https://news.ycombinator.com/news?p=3')

result = create_custom_hacker_news([soup1, soup2, soup3])

#pprint.pprint(result)
print(result)
