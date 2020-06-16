from functions import get_soup_lxml


def get_search_results(search_text, exact):
    url = 'https://www.boardgamegeek.com/xmlapi/search?search='+search_text+'&exact=1'*exact
    soup = get_soup_lxml(url)
    all_bg = soup.find_all('boardgame', inbound=False)
    oids = []
    for boardgame in all_bg:
        oids.append(boardgame['objectid'])
    apiurl = 'https://www.boardgamegeek.com/xmlapi/boardgame/'+','.join(oids)
    get_soup_lxml(apiurl)


get_search_results('gloom', 0)